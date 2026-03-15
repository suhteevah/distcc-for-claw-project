use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::Utc;
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use tracing::info;
use uuid::Uuid;

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Approval queue types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ApprovalEntry {
    id: String,
    #[serde(rename = "type")]
    entry_type: String,
    created_at: String,
    status: String,
    category: Option<String>,
    confidence: Option<f64>,
    draft: Option<String>,
    original_subject: Option<String>,
    original_from: Option<String>,
    job_title: Option<String>,
}

type ApprovalQueue = Arc<DashMap<String, serde_json::Value>>;

// ---------------------------------------------------------------------------
// Request / response types for direct API
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct ClassifyRequest {
    email_from: String,
    subject: String,
    body: String,
}

#[derive(Debug, Serialize)]
struct ClassifyResponse {
    category: String,
    confidence: f64,
    reasoning: String,
}

#[derive(Debug, Deserialize)]
struct DraftRequest {
    email_from: String,
    subject: String,
    body: String,
    #[serde(default = "default_tone")]
    tone: String,
}

fn default_tone() -> String {
    "professional".to_string()
}

#[derive(Debug, Serialize)]
struct DraftResponse {
    approval_id: String,
    category: String,
    confidence: f64,
    draft: String,
    status: String,
}

#[derive(Debug, Deserialize)]
struct UpworkRequest {
    job_title: String,
    job_description: String,
    #[serde(default)]
    relevant_experience: String,
    #[serde(default)]
    portfolio_highlights: String,
}

#[derive(Debug, Serialize)]
struct UpworkResponse {
    approval_id: String,
    draft: String,
    status: String,
}

// ---------------------------------------------------------------------------
// LLM interaction helpers
// ---------------------------------------------------------------------------

async fn classify_lead(
    agent: &OpenClawAgent,
    email_from: &str,
    subject: &str,
    body: &str,
) -> Result<ClassifyResponse> {
    let prompt = format!(
        r#"Classify the following email/message into exactly one category.

Categories:
- cold_inquiry: Unsolicited inquiry from a potential new client
- referral: Lead that mentions being referred by someone
- existing_client: Message from a known/existing client
- upwork_opportunity: Upwork job posting or related communication
- spam: Unsolicited marketing, scam, or irrelevant message
- newsletter: Newsletter, digest, or subscription-based email
- transactional: Automated notification, receipt, or system email

Email details:
From: {email_from}
Subject: {subject}
Body:
{body}

Respond with ONLY valid JSON in this exact format:
{{"category": "<one of the categories above>", "confidence": <0.0 to 1.0>, "reasoning": "<brief explanation>"}}"#
    );

    let llm_response = agent
        .llm
        .complete(&prompt, None, None, Some(512), Some(0.1), true)
        .await
        .context("LLM classification request failed")?;

    let parsed: serde_json::Value = serde_json::from_str(&llm_response.text)
        .context("Failed to parse LLM classification response as JSON")?;

    Ok(ClassifyResponse {
        category: parsed["category"]
            .as_str()
            .unwrap_or("cold_inquiry")
            .to_string(),
        confidence: parsed["confidence"].as_f64().unwrap_or(0.5),
        reasoning: parsed["reasoning"]
            .as_str()
            .unwrap_or("No reasoning provided")
            .to_string(),
    })
}

async fn draft_email_response(
    agent: &OpenClawAgent,
    email_from: &str,
    subject: &str,
    body: &str,
    category: &str,
    tone: &str,
) -> Result<String> {
    let prompt = format!(
        r#"Draft a professional email response to the following message.

Context:
- This is classified as: {category}
- Desired tone: {tone}
- We are a technology services company

Original email:
From: {email_from}
Subject: {subject}
Body:
{body}

Guidelines:
- Be {tone} but genuine
- Address the sender's specific needs or questions
- If it's a cold inquiry, express interest and suggest a discovery call
- If it's an existing client, be warm and reference the ongoing relationship
- If it's a referral, thank the referrer and welcome the new contact
- Keep the response concise (under 200 words)
- Include a clear call to action
- Do NOT include subject line — just the email body
- Sign off as "The Ridge Cell Team"

Write ONLY the email body text, no JSON wrapping:"#
    );

    let llm_response = agent
        .llm
        .complete(&prompt, None, None, Some(1024), Some(0.7), false)
        .await
        .context("LLM email draft request failed")?;

    Ok(llm_response.text.trim().to_string())
}

