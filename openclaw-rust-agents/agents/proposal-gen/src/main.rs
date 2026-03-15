use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use tracing::info;

use openclaw_sdk::{AgentConfig, ChatMessage, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SYSTEM_PROMPT: &str = "\
You are a freelance consultant for Ridge Cell Repair LLC specializing in \
web dev, SEO, and phone/device repair. You write compelling, professional \
proposals and statements of work. Be specific, use concrete numbers, and \
demonstrate expertise.";

const PORTFOLIO_CONTEXT: &str = "\
Ridge Cell Repair LLC — Matt Gates
- Web development (React, Next.js, WordPress, full-stack)
- SEO consulting (technical audits, content strategy, local SEO)
- Phone & device repair (iPhone, Android, tablets, laptops)
- Content creation (blog posts, social media, email campaigns)
- 5+ years experience, 50+ completed projects";

// ---------------------------------------------------------------------------
// Pricing constants
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize)]
struct ServiceRate {
    category: &'static str,
    hourly_min: u32,
    hourly_max: u32,
    project_min: u32,
    project_max: u32,
}

const SERVICE_RATES: &[ServiceRate] = &[
    ServiceRate {
        category: "web_development",
        hourly_min: 75,
        hourly_max: 150,
        project_min: 2_000,
        project_max: 25_000,
    },
    ServiceRate {
        category: "seo_consulting",
        hourly_min: 60,
        hourly_max: 120,
        project_min: 1_000,
        project_max: 10_000,
    },
    ServiceRate {
        category: "device_repair",
        hourly_min: 50,
        hourly_max: 100,
        project_min: 50,
        project_max: 500,
    },
    ServiceRate {
        category: "content_creation",
        hourly_min: 40,
        hourly_max: 80,
        project_min: 500,
        project_max: 5_000,
    },
];

// ---------------------------------------------------------------------------
// Request / Response types
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct ProposalRequest {
    job_title: String,
    #[serde(alias = "job_desc")]
    job_text: String,
    budget_range: Option<String>,
}

#[derive(Debug, Serialize)]
struct ProposalResponse {
    job_title: String,
    conservative_proposal: String,
    aggressive_proposal: String,
    tokens_used: u32,
    model: String,
}

#[derive(Debug, Deserialize)]
struct SowRequest {
    client_name: String,
    project_scope: String,
    deliverables: Vec<String>,
}

#[derive(Debug, Serialize)]
struct SowResponse {
    client_name: String,
    sow_document: String,
    tokens_used: u32,
    model: String,
}

#[derive(Debug, Deserialize)]
struct PricingRequest {
    scope_description: String,
    complexity: Option<String>,
}

#[derive(Debug, Serialize)]
struct PricingResponse {
    scope_description: String,
    complexity: String,
    matches: Vec<PricingMatch>,
}

#[derive(Debug, Serialize)]
struct PricingMatch {
    category: String,
    estimated_hours_min: u32,
    estimated_hours_max: u32,
    hourly_rate_min: u32,
    hourly_rate_max: u32,
    project_range_min: u32,
    project_range_max: u32,
    recommended_price: u32,
}

#[derive(Debug, Serialize)]
struct PortfolioResponse {
    company: &'static str,
    owner: &'static str,
    services: Vec<&'static str>,
    experience_years: u32,
    completed_projects: u32,
    service_rates: &'static [ServiceRate],
}

// ---------------------------------------------------------------------------
// Shared application state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: OpenClawAgent,
}

// ---------------------------------------------------------------------------
// Task handler (Core API task polling)
// ---------------------------------------------------------------------------

struct ProposalTaskHandler;

#[async_trait::async_trait]
impl TaskHandler for ProposalTaskHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "upwork_proposal" => {
                let req: ProposalRequest =
                    serde_json::from_value(task.payload.clone()).context("invalid proposal payload")?;
                let result = generate_proposal(agent, req).await?;
                serde_json::to_value(result).context("serialize proposal result")
            }
            "consulting_sow" => {
                let req: SowRequest =
                    serde_json::from_value(task.payload.clone()).context("invalid SOW payload")?;
                let result = generate_sow(agent, req).await?;
                serde_json::to_value(result).context("serialize SOW result")
            }
            "pricing" => {
                let req: PricingRequest =
                    serde_json::from_value(task.payload.clone()).context("invalid pricing payload")?;
                let result = calculate_pricing(req);
                serde_json::to_value(result).context("serialize pricing result")
            }
            other => anyhow::bail!("unknown task type: {}", other),
        }
    }
}

