use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;
use tracing::{error, info, warn};

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Request / response types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct SubmitRequest {
    job_url: String,
    cover_letter: String,
    #[serde(default = "default_bid_amount")]
    bid_amount: f64,
    #[serde(default = "default_bid_type")]
    bid_type: String,
}

fn default_bid_amount() -> f64 { 0.0 }
fn default_bid_type() -> String { "fixed".into() }

#[derive(Debug, Clone, Serialize, Deserialize)]
struct BulkSubmitRequest {
    proposals: Vec<SubmitRequest>,
    #[serde(default = "default_variant")]
    variant: String,
}

fn default_variant() -> String { "standard".into() }

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CoverLetterRequest {
    job_description: String,
    #[serde(default)]
    resume: Option<String>,
    #[serde(default)]
    tone: Option<String>,
    #[serde(default)]
    highlights: Option<Vec<String>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ResumeMatchRequest {
    job_description: String,
    resume: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ResumeMatchResult {
    match_score: u32,
    analysis: String,
    strengths: Vec<String>,
    gaps: Vec<String>,
    recommendations: Vec<String>,
}

// ---------------------------------------------------------------------------
// Shared state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: Arc<OpenClawAgent>,
    submissions: Arc<Mutex<Vec<serde_json::Value>>>,
}

// ---------------------------------------------------------------------------
// Stub: submit a single proposal (browser automation not yet ported)
// ---------------------------------------------------------------------------

fn stub_submit(req: &SubmitRequest) -> serde_json::Value {
    info!(
        job_url = %req.job_url,
        bid_amount = req.bid_amount,
        bid_type = %req.bid_type,
        "upwork_submit stub called (browser automation not yet ported)"
    );
    serde_json::json!({
        "status": "pending_implementation",
        "job_url": req.job_url,
        "bid_amount": req.bid_amount,
        "bid_type": req.bid_type,
        "message": "Browser automation not yet ported to Rust",
        "timestamp": Utc::now().to_rfc3339(),
    })
}

// ---------------------------------------------------------------------------
// LLM-powered: cover letter generation
// ---------------------------------------------------------------------------

async fn generate_cover_letter(
    agent: &OpenClawAgent,
    req: &CoverLetterRequest,
) -> Result<String> {
    let tone = req.tone.as_deref().unwrap_or("professional yet personable");

    let highlights_section = match &req.highlights {
        Some(h) if !h.is_empty() => {
            let bullet_list: String = h.iter().map(|s| format!("- {}\n", s)).collect();
            format!("\nKey highlights to emphasize:\n{}", bullet_list)
        }
        _ => String::new(),
    };

    let resume_section = match &req.resume {
        Some(r) if !r.is_empty() => format!("\n\nCandidate Resume / Background:\n{}", r),
        _ => String::new(),
    };

    let prompt = format!(
        r#"You are an expert freelance proposal writer. Write a compelling cover letter for the following job posting.

Job Description:
{}
{}{}
Tone: {}

Requirements:
1. Open with a hook that shows you understand the client's specific problem.
2. Demonstrate relevant experience with concrete examples or metrics.
3. Propose a clear approach or methodology for the project.
4. Close with a confident call to action.
5. Keep the letter between 150-300 words.
6. Do NOT use generic filler phrases like "I am writing to express my interest" or "I believe I am a perfect fit".
7. Do NOT include a subject line or greeting — just the body text.

Write the cover letter now."#,
        req.job_description,
        resume_section,
        highlights_section,
        tone,
    );

    let response = agent
        .llm
        .complete(&prompt, Some("heavy"), None, Some(4096), Some(0.7), false)
        .await
        .context("LLM cover letter generation failed")?;

    Ok(response.text)
}

// ---------------------------------------------------------------------------
// LLM-powered: resume match scoring
// ---------------------------------------------------------------------------

async fn score_resume_match(
    agent: &OpenClawAgent,
    req: &ResumeMatchRequest,
) -> Result<ResumeMatchResult> {
    let prompt = format!(
        r#"You are an expert recruiter and resume analyst. Analyze how well the following resume matches the job description.

Job Description:
{}

Resume:
{}

Respond in JSON with exactly this structure (no markdown, no code fences):
{{
  "match_score": <integer 0-100>,
  "analysis": "<2-3 sentence overall assessment>",
  "strengths": ["<strength 1>", "<strength 2>", ...],
  "gaps": ["<gap 1>", "<gap 2>", ...],
  "recommendations": ["<recommendation 1>", "<recommendation 2>", ...]
}}

Scoring guide:
- 90-100: Near-perfect match, candidate exceeds requirements
- 70-89: Strong match, candidate meets most requirements
- 50-69: Partial match, candidate has transferable skills but notable gaps
- 30-49: Weak match, significant skill gaps
- 0-29: Poor match, very few relevant qualifications

Be specific and reference actual content from both the resume and job description."#,
        req.job_description, req.resume,
    );

    let response = agent
        .llm
        .complete(&prompt, Some("heavy"), None, Some(4096), Some(0.3), true)
        .await
        .context("LLM resume match scoring failed")?;

    let result: ResumeMatchResult = serde_json::from_str(&response.text)
        .context("failed to parse LLM resume match response as JSON")?;

    Ok(result)
}

// ---------------------------------------------------------------------------
// TaskHandler implementation
// ---------------------------------------------------------------------------

struct JobHunterHandler {
    submissions: Arc<Mutex<Vec<serde_json::Value>>>,
}

#[async_trait::async_trait]
impl TaskHandler for JobHunterHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "upwork_submit" => {
                let req: SubmitRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid upwork_submit payload")?;
                let result = stub_submit(&req);
                let mut log = self.submissions.lock().await;
                log.push(result.clone());
                Ok(result)
            }

            "upwork_bulk_submit" => {
                let req: BulkSubmitRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid upwork_bulk_submit payload")?;
                info!(
                    count = req.proposals.len(),
                    variant = %req.variant,
                    "bulk submit requested"
                );
                let mut results = Vec::new();
                let mut log = self.submissions.lock().await;
                for proposal in &req.proposals {
                    let result = stub_submit(proposal);
                    log.push(result.clone());
                    results.push(result);
                }
                Ok(serde_json::json!({
                    "status": "pending_implementation",
                    "variant": req.variant,
                    "total": req.proposals.len(),
                    "results": results,
                }))
            }

            "check_login" => {
                warn!("check_login task received (browser session management not yet ported)");
                Ok(serde_json::json!({
                    "status": "pending_implementation",
                    "message": "Browser session management not yet ported",
                }))
            }

            "cover_letter" => {
                let req: CoverLetterRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid cover_letter payload")?;
                let letter = generate_cover_letter(agent, &req).await?;
                Ok(serde_json::json!({
                    "status": "completed",
                    "cover_letter": letter,
                    "generated_at": Utc::now().to_rfc3339(),
                }))
            }

            "resume_match" => {
                let req: ResumeMatchRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid resume_match payload")?;
                let result = score_resume_match(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize resume match result")
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

async fn submit_endpoint(
    State(state): State<AppState>,
    Json(req): Json<SubmitRequest>,
) -> impl IntoResponse {
    let result = stub_submit(&req);
    let mut log = state.submissions.lock().await;
    log.push(result.clone());
    (StatusCode::OK, Json(result))
}

async fn submissions_endpoint(
    State(state): State<AppState>,
) -> impl IntoResponse {
    let log = state.submissions.lock().await;
    let body = serde_json::json!({
        "total": log.len(),
        "submissions": *log,
    });
    (StatusCode::OK, Json(body))
}

async fn cover_letter_endpoint(
    State(state): State<AppState>,
    Json(req): Json<CoverLetterRequest>,
) -> impl IntoResponse {
    match generate_cover_letter(&state.agent, &req).await {
        Ok(letter) => {
            let body = serde_json::json!({
                "status": "completed",
                "cover_letter": letter,
                "generated_at": Utc::now().to_rfc3339(),
            });
            (StatusCode::OK, Json(body)).into_response()
        }
        Err(e) => {
            error!(error = %e, "cover letter generation failed");
            let body = serde_json::json!({
                "error": format!("{:#}", e),
            });
            (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response()
        }
    }
}

async fn resume_match_endpoint(
    State(state): State<AppState>,
    Json(req): Json<ResumeMatchRequest>,
) -> impl IntoResponse {
    match score_resume_match(&state.agent, &req).await {
        Ok(result) => {
            let body = serde_json::to_value(result).unwrap();
            (StatusCode::OK, Json(body)).into_response()
        }
        Err(e) => {
            error!(error = %e, "resume match scoring failed");
            let body = serde_json::json!({
                "error": format!("{:#}", e),
            });
            (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response()
        }
    }
}

async fn check_login_endpoint() -> impl IntoResponse {
    warn!("check_login endpoint called (browser session management not yet ported)");
    let body = serde_json::json!({
        "status": "pending_implementation",
        "message": "Browser session management not yet ported",
    });
    (StatusCode::OK, Json(body))
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config);

    let submissions: Arc<Mutex<Vec<serde_json::Value>>> = Arc::new(Mutex::new(Vec::new()));

    let app_state = AppState {
        agent: Arc::new(agent.clone()),
        submissions: submissions.clone(),
    };

    let routes = Router::new()
        .route("/submit", post(submit_endpoint))
        .route("/submissions", get(submissions_endpoint))
        .route("/cover-letter", post(cover_letter_endpoint))
        .route("/resume-match", post(resume_match_endpoint))
        .route("/check-login", get(check_login_endpoint))
        .with_state(app_state);

    let handler = JobHunterHandler { submissions };

    agent.run(handler, routes).await
}
