use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::Utc;
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;
use tracing::{error, info};

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ClientInfo {
    client_id: String,
    name: String,
    domain: String,
    services: Vec<String>,
    contact_email: String,
    #[serde(default)]
    notes: Option<String>,
    #[serde(default = "now_rfc3339")]
    created_at: String,
}

fn now_rfc3339() -> String {
    Utc::now().to_rfc3339()
}

#[derive(Debug, Deserialize)]
struct RegisterClientRequest {
    client_id: String,
    name: String,
    domain: String,
    #[serde(default)]
    services: Vec<String>,
    contact_email: String,
    #[serde(default)]
    notes: Option<String>,
}

#[derive(Debug, Deserialize)]
struct WeeklyReportRequest {
    client_id: String,
    #[serde(default)]
    period_start: Option<String>,
    #[serde(default = "default_true")]
    include_seo: bool,
    #[serde(default = "default_true")]
    include_content: bool,
    #[serde(default = "default_true")]
    include_recommendations: bool,
}

fn default_true() -> bool {
    true
}

#[derive(Debug, Deserialize)]
struct MonthlyReportRequest {
    client_id: String,
    #[serde(default)]
    month: Option<String>,
}

#[derive(Debug, Deserialize)]
struct SeoTrackRequest {
    client_id: String,
    url: String,
    #[serde(default)]
    keywords: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct ReportQuery {
    #[serde(default)]
    client_id: Option<String>,
}

// ---------------------------------------------------------------------------
// Shared application state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: Arc<OpenClawAgent>,
    clients: Arc<DashMap<String, ClientInfo>>,
    reports: Arc<Mutex<Vec<serde_json::Value>>>,
}

// ---------------------------------------------------------------------------
// Report generation helpers
// ---------------------------------------------------------------------------

async fn generate_weekly_report(
    agent: &OpenClawAgent,
    client: &ClientInfo,
    period_start: Option<&str>,
    include_seo: bool,
    include_content: bool,
    include_recommendations: bool,
) -> Result<serde_json::Value> {
    let period = period_start.unwrap_or("last 7 days");

    let mut sections = Vec::new();
    if include_seo {
        sections.push("- SEO performance metrics and ranking changes");
    }
    if include_content {
        sections.push("- Content performance and engagement metrics");
    }
    if include_recommendations {
        sections.push("- Actionable recommendations for the coming week");
    }
    let sections_text = if sections.is_empty() {
        "- General performance overview".to_string()
    } else {
        sections.join("\n")
    };

    let prompt = format!(
        r#"Generate a professional weekly digital marketing report for the following client.

Client: {name}
Domain: {domain}
Services: {services}
Report Period: {period}

Include the following sections:
{sections}

Structure the report with:
1. Executive Summary (2-3 sentences)
2. Key Performance Indicators (use realistic placeholder data)
3. Detailed section for each requested area
4. Summary and Next Steps

Write in a professional consulting tone. Use specific numbers and percentages where appropriate (generate realistic sample data).
Format as a clean text report suitable for email delivery."#,
        name = client.name,
        domain = client.domain,
        services = client.services.join(", "),
        period = period,
        sections = sections_text,
    );

    let response = agent
        .llm
        .complete(
            &prompt,
            Some("heavy"),
            Some("You are a digital marketing consultant writing client reports."),
            Some(4096),
            Some(0.4),
            false,
        )
        .await
        .context("LLM weekly report generation failed")?;

    let report = serde_json::json!({
        "type": "weekly",
        "client_id": client.client_id,
        "client_name": client.name,
        "domain": client.domain,
        "period_start": period,
        "include_seo": include_seo,
        "include_content": include_content,
        "include_recommendations": include_recommendations,
        "report_text": response.text,
        "tokens_used": response.tokens_used,
        "model": response.model,
        "generated_at": Utc::now().to_rfc3339(),
    });

    Ok(report)
}