// ---------------------------------------------------------------------------
// Core logic: proposal generation
// ---------------------------------------------------------------------------

async fn generate_proposal(agent: &OpenClawAgent, req: ProposalRequest) -> Result<ProposalResponse> {
    let budget_info = req
        .budget_range
        .as_deref()
        .map(|b| format!("\nClient budget range: {}", b))
        .unwrap_or_default();

    let prompt = format!(
        "Generate TWO proposal variants for the following Upwork job posting. \
         Separate them with the exact delimiter \"---VARIANT_SPLIT---\".\n\n\
         VARIANT 1 — CONSERVATIVE: Professional, measured tone. Focus on reliability, \
         proven track record, and risk mitigation. Quote at or slightly below budget.\n\n\
         VARIANT 2 — AGGRESSIVE: Bold, confident tone. Emphasize speed, innovation, and \
         exceeding expectations. Quote at premium positioning.\n\n\
         Job Title: {title}\n\
         Job Description: {desc}{budget}\n\n\
         Portfolio context:\n{portfolio}\n\n\
         Each variant should include:\n\
         1. Opening hook (2-3 sentences)\n\
         2. Relevant experience & portfolio highlights\n\
         3. Proposed approach & timeline\n\
         4. Pricing rationale\n\
         5. Call to action\n\n\
         Write both proposals now.",
        title = req.job_title,
        desc = req.job_text,
        budget = budget_info,
        portfolio = PORTFOLIO_CONTEXT,
    );

    let resp = agent
        .llm
        .complete(&prompt, Some("heavy"), Some(SYSTEM_PROMPT), Some(6144), Some(0.7), false)
        .await
        .context("LLM proposal generation failed")?;

    let (conservative, aggressive) = split_variants(&resp.text);

    Ok(ProposalResponse {
        job_title: req.job_title,
        conservative_proposal: conservative,
        aggressive_proposal: aggressive,
        tokens_used: resp.tokens_used,
        model: resp.model,
    })
}

fn split_variants(text: &str) -> (String, String) {
    if let Some(idx) = text.find("---VARIANT_SPLIT---") {
        let conservative = text[..idx].trim().to_string();
        let aggressive = text[idx + "---VARIANT_SPLIT---".len()..].trim().to_string();
        (conservative, aggressive)
    } else {
        // Fallback: try to split on common patterns
        let midpoint = text.len() / 2;
        // Look for a paragraph break near the midpoint
        let split_pos = text[midpoint.saturating_sub(200)..std::cmp::min(midpoint + 200, text.len())]
            .find("\n\n")
            .map(|p| p + midpoint.saturating_sub(200))
            .unwrap_or(midpoint);
        let conservative = text[..split_pos].trim().to_string();
        let aggressive = text[split_pos..].trim().to_string();
        (conservative, aggressive)
    }
}

// ---------------------------------------------------------------------------
// Core logic: SOW generation
// ---------------------------------------------------------------------------