async fn draft_upwork_proposal(
    agent: &OpenClawAgent,
    job_title: &str,
    job_description: &str,
    relevant_experience: &str,
    portfolio_highlights: &str,
) -> Result<String> {
    let experience_section = if relevant_experience.is_empty() {
        String::new()
    } else {
        format!("\nRelevant experience to highlight:\n{relevant_experience}")
    };

    let portfolio_section = if portfolio_highlights.is_empty() {
        String::new()
    } else {
        format!("\nPortfolio highlights:\n{portfolio_highlights}")
    };

    let prompt = format!(
        r#"Write a compelling Upwork proposal cover letter for the following job.

Job Title: {job_title}
Job Description:
{job_description}
{experience_section}
{portfolio_section}

Guidelines:
- Open with a hook that shows you understand their specific problem
- Demonstrate relevant expertise without being generic
- Include a brief mention of similar past work
- Propose a clear next step (discovery call, sample deliverable, etc.)
- Keep it under 250 words — Upwork clients skim proposals
- Be confident but not arrogant
- Avoid cliches like "I'm the perfect fit" or "I'd love the opportunity"
- Do NOT include the job title or "Dear Hiring Manager" — Upwork proposals start directly

Write ONLY the proposal text:"#
    );

    let llm_response = agent
        .llm
        .complete(&prompt, None, None, Some(1024), Some(0.7), false)
        .await
        .context("LLM Upwork proposal request failed")?;

    Ok(llm_response.text.trim().to_string())
}

// ---------------------------------------------------------------------------
// Approval queue helpers
// ---------------------------------------------------------------------------

fn queue_for_approval(
    queue: &ApprovalQueue,
    entry_type: &str,
    draft: &str,
    category: Option<&str>,
    confidence: Option<f64>,
    original_subject: Option<&str>,
    original_from: Option<&str>,
    job_title: Option<&str>,
) -> String {
    let id = Uuid::new_v4().to_string();
    let entry = ApprovalEntry {
        id: id.clone(),
        entry_type: entry_type.to_string(),
        created_at: Utc::now().to_rfc3339(),
        status: "pending_approval".to_string(),
        category: category.map(|s| s.to_string()),
        confidence,
        draft: Some(draft.to_string()),
        original_subject: original_subject.map(|s| s.to_string()),
        original_from: original_from.map(|s| s.to_string()),
        job_title: job_title.map(|s| s.to_string()),
    };
    let value = serde_json::to_value(&entry).expect("failed to serialize approval entry");
    queue.insert(id.clone(), value);
    id
}

// ---------------------------------------------------------------------------
// App state shared across handlers
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: OpenClawAgent,
    queue: ApprovalQueue,
}

// ---------------------------------------------------------------------------
// Direct API endpoint handlers
// ---------------------------------------------------------------------------

async fn classify_handler(
    State(state): State<AppState>,
    Json(req): Json<ClassifyRequest>,
) -> impl IntoResponse {
    match classify_lead(&state.agent, &req.email_from, &req.subject, &req.body).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())),
        Err(e) => (
            StatusCode::INTERNAL_SERVER_ERROR,
            Json(serde_json::json!({ "error": format!("{:#}", e) })),
        ),
    }
}

async fn draft_handler(
    State(state): State<AppState>,
    Json(req): Json<DraftRequest>,
) -> impl IntoResponse {
    // Step 1: classify
    let classification =
        match classify_lead(&state.agent, &req.email_from, &req.subject, &req.body).await {
            Ok(c) => c,
            Err(e) => {
                return (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(serde_json::json!({ "error": format!("Classification failed: {:#}", e) })),
                );
            }
        };

    // Step 2: draft response
    let draft = match draft_email_response(
        &state.agent,
        &req.email_from,
        &req.subject,
        &req.body,
        &classification.category,
        &req.tone,
    )
    .await
    {
        Ok(d) => d,
        Err(e) => {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("Draft generation failed: {:#}", e) })),
            );
        }
    };

    // Step 3: queue for approval — NEVER auto-send
    let approval_id = queue_for_approval(
        &state.queue,
        "email_draft",
        &draft,
        Some(&classification.category),
        Some(classification.confidence),
        Some(&req.subject),
        Some(&req.email_from),
        None,
    );

    let response = DraftResponse {
        approval_id,
        category: classification.category,
        confidence: classification.confidence,
        draft,
        status: "pending_approval".to_string(),
    };

    (
        StatusCode::OK,
        Json(serde_json::to_value(response).unwrap()),
    )
}