async fn generate_monthly_report(
    agent: &OpenClawAgent,
    client: &ClientInfo,
    month: Option<&str>,
) -> Result<serde_json::Value> {
    let month_label = month.unwrap_or("current month");

    let prompt = format!(
        r#"Generate a comprehensive monthly digital marketing report for the following client.

Client: {name}
Domain: {domain}
Services: {services}
Report Month: {month}

Structure the report with:

1. Executive Summary (3-4 sentences covering overall performance)

2. KPI Dashboard Table:
   | Metric | This Month | Last Month | Change |
   Include: organic traffic, keyword rankings, bounce rate, conversion rate, page speed score, backlinks acquired.

3. SEO Performance Deep Dive
   - Ranking changes for target keywords
   - New pages indexed
   - Technical SEO issues resolved

4. Content Performance
   - Top performing content pieces
   - Content published this month
   - Engagement metrics

5. ROI Analysis
   - Investment vs. returns
   - Cost per acquisition trends
   - Revenue attribution

6. Invoice Summary
   - Services rendered
   - Hours/deliverables
   - Total amount

7. Recommendations for Next Month
   - Priority actions
   - Strategic opportunities
   - Risk areas to monitor

Write in a professional consulting tone. Use specific numbers and percentages (generate realistic sample data).
Format as a polished report suitable for C-level review."#,
        name = client.name,
        domain = client.domain,
        services = client.services.join(", "),
        month = month_label,
    );

    let response = agent
        .llm
        .complete(
            &prompt,
            Some("heavy"),
            Some("You are a digital marketing consultant writing client reports."),
            Some(6144),
            Some(0.4),
            false,
        )
        .await
        .context("LLM monthly report generation failed")?;

    let report = serde_json::json!({
        "type": "monthly",
        "client_id": client.client_id,
        "client_name": client.name,
        "domain": client.domain,
        "month": month_label,
        "report_text": response.text,
        "tokens_used": response.tokens_used,
        "model": response.model,
        "generated_at": Utc::now().to_rfc3339(),
    });

    Ok(report)
}

fn build_client_health(
    client: &ClientInfo,
    reports: &[serde_json::Value],
) -> serde_json::Value {
    let client_reports: Vec<&serde_json::Value> = reports
        .iter()
        .filter(|r| r.get("client_id").and_then(|v| v.as_str()) == Some(&client.client_id))
        .collect();

    let weekly_count = client_reports
        .iter()
        .filter(|r| r.get("type").and_then(|v| v.as_str()) == Some("weekly"))
        .count();
    let monthly_count = client_reports
        .iter()
        .filter(|r| r.get("type").and_then(|v| v.as_str()) == Some("monthly"))
        .count();

    let last_report_date = client_reports
        .iter()
        .filter_map(|r| r.get("generated_at").and_then(|v| v.as_str()))
        .max()
        .map(|s| s.to_string());

    serde_json::json!({
        "client_id": client.client_id,
        "name": client.name,
        "domain": client.domain,
        "services": client.services,
        "contact_email": client.contact_email,
        "total_reports": client_reports.len(),
        "weekly_reports": weekly_count,
        "monthly_reports": monthly_count,
        "last_report_date": last_report_date,
        "status": if client_reports.is_empty() { "new" } else { "active" },
    })
}

async fn run_seo_tracking(
    client: &ClientInfo,
    url: &str,
    keywords: &[String],
) -> Result<serde_json::Value> {
    let http = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(60))
        .build()
        .context("failed to build HTTP client for SEO tracking")?;

    let audit_body = serde_json::json!({ "url": url });

    let resp = http
        .post("http://openclaw-seo-auditor:8001/audit")
        .json(&audit_body)
        .send()
        .await
        .context("SEO auditor request failed")?;

    let status = resp.status();
    if !status.is_success() {
        let text = resp.text().await.unwrap_or_default();
        anyhow::bail!("SEO auditor returned {}: {}", status, text);
    }

    let audit_result: serde_json::Value = resp
        .json()
        .await
        .context("failed to parse SEO auditor response")?;

    let tracking = serde_json::json!({
        "client_id": client.client_id,
        "client_name": client.name,
        "url": url,
        "keywords": keywords,
        "audit": audit_result,
        "tracked_at": Utc::now().to_rfc3339(),
    });

    Ok(tracking)
}

// ---------------------------------------------------------------------------
// TaskHandler
// ---------------------------------------------------------------------------

struct DashboardHandler;

#[async_trait::async_trait]
impl TaskHandler for DashboardHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "weekly_report" => {
                let client_id = task
                    .payload
                    .get("client_id")
                    .and_then(|v| v.as_str())
                    .context("task payload missing 'client_id'")?;
                let period_start = task
                    .payload
                    .get("period_start")
                    .and_then(|v| v.as_str());
                let include_seo = task
                    .payload
                    .get("include_seo")
                    .and_then(|v| v.as_bool())
                    .unwrap_or(true);
                let include_content = task
                    .payload
                    .get("include_content")
                    .and_then(|v| v.as_bool())
                    .unwrap_or(true);
                let include_recommendations = task
                    .payload
                    .get("include_recommendations")
                    .and_then(|v| v.as_bool())
                    .unwrap_or(true);