async fn generate_sow(agent: &OpenClawAgent, req: SowRequest) -> Result<SowResponse> {
    let deliverables_list = req
        .deliverables
        .iter()
        .enumerate()
        .map(|(i, d)| format!("{}. {}", i + 1, d))
        .collect::<Vec<_>>()
        .join("\n");

    let prompt = format!(
        "Generate a professional Statement of Work (SOW) document for the following project.\n\n\
         Client: {client}\n\
         Project Scope: {scope}\n\
         Deliverables:\n{deliverables}\n\n\
         Portfolio context:\n{portfolio}\n\n\
         The SOW must include ALL of the following sections:\n\n\
         1. PROJECT OVERVIEW — Executive summary of the engagement\n\
         2. SCOPE OF WORK — Detailed description of what is and is not included\n\
         3. DELIVERABLES TABLE — Markdown table with columns: #, Deliverable, Description, Estimated Timeline\n\
         4. TIMELINE — Phase-by-phase project schedule with milestones\n\
         5. PRICING — Itemized cost breakdown with total. Use rates appropriate for the scope.\n\
         6. TERMS & CONDITIONS — Payment schedule (50% upfront, 25% midpoint, 25% completion), \
            revision policy (2 rounds included), IP transfer upon final payment, \
            confidentiality clause, cancellation terms (30-day notice)\n\n\
         Format the document professionally with clear headings. \
         Use concrete timelines and realistic pricing based on the scope.",
        client = req.client_name,
        scope = req.project_scope,
        deliverables = deliverables_list,
        portfolio = PORTFOLIO_CONTEXT,
    );

    let resp = agent
        .llm
        .complete(&prompt, Some("heavy"), Some(SYSTEM_PROMPT), Some(8192), Some(0.5), false)
        .await
        .context("LLM SOW generation failed")?;

    Ok(SowResponse {
        client_name: req.client_name,
        sow_document: resp.text,
        tokens_used: resp.tokens_used,
        model: resp.model,
    })
}

// ---------------------------------------------------------------------------
// Core logic: pricing (pure calculation, no LLM)
// ---------------------------------------------------------------------------

fn calculate_pricing(req: PricingRequest) -> PricingResponse {
    let complexity = req.complexity.unwrap_or_else(|| "medium".to_string());
    let complexity_lower = complexity.to_lowercase();

    // Complexity multiplier for hours and price
    let (hours_mult, price_mult) = match complexity_lower.as_str() {
        "low" | "simple" => (0.6_f64, 0.7_f64),
        "high" | "complex" => (1.5, 1.3),
        "very_high" | "enterprise" => (2.0, 1.6),
        _ => (1.0, 1.0), // medium / default
    };

    let scope_lower = req.scope_description.to_lowercase();

    let matches: Vec<PricingMatch> = SERVICE_RATES
        .iter()
        .filter(|rate| {
            // Match service category keywords against the scope description
            let keywords: &[&str] = match rate.category {
                "web_development" => &[
                    "web", "website", "app", "application", "frontend", "backend",
                    "full-stack", "fullstack", "react", "next", "wordpress", "api",
                    "dashboard", "portal", "ecommerce", "e-commerce",
                ],
                "seo_consulting" => &[
                    "seo", "search engine", "ranking", "organic", "keyword",
                    "content strategy", "audit", "local seo", "google",
                    "traffic", "serp",
                ],
                "device_repair" => &[
                    "repair", "phone", "device", "iphone", "android", "tablet",
                    "laptop", "screen", "battery", "fix",
                ],
                "content_creation" => &[
                    "content", "blog", "article", "writing", "copywriting",
                    "social media", "email campaign", "newsletter", "copy",
                ],
                _ => &[],
            };
            keywords.iter().any(|kw| scope_lower.contains(kw))
        })
        .map(|rate| {
            // Base estimated hours derived from project range and hourly rate midpoint
            let hourly_mid = (rate.hourly_min + rate.hourly_max) / 2;
            let base_hours_min = rate.project_min / hourly_mid;
            let base_hours_max = rate.project_max / hourly_mid;

            let est_hours_min = ((base_hours_min as f64 * hours_mult).round() as u32).max(1);
            let est_hours_max = ((base_hours_max as f64 * hours_mult).round() as u32).max(est_hours_min);

            let adj_hourly_min = (rate.hourly_min as f64 * price_mult).round() as u32;
            let adj_hourly_max = (rate.hourly_max as f64 * price_mult).round() as u32;

            let project_min = (rate.project_min as f64 * hours_mult * price_mult).round() as u32;
            let project_max = (rate.project_max as f64 * hours_mult * price_mult).round() as u32;

            // Recommended: 60th-percentile point in the range
            let recommended = project_min + ((project_max - project_min) as f64 * 0.6).round() as u32;

            PricingMatch {
                category: rate.category.to_string(),
                estimated_hours_min: est_hours_min,
                estimated_hours_max: est_hours_max,
                hourly_rate_min: adj_hourly_min,
                hourly_rate_max: adj_hourly_max,
                project_range_min: project_min,
                project_range_max: project_max,
                recommended_price: recommended,
            }
        })
        .collect();

    // If no categories matched, return a generic web_development estimate
    let matches = if matches.is_empty() {
        let rate = &SERVICE_RATES[0]; // web_development as fallback
        let hourly_mid = (rate.hourly_min + rate.hourly_max) / 2;
        let base_hours_min = rate.project_min / hourly_mid;
        let base_hours_max = rate.project_max / hourly_mid;
        let est_hours_min = ((base_hours_min as f64 * hours_mult).round() as u32).max(1);
        let est_hours_max = ((base_hours_max as f64 * hours_mult).round() as u32).max(est_hours_min);
        let adj_hourly_min = (rate.hourly_min as f64 * price_mult).round() as u32;
        let adj_hourly_max = (rate.hourly_max as f64 * price_mult).round() as u32;
        let project_min = (rate.project_min as f64 * hours_mult * price_mult).round() as u32;
        let project_max = (rate.project_max as f64 * hours_mult * price_mult).round() as u32;
        let recommended = project_min + ((project_max - project_min) as f64 * 0.6).round() as u32;
        vec![PricingMatch {
            category: "web_development (default)".to_string(),
            estimated_hours_min: est_hours_min,
            estimated_hours_max: est_hours_max,
            hourly_rate_min: adj_hourly_min,
            hourly_rate_max: adj_hourly_max,
            project_range_min: project_min,
            project_range_max: project_max,
            recommended_price: recommended,
        }]
    } else {
        matches
    };

    PricingResponse {
        scope_description: req.scope_description,
        complexity: complexity_lower,
        matches,
    }
}