async fn upwork_handler(
    State(state): State<AppState>,
    Json(req): Json<UpworkRequest>,
) -> impl IntoResponse {
    let draft = match draft_upwork_proposal(
        &state.agent,
        &req.job_title,
        &req.job_description,
        &req.relevant_experience,
        &req.portfolio_highlights,
    )
    .await
    {
        Ok(d) => d,
        Err(e) => {
            return (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("Upwork draft failed: {:#}", e) })),
            );
        }
    };

    let approval_id = queue_for_approval(
        &state.queue,
        "upwork_proposal",
        &draft,
        None,
        None,
        None,
        None,
        Some(&req.job_title),
    );

    let response = UpworkResponse {
        approval_id,
        draft,
        status: "pending_approval".to_string(),
    };

    (
        StatusCode::OK,
        Json(serde_json::to_value(response).unwrap()),
    )
}

async fn pending_handler(State(state): State<AppState>) -> impl IntoResponse {
    let pending: Vec<serde_json::Value> = state
        .queue
        .iter()
        .filter(|entry| {
            entry
                .value()
                .get("status")
                .and_then(|s| s.as_str())
                .map(|s| s == "pending_approval")
                .unwrap_or(false)
        })
        .map(|entry| entry.value().clone())
        .collect();

    Json(serde_json::json!({
        "pending": pending,
        "count": pending.len(),
    }))
}

async fn approve_handler(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> impl IntoResponse {
    match state.queue.get_mut(&id) {
        Some(mut entry) => {
            if let Some(obj) = entry.value_mut().as_object_mut() {
                let current_status = obj
                    .get("status")
                    .and_then(|s| s.as_str())
                    .unwrap_or("")
                    .to_string();

                if current_status != "pending_approval" {
                    return (
                        StatusCode::CONFLICT,
                        Json(serde_json::json!({
                            "error": format!("Entry is already '{}'", current_status),
                            "id": id,
                        })),
                    );
                }

                obj.insert(
                    "status".to_string(),
                    serde_json::Value::String("approved".to_string()),
                );
                obj.insert(
                    "approved_at".to_string(),
                    serde_json::Value::String(Utc::now().to_rfc3339()),
                );

                (
                    StatusCode::OK,
                    Json(serde_json::json!({
                        "id": id,
                        "status": "approved",
                        "message": "Draft approved. Ready for sending.",
                    })),
                )
            } else {
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(serde_json::json!({ "error": "Malformed entry" })),
                )
            }
        }
        None => (
            StatusCode::NOT_FOUND,
            Json(serde_json::json!({
                "error": "Approval entry not found",
                "id": id,
            })),
        ),
    }
}