                // Build a minimal ClientInfo from task payload if no registered client
                let client = ClientInfo {
                    client_id: client_id.to_string(),
                    name: task
                        .payload
                        .get("client_name")
                        .and_then(|v| v.as_str())
                        .unwrap_or(client_id)
                        .to_string(),
                    domain: task
                        .payload
                        .get("domain")
                        .and_then(|v| v.as_str())
                        .unwrap_or("unknown")
                        .to_string(),
                    services: task
                        .payload
                        .get("services")
                        .and_then(|v| v.as_array())
                        .map(|arr| {
                            arr.iter()
                                .filter_map(|s| s.as_str().map(|s| s.to_string()))
                                .collect()
                        })
                        .unwrap_or_default(),
                    contact_email: task
                        .payload
                        .get("contact_email")
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string(),
                    notes: None,
                    created_at: now_rfc3339(),
                };

                let report = generate_weekly_report(
                    agent,
                    &client,
                    period_start,
                    include_seo,
                    include_content,
                    include_recommendations,
                )
                .await?;

                Ok(report)
            }

            "monthly_report" => {
                let client_id = task
                    .payload
                    .get("client_id")
                    .and_then(|v| v.as_str())
                    .context("task payload missing 'client_id'")?;
                let month = task.payload.get("month").and_then(|v| v.as_str());

                let client = ClientInfo {
                    client_id: client_id.to_string(),
                    name: task
                        .payload
                        .get("client_name")
                        .and_then(|v| v.as_str())
                        .unwrap_or(client_id)
                        .to_string(),
                    domain: task
                        .payload
                        .get("domain")
                        .and_then(|v| v.as_str())
                        .unwrap_or("unknown")
                        .to_string(),
                    services: task
                        .payload
                        .get("services")
                        .and_then(|v| v.as_array())
                        .map(|arr| {
                            arr.iter()
                                .filter_map(|s| s.as_str().map(|s| s.to_string()))
                                .collect()
                        })
                        .unwrap_or_default(),
                    contact_email: task
                        .payload
                        .get("contact_email")
                        .and_then(|v| v.as_str())
                        .unwrap_or("")
                        .to_string(),
                    notes: None,
                    created_at: now_rfc3339(),
                };

                let report = generate_monthly_report(agent, &client, month).await?;
                Ok(report)
            }

            "client_health" => {
                let client_id = task
                    .payload
                    .get("client_id")
                    .and_then(|v| v.as_str())
                    .unwrap_or("");

                // For task-based health checks, return a simple status since we
                // don't have access to the in-memory stores from here.
                Ok(serde_json::json!({
                    "client_id": client_id,
                    "status": "healthy",
                    "note": "Use the /health-check API endpoint for full client health data",
                    "checked_at": Utc::now().to_rfc3339(),
                }))
            }

            "seo_tracking" => {
                let client_id = task
                    .payload
                    .get("client_id")
                    .and_then(|v| v.as_str())
                    .context("task payload missing 'client_id'")?;
                let url = task
                    .payload
                    .get("url")
                    .and_then(|v| v.as_str())
                    .context("task payload missing 'url'")?;
                let keywords: Vec<String> = task
                    .payload
                    .get("keywords")
                    .and_then(|v| v.as_array())
                    .map(|arr| {
                        arr.iter()
                            .filter_map(|s| s.as_str().map(|s| s.to_string()))
                            .collect()
                    })
                    .unwrap_or_default();

                let client = ClientInfo {
                    client_id: client_id.to_string(),
                    name: task
                        .payload
                        .get("client_name")
                        .and_then(|v| v.as_str())
                        .unwrap_or(client_id)
                        .to_string(),
                    domain: task
                        .payload
                        .get("domain")
                        .and_then(|v| v.as_str())
                        .unwrap_or("unknown")
                        .to_string(),
                    services: Vec::new(),
                    contact_email: String::new(),
                    notes: None,
                    created_at: now_rfc3339(),
                };

                let result = run_seo_tracking(&client, url, &keywords).await?;
                Ok(result)
            }

            other => {
                anyhow::bail!("unsupported task_type: {}", other);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Direct API endpoints
// ---------------------------------------------------------------------------

async fn register_client(
    State(state): State<AppState>,
    Json(req): Json<RegisterClientRequest>,
) -> impl IntoResponse {
    let client = ClientInfo {
        client_id: req.client_id.clone(),
        name: req.name,
        domain: req.domain,
        services: req.services,
        contact_email: req.contact_email,
        notes: req.notes,
        created_at: now_rfc3339(),
    };

    info!(client_id = %client.client_id, "registering client");
    state.clients.insert(req.client_id.clone(), client.clone());

    (
        StatusCode::CREATED,
        Json(serde_json::json!({
            "status": "registered",
            "client": client,
        })),
    )
        .into_response()
}

async fn list_clients(State(state): State<AppState>) -> impl IntoResponse {
    let clients: Vec<ClientInfo> = state
        .clients
        .iter()
        .map(|entry| entry.value().clone())
        .collect();

    Json(serde_json::json!({
        "count": clients.len(),
        "clients": clients,
    }))
}

async fn get_client(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> impl IntoResponse {
    match state.clients.get(&id) {
        Some(client) => (StatusCode::OK, Json(serde_json::to_value(client.value()).unwrap()))
            .into_response(),
        None => (
            StatusCode::NOT_FOUND,
            Json(serde_json::json!({ "error": format!("client '{}' not found", id) })),
        )
            .into_response(),
    }
}

async fn weekly_report_endpoint(
    State(state): State<AppState>,
    Json(req): Json<WeeklyReportRequest>,
) -> impl IntoResponse {
    let client = match state.clients.get(&req.client_id) {
        Some(c) => c.value().clone(),
        None => {
            return (
                StatusCode::NOT_FOUND,
                Json(serde_json::json!({
                    "error": format!("client '{}' not found, register first via POST /clients", req.client_id)
                })),
            )
                .into_response();
        }
    };

    match generate_weekly_report(
        &state.agent,
        &client,
        req.period_start.as_deref(),
        req.include_seo,
        req.include_content,
        req.include_recommendations,
    )
    .await
    {
        Ok(report) => {
            let mut reports = state.reports.lock().await;
            reports.push(report.clone());
            info!(client_id = %req.client_id, "weekly report generated");
            (StatusCode::OK, Json(report)).into_response()
        }
        Err(e) => {
            error!(error = %e, "weekly report generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn monthly_report_endpoint(
    State(state): State<AppState>,
    Json(req): Json<MonthlyReportRequest>,
) -> impl IntoResponse {
    let client = match state.clients.get(&req.client_id) {
        Some(c) => c.value().clone(),
        None => {
            return (
                StatusCode::NOT_FOUND,
                Json(serde_json::json!({
                    "error": format!("client '{}' not found, register first via POST /clients", req.client_id)
                })),
            )
                .into_response();
        }
    };

    match generate_monthly_report(&state.agent, &client, req.month.as_deref()).await {
        Ok(report) => {
            let mut reports = state.reports.lock().await;
            reports.push(report.clone());
            info!(client_id = %req.client_id, "monthly report generated");
            (StatusCode::OK, Json(report)).into_response()
        }
        Err(e) => {
            error!(error = %e, "monthly report generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn list_reports(
    State(state): State<AppState>,
    Query(query): Query<ReportQuery>,
) -> impl IntoResponse {
    let reports = state.reports.lock().await;

    let filtered: Vec<&serde_json::Value> = match &query.client_id {
        Some(cid) => reports
            .iter()
            .filter(|r| r.get("client_id").and_then(|v| v.as_str()) == Some(cid.as_str()))
            .collect(),
        None => reports.iter().collect(),
    };

    Json(serde_json::json!({
        "count": filtered.len(),
        "reports": filtered,
    }))
}

async fn health_check_endpoint(State(state): State<AppState>) -> impl IntoResponse {
    let reports = state.reports.lock().await;

    let overview: Vec<serde_json::Value> = state
        .clients
        .iter()
        .map(|entry| build_client_health(entry.value(), &reports))
        .collect();

    Json(serde_json::json!({
        "total_clients": overview.len(),
        "clients": overview,
        "checked_at": Utc::now().to_rfc3339(),
    }))
}

async fn seo_track_endpoint(
    State(state): State<AppState>,
    Json(req): Json<SeoTrackRequest>,
) -> impl IntoResponse {
    let client = match state.clients.get(&req.client_id) {
        Some(c) => c.value().clone(),
        None => {
            return (
                StatusCode::NOT_FOUND,
                Json(serde_json::json!({
                    "error": format!("client '{}' not found, register first via POST /clients", req.client_id)
                })),
            )
                .into_response();
        }
    };

    match run_seo_tracking(&client, &req.url, &req.keywords).await {
        Ok(result) => {
            info!(client_id = %req.client_id, url = %req.url, "SEO tracking completed");
            (StatusCode::OK, Json(result)).into_response()
        }
        Err(e) => {
            error!(error = %e, "SEO tracking failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config);

    let app_state = AppState {
        agent: Arc::new(agent.clone()),
        clients: Arc::new(DashMap::new()),
        reports: Arc::new(Mutex::new(Vec::new())),
    };

    let routes = Router::new()
        .route("/clients", post(register_client).get(list_clients))
        .route("/clients/{id}", get(get_client))
        .route("/reports/weekly", post(weekly_report_endpoint))
        .route("/reports/monthly", post(monthly_report_endpoint))
        .route("/reports", get(list_reports))
        .route("/health-check", get(health_check_endpoint))
        .route("/seo-track", post(seo_track_endpoint))
        .with_state(app_state);

    agent.run(DashboardHandler, routes).await
}
