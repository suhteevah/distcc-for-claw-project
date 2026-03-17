use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::Utc;
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;
use tracing::{error, info, warn};

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ItemData {
    item_id: String,
    name: String,
    market_value: f64,
    min_buyout: f64,
    quantity: u64,
    historical_price: f64,
    #[serde(default = "default_timestamp")]
    imported_at: String,
}

fn default_timestamp() -> String {
    Utc::now().to_rfc3339()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Reagent {
    item_id: String,
    #[serde(default)]
    item_name: Option<String>,
    quantity: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CraftingRecipe {
    result_item_id: String,
    #[serde(default)]
    result_item_name: Option<String>,
    result_quantity: Option<u64>,
    reagents: Vec<Reagent>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ArbitrageOpportunity {
    item_id: String,
    name: String,
    min_buyout: f64,
    market_value: f64,
    profit_per_unit: f64,
    profit_margin_pct: f64,
    available_quantity: u64,
    total_potential_profit: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CraftingAnalysis {
    result_item: String,
    result_market_value: f64,
    craft_quantity: u64,
    total_reagent_cost: f64,
    profit_per_craft: f64,
    profit_margin_pct: f64,
    reagent_breakdown: Vec<ReagentCost>,
    verdict: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ReagentCost {
    item_id: String,
    name: String,
    quantity_needed: u64,
    unit_price: f64,
    total_cost: f64,
    price_source: String,
}

// ---------------------------------------------------------------------------
// Shared application state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: Arc<OpenClawAgent>,
    items: Arc<DashMap<String, ItemData>>,
    scan_history: Arc<Mutex<Vec<serde_json::Value>>>,
    soul: Arc<String>,
}

// ---------------------------------------------------------------------------
// TSM Import
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct ImportRequest {
    items: Vec<ItemData>,
}

#[derive(Debug, Serialize)]
struct ImportSummary {
    imported_count: usize,
    updated_count: usize,
    total_items_in_store: usize,
    imported_at: String,
}

fn do_import(items_store: &DashMap<String, ItemData>, incoming: Vec<ItemData>) -> ImportSummary {
    let mut imported_count = 0usize;
    let mut updated_count = 0usize;
    let now = Utc::now().to_rfc3339();

    for mut item in incoming {
        item.imported_at = now.clone();
        let key = item.item_id.clone();
        if items_store.contains_key(&key) {
            updated_count += 1;
        } else {
            imported_count += 1;
        }
        items_store.insert(key, item);
    }

    ImportSummary {
        imported_count,
        updated_count,
        total_items_in_store: items_store.len(),
        imported_at: now,
    }
}

async fn import_endpoint(
    State(state): State<AppState>,
    Json(req): Json<ImportRequest>,
) -> impl IntoResponse {
    let summary = do_import(&state.items, req.items);
    info!(
        imported = summary.imported_count,
        updated = summary.updated_count,
        total = summary.total_items_in_store,
        "TSM import completed"
    );
    (StatusCode::OK, Json(serde_json::to_value(summary).unwrap()))
}

// ---------------------------------------------------------------------------
// Arbitrage scan
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct ScanParams {
    threshold: Option<f64>,
    min_profit: Option<f64>,
}

fn run_arbitrage_scan(
    items: &DashMap<String, ItemData>,
    threshold: f64,
    min_profit: f64,
) -> Vec<ArbitrageOpportunity> {
    let mut opportunities: Vec<ArbitrageOpportunity> = Vec::new();

    for entry in items.iter() {
        let item = entry.value();

        if item.min_buyout <= 0.0 || item.market_value <= 0.0 {
            continue;
        }

        let threshold_price = item.market_value * threshold;
        if item.min_buyout < threshold_price {
            let profit_per_unit = item.market_value - item.min_buyout;
            if profit_per_unit < min_profit {
                continue;
            }
            let profit_margin_pct = (profit_per_unit / item.min_buyout) * 100.0;
            let total_potential_profit = profit_per_unit * item.quantity as f64;

            opportunities.push(ArbitrageOpportunity {
                item_id: item.item_id.clone(),
                name: item.name.clone(),
                min_buyout: item.min_buyout,
                market_value: item.market_value,
                profit_per_unit,
                profit_margin_pct,
                available_quantity: item.quantity,
                total_potential_profit,
            });
        }
    }

    // Sort by total potential profit descending
    opportunities.sort_by(|a, b| {
        b.total_potential_profit
            .partial_cmp(&a.total_potential_profit)
            .unwrap_or(std::cmp::Ordering::Equal)
    });

    opportunities
}

async fn scan_endpoint(
    State(state): State<AppState>,
    Query(params): Query<ScanParams>,
) -> impl IntoResponse {
    let threshold = params.threshold.unwrap_or(0.8); // items below 80% of market value
    let min_profit = params.min_profit.unwrap_or(100.0); // minimum 100g profit

    if state.items.is_empty() {
        let body = serde_json::json!({
            "error": "No item data loaded. Import TSM data first via POST /import.",
        });
        return (StatusCode::BAD_REQUEST, Json(body)).into_response();
    }

    let opportunities = run_arbitrage_scan(&state.items, threshold, min_profit);

    let result = serde_json::json!({
        "scan_time": Utc::now().to_rfc3339(),
        "threshold": threshold,
        "min_profit": min_profit,
        "total_items_scanned": state.items.len(),
        "opportunities_found": opportunities.len(),
        "opportunities": opportunities,
    });

    // Store scan in history
    {
        let mut history = state.scan_history.lock().await;
        history.push(result.clone());
        // Keep last 50 scans
        if history.len() > 50 {
            let drain_count = history.len() - 50;
            history.drain(..drain_count);
        }
    }

    info!(
        opportunities = opportunities.len(),
        threshold = threshold,
        "arbitrage scan completed"
    );

    (StatusCode::OK, Json(result)).into_response()
}

// ---------------------------------------------------------------------------
// Crafting profit check
// ---------------------------------------------------------------------------

fn check_crafting_profit(
    items: &DashMap<String, ItemData>,
    recipe: &CraftingRecipe,
) -> Result<CraftingAnalysis> {
    let craft_quantity = recipe.result_quantity.unwrap_or(1);

    // Look up result item price
    let result_item = items
        .get(&recipe.result_item_id)
        .map(|e| e.value().clone());

    let result_market_value = match &result_item {
        Some(item) => item.market_value * craft_quantity as f64,
        None => {
            anyhow::bail!(
                "Result item '{}' not found in price data. Import TSM data first.",
                recipe.result_item_id
            );
        }
    };

    let result_name = result_item
        .as_ref()
        .map(|i| i.name.clone())
        .or_else(|| recipe.result_item_name.clone())
        .unwrap_or_else(|| recipe.result_item_id.clone());

    // Calculate reagent costs
    let mut total_reagent_cost = 0.0f64;
    let mut reagent_breakdown: Vec<ReagentCost> = Vec::new();

    for reagent in &recipe.reagents {
        let reagent_data = items.get(&reagent.item_id).map(|e| e.value().clone());

        let (unit_price, price_source, name) = match &reagent_data {
            Some(item) => {
                // Use min_buyout as the buy price (what you'd pay on AH)
                let price = if item.min_buyout > 0.0 {
                    item.min_buyout
                } else {
                    item.market_value
                };
                let source = if item.min_buyout > 0.0 {
                    "min_buyout"
                } else {
                    "market_value"
                };
                (price, source.to_string(), item.name.clone())
            }
            None => {
                anyhow::bail!(
                    "Reagent '{}' not found in price data. Import TSM data first.",
                    reagent.item_id
                );
            }
        };

        let total_cost = unit_price * reagent.quantity as f64;
        total_reagent_cost += total_cost;

        reagent_breakdown.push(ReagentCost {
            item_id: reagent.item_id.clone(),
            name,
            quantity_needed: reagent.quantity,
            unit_price,
            total_cost,
            price_source,
        });
    }

    let profit_per_craft = result_market_value - total_reagent_cost;
    let profit_margin_pct = if total_reagent_cost > 0.0 {
        (profit_per_craft / total_reagent_cost) * 100.0
    } else {
        0.0
    };

    let verdict = if profit_per_craft > 0.0 {
        if profit_margin_pct > 50.0 {
            "HIGHLY PROFITABLE - Strong margins, craft aggressively".to_string()
        } else if profit_margin_pct > 20.0 {
            "PROFITABLE - Good margins, worth crafting".to_string()
        } else if profit_margin_pct > 5.0 {
            "MARGINALLY PROFITABLE - Thin margins, craft cautiously".to_string()
        } else {
            "BREAK-EVEN - Margins too thin after AH cut, not recommended".to_string()
        }
    } else {
        format!(
            "UNPROFITABLE - Crafting costs {:.1}g more than market value",
            -profit_per_craft
        )
    };

    Ok(CraftingAnalysis {
        result_item: result_name,
        result_market_value,
        craft_quantity,
        total_reagent_cost,
        profit_per_craft,
        profit_margin_pct,
        reagent_breakdown,
        verdict,
    })
}

async fn craft_check_endpoint(
    State(state): State<AppState>,
    Json(recipe): Json<CraftingRecipe>,
) -> impl IntoResponse {
    match check_crafting_profit(&state.items, &recipe) {
        Ok(analysis) => {
            (StatusCode::OK, Json(serde_json::to_value(analysis).unwrap())).into_response()
        }
        Err(e) => {
            let body = serde_json::json!({ "error": format!("{:#}", e) });
            (StatusCode::BAD_REQUEST, Json(body)).into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// Market trend analysis (LLM-powered)
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct TrendRequest {
    #[serde(default)]
    item_id: Option<String>,
    #[serde(default)]
    item_name: Option<String>,
}

async fn analyze_trend(agent: &OpenClawAgent, items: &DashMap<String, ItemData>, req: &TrendRequest, soul: &str) -> Result<serde_json::Value> {
    // Find the item by ID or by name (case-insensitive partial match)
    let item = if let Some(id) = &req.item_id {
        items.get(id).map(|e| e.value().clone())
    } else if let Some(name) = &req.item_name {
        let lower = name.to_lowercase();
        items
            .iter()
            .find(|entry| entry.value().name.to_lowercase().contains(&lower))
            .map(|entry| entry.value().clone())
    } else {
        anyhow::bail!("Must provide either 'item_id' or 'item_name'");
    };

    let item = item.context("Item not found in price data. Import TSM data first.")?;

    // Calculate derived metrics
    let price_vs_historical = if item.historical_price > 0.0 {
        ((item.market_value - item.historical_price) / item.historical_price) * 100.0
    } else {
        0.0
    };

    let buyout_vs_market = if item.market_value > 0.0 {
        ((item.min_buyout - item.market_value) / item.market_value) * 100.0
    } else {
        0.0
    };

    // Gather similar items for context (same price range, +/- 50%)
    let price_low = item.market_value * 0.5;
    let price_high = item.market_value * 1.5;
    let similar_items: Vec<String> = items
        .iter()
        .filter(|e| {
            let v = e.value();
            v.item_id != item.item_id
                && v.market_value >= price_low
                && v.market_value <= price_high
        })
        .take(10)
        .map(|e| {
            let v = e.value();
            format!(
                "  - {} (ID: {}): market={:.1}g, min_buyout={:.1}g, qty={}",
                v.name, v.item_id, v.market_value, v.min_buyout, v.quantity
            )
        })
        .collect();

    let similar_context = if similar_items.is_empty() {
        "No similar-priced items found in current data.".to_string()
    } else {
        format!(
            "Similar-priced items in current snapshot:\n{}",
            similar_items.join("\n")
        )
    };

    let prompt = format!(
        r#"You are a World of Warcraft auction house economy analyst. Analyze the following item's market data and provide a trading recommendation.

Item: {} (ID: {})
Current Market Value: {:.2}g
Current Min Buyout: {:.2}g
Available Quantity: {}
Historical Price: {:.2}g
Price vs Historical: {:.1}% ({})
Min Buyout vs Market Value: {:.1}% ({})

{}

Provide your analysis as JSON with these fields:
- "trend": one of "bullish", "bearish", "stable", "volatile"
- "recommendation": one of "STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"
- "confidence": a number 1-10
- "reasoning": 2-3 sentence explanation of your recommendation
- "risk_factors": array of 1-3 risk factors to consider
- "price_target": estimated fair value in gold (number)

Respond ONLY with the JSON object, no other text."#,
        item.name,
        item.item_id,
        item.market_value,
        item.min_buyout,
        item.quantity,
        item.historical_price,
        price_vs_historical.abs(),
        if price_vs_historical >= 0.0 { "above" } else { "below" },
        buyout_vs_market.abs(),
        if buyout_vs_market >= 0.0 { "above" } else { "below" },
        similar_context,
    );

    let messages = vec![
        openclaw_sdk::ChatMessage { role: "system".into(), content: soul.to_string() },
        openclaw_sdk::ChatMessage { role: "user".into(), content: prompt },
    ];
    let llm_response = agent
        .groq()
        .chat(messages, Some(openclaw_sdk::GroqModel::Fast), Some(1024), Some(0.3), true)
        .await;

    let analysis = match llm_response {
        Ok(resp) => {
            // Try to parse as JSON; fall back to raw text
            match serde_json::from_str::<serde_json::Value>(&resp.text) {
                Ok(parsed) => parsed,
                Err(_) => {
                    warn!("LLM returned non-JSON, wrapping as raw analysis");
                    serde_json::json!({ "raw_analysis": resp.text })
                }
            }
        }
        Err(e) => {
            warn!(error = %e, "LLM trend analysis failed, using heuristic fallback");
            // Heuristic fallback
            let (trend, recommendation) = if price_vs_historical < -20.0 {
                ("bearish", "BUY")
            } else if price_vs_historical > 20.0 {
                ("bullish", "SELL")
            } else if buyout_vs_market < -15.0 {
                ("volatile", "BUY")
            } else {
                ("stable", "HOLD")
            };

            serde_json::json!({
                "trend": trend,
                "recommendation": recommendation,
                "confidence": 4,
                "reasoning": format!(
                    "Heuristic analysis (LLM unavailable): Price is {:.1}% {} historical average. \
                     Min buyout is {:.1}% {} market value. {} units available.",
                    price_vs_historical.abs(),
                    if price_vs_historical >= 0.0 { "above" } else { "below" },
                    buyout_vs_market.abs(),
                    if buyout_vs_market >= 0.0 { "above" } else { "below" },
                    item.quantity
                ),
                "risk_factors": [
                    "Analysis based on heuristics only — LLM was unavailable",
                    "Single snapshot data — no time-series trend available"
                ],
                "price_target": item.historical_price,
            })
        }
    };

    Ok(serde_json::json!({
        "item": {
            "item_id": item.item_id,
            "name": item.name,
            "market_value": item.market_value,
            "min_buyout": item.min_buyout,
            "quantity": item.quantity,
            "historical_price": item.historical_price,
        },
        "analysis": analysis,
        "analyzed_at": Utc::now().to_rfc3339(),
    }))
}

async fn trend_endpoint(
    State(state): State<AppState>,
    Json(req): Json<TrendRequest>,
) -> impl IntoResponse {
    match analyze_trend(&state.agent, &state.items, &req, &state.soul).await {
        Ok(result) => (StatusCode::OK, Json(result)).into_response(),
        Err(e) => {
            let body = serde_json::json!({ "error": format!("{:#}", e) });
            (StatusCode::BAD_REQUEST, Json(body)).into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// Items list endpoint
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct ItemsParams {
    #[serde(default)]
    search: Option<String>,
    #[serde(default)]
    sort_by: Option<String>,
    #[serde(default)]
    limit: Option<usize>,
}

async fn items_endpoint(
    State(state): State<AppState>,
    Query(params): Query<ItemsParams>,
) -> impl IntoResponse {
    let limit = params.limit.unwrap_or(100);

    let mut items_list: Vec<ItemData> = state
        .items
        .iter()
        .filter(|entry| {
            if let Some(search) = &params.search {
                let lower = search.to_lowercase();
                entry.value().name.to_lowercase().contains(&lower)
                    || entry.value().item_id.to_lowercase().contains(&lower)
            } else {
                true
            }
        })
        .map(|entry| entry.value().clone())
        .collect();

    // Sort
    match params.sort_by.as_deref() {
        Some("name") => items_list.sort_by(|a, b| a.name.cmp(&b.name)),
        Some("min_buyout") => items_list.sort_by(|a, b| {
            a.min_buyout
                .partial_cmp(&b.min_buyout)
                .unwrap_or(std::cmp::Ordering::Equal)
        }),
        Some("quantity") => items_list.sort_by(|a, b| b.quantity.cmp(&a.quantity)),
        _ => {
            // Default: sort by market_value descending
            items_list.sort_by(|a, b| {
                b.market_value
                    .partial_cmp(&a.market_value)
                    .unwrap_or(std::cmp::Ordering::Equal)
            });
        }
    }

    items_list.truncate(limit);

    let body = serde_json::json!({
        "total_items": state.items.len(),
        "returned": items_list.len(),
        "items": items_list,
    });

    (StatusCode::OK, Json(body))
}

// ---------------------------------------------------------------------------
// TaskHandler implementation
// ---------------------------------------------------------------------------

struct WowEconomyHandler {
    items: Arc<DashMap<String, ItemData>>,
    scan_history: Arc<Mutex<Vec<serde_json::Value>>>,
    soul: Arc<String>,
}

#[async_trait::async_trait]
impl TaskHandler for WowEconomyHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "tsm_import" => {
                let incoming: Vec<ItemData> = serde_json::from_value(
                    task.payload
                        .get("items")
                        .cloned()
                        .context("tsm_import payload missing 'items' array")?,
                )
                .context("failed to parse items array")?;

                let summary = do_import(&self.items, incoming);
                serde_json::to_value(summary).context("failed to serialize import summary")
            }

            "arbitrage_scan" => {
                let threshold = task
                    .payload
                    .get("threshold")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(0.8);
                let min_profit = task
                    .payload
                    .get("min_profit")
                    .and_then(|v| v.as_f64())
                    .unwrap_or(100.0);

                if self.items.is_empty() {
                    anyhow::bail!("No item data loaded. Submit a tsm_import task first.");
                }

                let opportunities = run_arbitrage_scan(&self.items, threshold, min_profit);

                let result = serde_json::json!({
                    "scan_time": Utc::now().to_rfc3339(),
                    "threshold": threshold,
                    "min_profit": min_profit,
                    "total_items_scanned": self.items.len(),
                    "opportunities_found": opportunities.len(),
                    "opportunities": opportunities,
                });

                {
                    let mut history = self.scan_history.lock().await;
                    history.push(result.clone());
                    if history.len() > 50 {
                        let drain_count = history.len() - 50;
                        history.drain(..drain_count);
                    }
                }

                Ok(result)
            }

            "crafting_profit" => {
                let recipe: CraftingRecipe = serde_json::from_value(task.payload.clone())
                    .context("failed to parse crafting recipe from payload")?;
                let analysis = check_crafting_profit(&self.items, &recipe)?;
                serde_json::to_value(analysis).context("failed to serialize crafting analysis")
            }

            "market_trend" => {
                let req = TrendRequest {
                    item_id: task
                        .payload
                        .get("item_id")
                        .and_then(|v| v.as_str())
                        .map(|s| s.to_string()),
                    item_name: task
                        .payload
                        .get("item_name")
                        .and_then(|v| v.as_str())
                        .map(|s| s.to_string()),
                };
                analyze_trend(agent, &self.items, &req, &self.soul).await
            }

            other => {
                anyhow::bail!("unsupported task_type: {}", other);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config.clone());

    let soul = Arc::new(
        openclaw_sdk::load_soul(&config.agent_id)
            .unwrap_or_else(|| "You are a World of Warcraft economy analyst.".to_string()),
    );

    let items: Arc<DashMap<String, ItemData>> = Arc::new(DashMap::new());
    let scan_history: Arc<Mutex<Vec<serde_json::Value>>> = Arc::new(Mutex::new(Vec::new()));

    let handler = WowEconomyHandler {
        items: items.clone(),
        scan_history: scan_history.clone(),
        soul: soul.clone(),
    };

    let state = AppState {
        agent: Arc::new(agent.clone()),
        items,
        scan_history,
        soul,
    };

    let routes = Router::new()
        .route("/import", post(import_endpoint))
        .route("/scan", get(scan_endpoint))
        .route("/craft-check", post(craft_check_endpoint))
        .route("/trend", post(trend_endpoint))
        .route("/items", get(items_endpoint))
        .with_state(state);

    agent.run(handler, routes).await
}