async fn reject_handler(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> impl IntoResponse {
    match state.queue.get_mut(&id) {
        Some(mut entry) => {
            if let Some(obj) = entry.value_mut().as_object_mut() {
                let current_status = obj
                    .get("status")
                    .and_then(|s| s.as_str())
                    .unwrap_or("")
                    .to_string();

                if current_status != "pending_approval" {
                    return (
                        StatusCode::CONFLICT,
                        Json(serde_json::json!({
                            "error": format!("Entry is already '{}'", current_status),
                            "id": id,
                        })),
                    );
                }

                obj.insert(
                    "status".to_string(),
                    serde_json::Value::String("rejected".to_string()),
                );
                obj.insert(
                    "rejected_at".to_string(),
                    serde_json::Value::String(Utc::now().to_rfc3339()),
                );

                (
                    StatusCode::OK,
                    Json(serde_json::json!({
                        "id": id,
                        "status": "rejected",
                        "message": "Draft rejected.",
                    })),
                )
            } else {
                (
                    StatusCode::INTERNAL_SERVER_ERROR,
                    Json(serde_json::json!({ "error": "Malformed entry" })),
                )
            }
        }
        None => (
            StatusCode::NOT_FOUND,
            Json(serde_json::json!({
                "error": "Approval entry not found",
                "id": id,
            })),
        ),
    }
}

// ---------------------------------------------------------------------------
// TaskHandler implementation
// ---------------------------------------------------------------------------

struct LeadResponderHandler {
    queue: ApprovalQueue,
}

#[async_trait::async_trait]
impl TaskHandler for LeadResponderHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "lead_classify" => {
                let email_from = task.payload["email_from"]
                    .as_str()
                    .context("missing email_from in payload")?;
                let subject = task.payload["subject"]
                    .as_str()
                    .context("missing subject in payload")?;
                let body = task.payload["body"]
                    .as_str()
                    .context("missing body in payload")?;

                let result = classify_lead(agent, email_from, subject, body).await?;
                Ok(serde_json::to_value(result)?)
            }

            "email_draft" => {
                let email_from = task.payload["email_from"]
                    .as_str()
                    .context("missing email_from in payload")?;
                let subject = task.payload["subject"]
                    .as_str()
                    .context("missing subject in payload")?;
                let body = task.payload["body"]
                    .as_str()
                    .context("missing body in payload")?;
                let tone = task.payload["tone"].as_str().unwrap_or("professional");

                // Classify first
                let classification =
                    classify_lead(agent, email_from, subject, body).await?;

                // Draft response
                let draft = draft_email_response(
                    agent,
                    email_from,
                    subject,
                    body,
                    &classification.category,
                    tone,
                )
                .await?;

                // Queue for approval — NEVER auto-send
                let approval_id = queue_for_approval(
                    &self.queue,
                    "email_draft",
                    &draft,
                    Some(&classification.category),
                    Some(classification.confidence),
                    Some(subject),
                    Some(email_from),
                    None,
                );

                Ok(serde_json::json!({
                    "approval_id": approval_id,
                    "category": classification.category,
                    "confidence": classification.confidence,
                    "draft": draft,
                    "status": "pending_approval",
                }))
            }

            "upwork_respond" => {
                let job_title = task.payload["job_title"]
                    .as_str()
                    .context("missing job_title in payload")?;
                let job_description = task.payload["job_description"]
                    .as_str()
                    .context("missing job_description in payload")?;
                let relevant_experience = task.payload["relevant_experience"]
                    .as_str()
                    .unwrap_or("");
                let portfolio_highlights = task.payload["portfolio_highlights"]
                    .as_str()
                    .unwrap_or("");

                let draft = draft_upwork_proposal(
                    agent,
                    job_title,
                    job_description,
                    relevant_experience,
                    portfolio_highlights,
                )
                .await?;

                let approval_id = queue_for_approval(
                    &self.queue,
                    "upwork_proposal",
                    &draft,
                    None,
                    None,
                    None,
                    None,
                    Some(job_title),
                );

                Ok(serde_json::json!({
                    "approval_id": approval_id,
                    "draft": draft,
                    "status": "pending_approval",
                }))
            }

            "inbox_scan" => {
                // Placeholder — Gmail integration will come later
                Ok(serde_json::json!({
                    "message": "inbox_scan not yet implemented",
                    "processed": 0,
                }))
            }

            other => {
                anyhow::bail!("unknown task type: {}", other);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> Result<()> {
    // Override defaults for this agent
    std::env::set_var("AGENT_PORT", std::env::var("AGENT_PORT").unwrap_or_else(|_| "8002".to_string()));
    std::env::set_var(
        "AGENT_CAPABILITIES",
        std::env::var("AGENT_CAPABILITIES")
            .unwrap_or_else(|_| "lead_classify,email_draft,upwork_respond,inbox_scan".to_string()),
    );
    if std::env::var("AGENT_ID").is_err() {
        std::env::set_var("AGENT_ID", "lead-responder");
    }

    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config);

    // Shared approval queue
    let queue: ApprovalQueue = Arc::new(DashMap::new());

    let handler = LeadResponderHandler {
        queue: Arc::clone(&queue),
    };

    // Build agent-specific routes with state
    let app_state = AppState {
        agent: agent.clone(),
        queue: Arc::clone(&queue),
    };

    let extra_routes = Router::new()
        .route("/classify", post(classify_handler))
        .route("/draft", post(draft_handler))
        .route("/upwork", post(upwork_handler))
        .route("/leads/pending", get(pending_handler))
        .route("/leads/approve/{id}", post(approve_handler))
        .route("/leads/reject/{id}", post(reject_handler))
        .with_state(app_state);

    agent.run(handler, extra_routes).await
}