// ---------------------------------------------------------------------------
// Direct API HTTP handlers
// ---------------------------------------------------------------------------

async fn propose_handler(
    State(state): State<AppState>,
    Json(req): Json<ProposalRequest>,
) -> impl IntoResponse {
    match generate_proposal(&state.agent, req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({ "error": format!("{:#}", e) })),
        )
            .into_response(),
    }
}

async fn sow_handler(
    State(state): State<AppState>,
    Json(req): Json<SowRequest>,
) -> impl IntoResponse {
    match generate_sow(&state.agent, req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({ "error": format!("{:#}", e) })),
        )
            .into_response(),
    }
}

async fn price_handler(Json(req): Json<PricingRequest>) -> impl IntoResponse {
    let result = calculate_pricing(req);
    (StatusCode::OK, Json(serde_json::to_value(result).unwrap()))
}

async fn portfolio_handler() -> impl IntoResponse {
    let resp = PortfolioResponse {
        company: "Ridge Cell Repair LLC",
        owner: "Matt Gates",
        services: vec![
            "Web development (React, Next.js, WordPress, full-stack)",
            "SEO consulting (technical audits, content strategy, local SEO)",
            "Phone & device repair (iPhone, Android, tablets, laptops)",
            "Content creation (blog posts, social media, email campaigns)",
        ],
        experience_years: 5,
        completed_projects: 50,
        service_rates: SERVICE_RATES,
    };
    Json(serde_json::to_value(resp).unwrap())
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> Result<()> {
    // Override defaults for this agent
    if std::env::var("AGENT_ID").is_err() {
        std::env::set_var("AGENT_ID", "proposal-gen");
    }
    if std::env::var("AGENT_PORT").is_err() {
        std::env::set_var("AGENT_PORT", "8004");
    }
    if std::env::var("AGENT_CAPABILITIES").is_err() {
        std::env::set_var("AGENT_CAPABILITIES", "upwork_proposal,consulting_sow,pricing");
    }

    let config = AgentConfig::from_env().context("failed to load agent config")?;
    let agent = OpenClawAgent::new(config);

    let app_state = AppState {
        agent: agent.clone(),
    };

    let extra_routes = Router::new()
        .route("/propose", post(propose_handler))
        .route("/sow", post(sow_handler))
        .route("/price", post(price_handler))
        .route("/portfolio", get(portfolio_handler))
        .with_state(app_state);

    agent.run(ProposalTaskHandler, extra_routes).await
}
