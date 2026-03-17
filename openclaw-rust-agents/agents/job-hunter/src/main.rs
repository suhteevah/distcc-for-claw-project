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

use openclaw_sdk::{AgentConfig, ChatMessage, GroqModel, OpenClawAgent, Task, TaskHandler};

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
struct ScoreJobRequest {
    job_title: String,
    job_description: String,
    #[serde(default)]
    budget_range: Option<String>,
    #[serde(default)]
    job_url: Option<String>,
    #[serde(default)]
    source: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ScoreJobResult {
    score: u32,
    verdict: String,
    reasoning: String,
    strengths: Vec<String>,
    concerns: Vec<String>,
    recommended_bid: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    connect_cost: Option<u32>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    job_url: Option<String>,
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
// Scored job result (persisted)
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ScoredJob {
    job_title: String,
    job_url: Option<String>,
    score: u32,
    verdict: String,
    reasoning: String,
    strengths: Vec<String>,
    concerns: Vec<String>,
    recommended_bid: Option<String>,
    connect_cost: Option<u32>,
    scored_at: String,
    source: Option<String>,
}

const RESULTS_FILE: &str = "/opt/openclaw/job-hunter-results.json";

async fn load_results() -> Vec<ScoredJob> {
    match tokio::fs::read_to_string(RESULTS_FILE).await {
        Ok(s) => serde_json::from_str(&s).unwrap_or_default(),
        Err(_) => Vec::new(),
    }
}

async fn save_results(results: &[ScoredJob]) {
    if let Ok(json) = serde_json::to_string_pretty(results) {
        if let Err(e) = tokio::fs::write(RESULTS_FILE, json).await {
            tracing::error!(error = %e, "failed to save results file");
        }
    }
}

// ---------------------------------------------------------------------------
// Shared state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: Arc<OpenClawAgent>,
    soul: String,
    submissions: Arc<Mutex<Vec<serde_json::Value>>>,
    scored_jobs: Arc<Mutex<Vec<ScoredJob>>>,
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
// Connect cost scraper: fetch job page and extract connect cost
// ---------------------------------------------------------------------------

async fn scrape_connect_cost(job_url: &str) -> Option<u32> {
    // Load cookies from file
    let cookie_path = std::env::var("UPWORK_COOKIES_FILE")
        .unwrap_or_else(|_| "/opt/openclaw/openclaw-rust-agents/openclaw-rust-agents/agents/job-hunter/upwork-cookies.txt".into());

    let cookie_str = match tokio::fs::read_to_string(&cookie_path).await {
        Ok(s) => s.trim().to_string(),
        Err(e) => {
            warn!(error = %e, "could not read upwork cookies file");
            return None;
        }
    };

    let client = reqwest::Client::builder()
        .user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0")
        .build()
        .ok()?;

    let resp = client
        .get(job_url)
        .header("Cookie", &cookie_str)
        .header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        .header("Accept-Language", "en-US,en;q=0.9")
        .send()
        .await
        .ok()?;

    let body = resp.text().await.ok()?;

    // Look for "Send a proposal for: X Connects" pattern in the page HTML
    // Patterns seen: "Send a proposal for: 14 Connects" or "connectsRequired":14
    if let Some(cap) = regex_find_connects(&body) {
        return Some(cap);
    }

    None
}

fn regex_find_connects(html: &str) -> Option<u32> {
    // Pattern 1: "Send a proposal for: 14 Connects"
    if let Some(pos) = html.find("Send a proposal for:") {
        let after = &html[pos..std::cmp::min(pos + 80, html.len())];
        for word in after.split_whitespace() {
            if let Ok(n) = word.parse::<u32>() {
                return Some(n);
            }
        }
    }
    // Pattern 2: "connectsRequired":14 or "connects_required":14
    for pat in &["connectsRequired\":", "connects_required\":"] {
        if let Some(pos) = html.find(pat) {
            let after = &html[pos + pat.len()..std::cmp::min(pos + pat.len() + 10, html.len())];
            let num_str: String = after.chars().take_while(|c| c.is_ascii_digit()).collect();
            if let Ok(n) = num_str.parse::<u32>() {
                return Some(n);
            }
        }
    }
    // Pattern 3: "proposal for: <strong>14</strong> Connects"
    if let Some(pos) = html.find("proposal for:") {
        let after = &html[pos..std::cmp::min(pos + 120, html.len())];
        // Extract digits between tags
        let nums: String = after.chars().filter(|c| c.is_ascii_digit() || *c == ' ').collect();
        for word in nums.split_whitespace() {
            if let Ok(n) = word.parse::<u32>() {
                if n > 0 && n < 100 {
                    return Some(n);
                }
            }
        }
    }
    None
}

// ---------------------------------------------------------------------------
// LLM-powered: job scoring
// ---------------------------------------------------------------------------

const RIDGE_CELL_SKILLS: &str = "\
Ridge Cell Repair LLC — Matt Gates — Core Skills:
- AI/ML: Claude, GPT, Gemini, LLM integration, agentic AI, RAG, embeddings
- Full-stack: React, Next.js, Node.js, TypeScript, Python, Rust
- Infrastructure: Linux admin, Docker, Kubernetes, distributed systems
- Automation: Claude Code agents, API integrations, workflow automation
- Web: SEO, WordPress, web scraping, browser automation
- Hardware: Phone/device repair, soldering, diagnostics";

async fn score_upwork_job(
    agent: &OpenClawAgent,
    soul: &str,
    req: &ScoreJobRequest,
) -> Result<ScoreJobResult> {
    let prompt = format!(
        r#"You are a freelance job evaluator for Ridge Cell Repair LLC. Score how well this Upwork job matches our skills and business goals.

Job Title: {title}
Job Description: {desc}
{budget}

Our Skills & Services:
{skills}

Respond in JSON with exactly this structure (no markdown, no code fences):
{{
  "score": <integer 0-100>,
  "verdict": "<PURSUE or SKIP or MAYBE>",
  "reasoning": "<2-3 sentence assessment>",
  "strengths": ["<why we're a good fit>"],
  "concerns": ["<red flags or gaps>"],
  "recommended_bid": "<dollar amount or hourly rate suggestion, or null>"
}}

Scoring guide:
- 90-100 PURSUE: Perfect fit, directly matches our AI/automation expertise
- 70-89 PURSUE: Strong fit, we can deliver with high confidence
- 50-69 MAYBE: Partial fit, some skill overlap but not ideal
- 30-49 SKIP: Weak fit, too far from our core
- 0-29 SKIP: Not relevant at all

Prioritize jobs that:
1. Explicitly mention Claude, AI agents, or automation
2. Have reasonable budgets ($500+ fixed or $30+/hr)
3. Are from clients with good history
4. Match our full-stack AI development capabilities

Be harsh — only PURSUE jobs we can genuinely dominate."#,
        title = req.job_title,
        desc = req.job_description,
        budget = req.budget_range.as_deref().map(|b| format!("Budget: {}", b)).unwrap_or_default(),
        skills = RIDGE_CELL_SKILLS,
    );

    let messages = vec![
        ChatMessage { role: "system".into(), content: soul.to_string() },
        ChatMessage { role: "user".into(), content: prompt },
    ];
    let response = agent
        .groq()
        .chat(messages, Some(GroqModel::Smart), Some(4096), Some(0.3), true)
        .await
        .context("Groq job scoring failed")?;

    let result: ScoreJobResult = serde_json::from_str(&response.text)
        .context("failed to parse LLM job score response as JSON")?;

    Ok(result)
}

// ---------------------------------------------------------------------------
// LLM-powered: cover letter generation
// ---------------------------------------------------------------------------

async fn generate_cover_letter(
    agent: &OpenClawAgent,
    soul: &str,
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
        .groq()
        .complete(&prompt, Some(GroqModel::Smart), Some(soul), Some(4096), Some(0.7))
        .await
        .context("Groq cover letter generation failed")?;

    Ok(response.text)
}

// ---------------------------------------------------------------------------
// LLM-powered: resume match scoring
// ---------------------------------------------------------------------------

async fn score_resume_match(
    agent: &OpenClawAgent,
    soul: &str,
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

    let messages = vec![
        ChatMessage { role: "system".into(), content: soul.to_string() },
        ChatMessage { role: "user".into(), content: prompt },
    ];
    let response = agent
        .groq()
        .chat(messages, Some(GroqModel::Smart), Some(4096), Some(0.3), true)
        .await
        .context("Groq resume match scoring failed")?;

    let result: ResumeMatchResult = serde_json::from_str(&response.text)
        .context("failed to parse LLM resume match response as JSON")?;

    Ok(result)
}

// ---------------------------------------------------------------------------
// TaskHandler implementation
// ---------------------------------------------------------------------------

struct JobHunterHandler {
    soul: String,
    submissions: Arc<Mutex<Vec<serde_json::Value>>>,
    scored_jobs: Arc<Mutex<Vec<ScoredJob>>>,
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
                let letter = generate_cover_letter(agent, &self.soul, &req).await?;
                Ok(serde_json::json!({
                    "status": "completed",
                    "cover_letter": letter,
                    "generated_at": Utc::now().to_rfc3339(),
                }))
            }

            "resume_match" => {
                let req: ResumeMatchRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid resume_match payload")?;
                let result = score_resume_match(agent, &self.soul, &req).await?;
                serde_json::to_value(result).context("failed to serialize resume match result")
            }

            "score_job" => {
                let req: ScoreJobRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid score_job payload")?;
                info!(job_title = %req.job_title, "scoring upwork job");
                let mut result = score_upwork_job(agent, &self.soul, &req).await?;

                // Scrape connect cost if we have a job URL
                if let Some(ref url) = req.job_url {
                    info!(job_url = %url, "scraping connect cost");
                    match scrape_connect_cost(url).await {
                        Some(cost) => {
                            info!(job_title = %req.job_title, connect_cost = cost, "connect cost found");
                            result.connect_cost = Some(cost);
                        }
                        None => {
                            warn!(job_title = %req.job_title, "could not scrape connect cost (Cloudflare likely blocking)");
                        }
                    }
                    result.job_url = Some(url.clone());
                }

                // Only keep PURSUE for 95+ scores — we need sure-fire hits only
                if result.score < 95 && result.verdict == "PURSUE" {
                    info!(
                        job_title = %req.job_title,
                        score = result.score,
                        "downgrading PURSUE to MAYBE — score below 95 threshold"
                    );
                    result.verdict = "MAYBE".to_string();
                    result.concerns.push(format!("Score {} is below auto-propose threshold of 95", result.score));
                }

                // Downgrade verdict if connects are too expensive
                if let Some(cost) = result.connect_cost {
                    if cost > 6 && result.verdict == "PURSUE" {
                        info!(
                            job_title = %req.job_title,
                            connect_cost = cost,
                            "downgrading PURSUE to MAYBE — connects too expensive (>6)"
                        );
                        result.verdict = "MAYBE".to_string();
                        result.concerns.push(format!("Connect cost is {} (>6), too expensive for auto-propose", cost));
                    }
                }

                info!(
                    job_title = %req.job_title,
                    score = result.score,
                    verdict = %result.verdict,
                    connect_cost = ?result.connect_cost,
                    "job scored"
                );

                // Persist scored result to dashboard
                let scored = ScoredJob {
                    job_title: req.job_title.clone(),
                    job_url: result.job_url.clone(),
                    score: result.score,
                    verdict: result.verdict.clone(),
                    reasoning: result.reasoning.clone(),
                    strengths: result.strengths.clone(),
                    concerns: result.concerns.clone(),
                    recommended_bid: result.recommended_bid.clone(),
                    connect_cost: result.connect_cost,
                    scored_at: Utc::now().to_rfc3339(),
                    source: req.source.clone(),
                };
                {
                    let mut jobs = self.scored_jobs.lock().await;
                    // Deduplicate by job_url or title
                    jobs.retain(|j| {
                        if let (Some(a), Some(b)) = (&j.job_url, &scored.job_url) {
                            // Strip query params for comparison
                            let a_base = a.split('?').next().unwrap_or(a);
                            let b_base = b.split('?').next().unwrap_or(b);
                            a_base != b_base
                        } else {
                            j.job_title != scored.job_title
                        }
                    });
                    jobs.push(scored);
                    save_results(&jobs).await;
                }

                serde_json::to_value(result).context("failed to serialize job score result")
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
    match generate_cover_letter(&state.agent, &state.soul, &req).await {
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
    match score_resume_match(&state.agent, &state.soul, &req).await {
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
// Propose endpoint: generate a ready-to-submit proposal for a scored job
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ProposeRequest {
    /// Base job URL (e.g. https://www.upwork.com/jobs/~012345)
    job_url: String,
    /// Optional: override the job description (if scraped from browser)
    #[serde(default)]
    job_description: Option<String>,
    /// Optional: connect cost seen in browser
    #[serde(default)]
    connect_cost: Option<u32>,
    /// Optional: bid amount override
    #[serde(default)]
    bid_amount: Option<f64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ProposeResponse {
    status: String,
    job_title: String,
    job_url: String,
    score: u32,
    verdict: String,
    connect_cost: Option<u32>,
    cover_letter: String,
    recommended_bid: Option<String>,
    bid_amount: f64,
    generated_at: String,
}

async fn propose_endpoint(
    State(state): State<AppState>,
    Json(req): Json<ProposeRequest>,
) -> impl IntoResponse {
    // Find the scored job by URL (strip query params for matching)
    let req_base = req.job_url.split('?').next().unwrap_or(&req.job_url);

    let scored_job = {
        let jobs = state.scored_jobs.lock().await;
        jobs.iter().find(|j| {
            j.job_url.as_deref()
                .map(|u| u.split('?').next().unwrap_or(u) == req_base)
                .unwrap_or(false)
        }).cloned()
    };

    let job = match scored_job {
        Some(j) => j,
        None => {
            let body = serde_json::json!({
                "error": "Job not found in scored results. Score the job first via the pipeline.",
                "job_url": req.job_url,
            });
            return (StatusCode::NOT_FOUND, Json(body)).into_response();
        }
    };

    // Use browser-provided description if available, else use stored reasoning as context
    let description = req.job_description.unwrap_or_else(|| {
        format!(
            "{}\n\nStrengths: {}\n\nOur assessment: {}",
            job.job_title,
            job.strengths.join(", "),
            job.reasoning
        )
    });

    // Generate cover letter
    let letter_req = CoverLetterRequest {
        job_description: description,
        resume: Some(RIDGE_CELL_SKILLS.to_string()),
        tone: Some("confident, direct, and technical — no fluff".to_string()),
        highlights: Some(job.strengths.clone()),
    };

    match generate_cover_letter(&state.agent, &state.soul, &letter_req).await {
        Ok(letter) => {
            let connect_cost = req.connect_cost.or(job.connect_cost);
            let bid = req.bid_amount.unwrap_or_else(|| {
                // Parse recommended_bid if available, default to $50/hr
                job.recommended_bid.as_deref()
                    .and_then(|b| {
                        b.chars().filter(|c| c.is_ascii_digit() || *c == '.').collect::<String>()
                            .parse::<f64>().ok()
                    })
                    .unwrap_or(50.0)
            });

            let resp = ProposeResponse {
                status: "ready".to_string(),
                job_title: job.job_title,
                job_url: req.job_url,
                score: job.score,
                verdict: job.verdict,
                connect_cost,
                cover_letter: letter,
                recommended_bid: job.recommended_bid,
                bid_amount: bid,
                generated_at: Utc::now().to_rfc3339(),
            };
            (StatusCode::OK, Json(serde_json::to_value(resp).unwrap())).into_response()
        }
        Err(e) => {
            error!(error = %e, "proposal generation failed");
            let body = serde_json::json!({
                "error": format!("Cover letter generation failed: {:#}", e),
            });
            (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// Results dashboard endpoints
// ---------------------------------------------------------------------------

async fn results_endpoint(
    State(state): State<AppState>,
) -> impl IntoResponse {
    let jobs = state.scored_jobs.lock().await;
    let body = serde_json::json!({
        "total": jobs.len(),
        "pursue": jobs.iter().filter(|j| j.verdict == "PURSUE").count(),
        "maybe": jobs.iter().filter(|j| j.verdict == "MAYBE").count(),
        "skip": jobs.iter().filter(|j| j.verdict == "SKIP").count(),
        "jobs": *jobs,
    });
    (StatusCode::OK, Json(body))
}

async fn dashboard_endpoint(
    State(state): State<AppState>,
) -> impl IntoResponse {
    let jobs = state.scored_jobs.lock().await;
    let pursue_count = jobs.iter().filter(|j| j.verdict == "PURSUE").count();
    let maybe_count = jobs.iter().filter(|j| j.verdict == "MAYBE").count();
    let skip_count = jobs.iter().filter(|j| j.verdict == "SKIP").count();

    let mut rows = String::new();
    // Sort: PURSUE first, then MAYBE, then SKIP; within each, by score desc
    let mut sorted: Vec<_> = jobs.iter().collect();
    sorted.sort_by(|a, b| {
        let ord = |v: &str| match v { "PURSUE" => 0, "MAYBE" => 1, _ => 2 };
        ord(&a.verdict).cmp(&ord(&b.verdict)).then(b.score.cmp(&a.score))
    });

    for job in &sorted {
        let verdict_class = match job.verdict.as_str() {
            "PURSUE" => "pursue",
            "MAYBE" => "maybe",
            _ => "skip",
        };
        let connects = job.connect_cost
            .map(|c| format!("{}", c))
            .unwrap_or_else(|| "?".into());
        let url_link = job.job_url.as_deref()
            .map(|u| {
                let base = u.split('?').next().unwrap_or(u);
                format!("<a href=\"{}\" target=\"_blank\">View →</a>", base)
            })
            .unwrap_or_else(|| "—".into());
        let scored_time = &job.scored_at[..19]; // trim to readable
        let title_short = if job.job_title.len() > 70 {
            format!("{}…", &job.job_title[..67])
        } else {
            job.job_title.clone()
        };

        rows.push_str(&format!(
            r#"<tr class="{vc}">
                <td class="verdict-cell">{verdict}</td>
                <td class="score-cell">{score}</td>
                <td class="connects-cell">{connects}</td>
                <td class="title-cell" title="{full_title}">{title}</td>
                <td class="bid-cell">{bid}</td>
                <td class="time-cell">{time}</td>
                <td class="link-cell">{link}</td>
                <td class="action-cell">{action}</td>
            </tr>"#,
            vc = verdict_class,
            verdict = job.verdict,
            score = job.score,
            connects = connects,
            full_title = job.job_title.replace('"', "&quot;"),
            title = title_short,
            bid = job.recommended_bid.as_deref().unwrap_or("—"),
            time = scored_time,
            link = url_link,
            action = if job.verdict == "PURSUE" {
                let base_url = job.job_url.as_deref()
                    .map(|u| u.split('?').next().unwrap_or(u))
                    .unwrap_or("");
                format!("<button class=\"propose-btn\" onclick=\"propose('{}')\">Generate Proposal</button>", base_url)
            } else {
                "—".to_string()
            },
        ));
    }

    let html = format!(r#"<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Job Hunter Dashboard — OpenClaw</title>
<meta http-equiv="refresh" content="60">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }}
h1 {{ color: #58a6ff; margin-bottom: 6px; font-size: 1.6em; }}
.subtitle {{ color: #8b949e; margin-bottom: 20px; font-size: 0.9em; }}
.stats {{ display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
.stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px 24px; min-width: 120px; }}
.stat-card .number {{ font-size: 2em; font-weight: bold; }}
.stat-card .label {{ color: #8b949e; font-size: 0.85em; margin-top: 4px; }}
.stat-card.pursue .number {{ color: #3fb950; }}
.stat-card.maybe .number {{ color: #d29922; }}
.stat-card.skip .number {{ color: #f85149; }}
.stat-card.total .number {{ color: #58a6ff; }}
table {{ width: 100%; border-collapse: collapse; background: #161b22; border-radius: 8px; overflow: hidden; }}
th {{ background: #21262d; color: #8b949e; padding: 10px 12px; text-align: left; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #30363d; }}
td {{ padding: 10px 12px; border-bottom: 1px solid #21262d; font-size: 0.9em; }}
tr:hover {{ background: #1c2128; }}
tr.pursue .verdict-cell {{ color: #3fb950; font-weight: bold; }}
tr.maybe .verdict-cell {{ color: #d29922; font-weight: bold; }}
tr.skip .verdict-cell {{ color: #f85149; font-weight: bold; }}
.score-cell {{ font-weight: bold; font-size: 1.1em; }}
tr.pursue .score-cell {{ color: #3fb950; }}
tr.maybe .score-cell {{ color: #d29922; }}
tr.skip .score-cell {{ color: #8b949e; }}
.connects-cell {{ text-align: center; }}
.title-cell {{ max-width: 400px; }}
.time-cell {{ color: #8b949e; font-size: 0.85em; white-space: nowrap; }}
a {{ color: #58a6ff; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.footer {{ margin-top: 20px; color: #484f58; font-size: 0.8em; text-align: center; }}
.propose-btn {{ background: #238636; color: #fff; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.8em; font-weight: 600; }}
.propose-btn:hover {{ background: #2ea043; }}
.propose-btn:disabled {{ background: #484f58; cursor: not-allowed; }}
.proposal-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 100; justify-content: center; align-items: center; }}
.proposal-modal.active {{ display: flex; }}
.modal-content {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 24px; max-width: 700px; width: 90%; max-height: 80vh; overflow-y: auto; }}
.modal-content h2 {{ color: #58a6ff; margin-bottom: 12px; }}
.modal-content pre {{ background: #0d1117; padding: 16px; border-radius: 8px; white-space: pre-wrap; word-wrap: break-word; font-size: 0.9em; line-height: 1.5; margin: 12px 0; }}
.modal-content .meta {{ color: #8b949e; font-size: 0.85em; margin: 8px 0; }}
.modal-close {{ background: #f85149; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-right: 8px; }}
.modal-copy {{ background: #58a6ff; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }}
</style>
<script>
async function propose(jobUrl) {{
    const btn = event.target;
    btn.disabled = true;
    btn.textContent = 'Generating...';
    try {{
        const resp = await fetch('/propose', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ job_url: jobUrl }})
        }});
        const data = await resp.json();
        if (data.error) {{
            alert('Error: ' + data.error);
            btn.disabled = false;
            btn.textContent = 'Generate Proposal';
            return;
        }}
        const modal = document.getElementById('proposal-modal');
        document.getElementById('modal-title').textContent = data.job_title;
        document.getElementById('modal-letter').textContent = data.cover_letter;
        const metaEl = document.getElementById('modal-meta');
        metaEl.textContent = 'Score: ' + data.score + ' | Connects: ' + (data.connect_cost || '?') + ' | Bid: $' + data.bid_amount + '/hr';
        const link = document.createElement('a');
        link.href = data.job_url;
        link.target = '_blank';
        link.textContent = ' Open on Upwork';
        link.style.color = '#58a6ff';
        metaEl.appendChild(document.createTextNode(' | '));
        metaEl.appendChild(link);
        modal.classList.add('active');
        window._currentProposal = data;
    }} catch(e) {{
        alert('Failed: ' + e.message);
    }}
    btn.disabled = false;
    btn.textContent = 'Generate Proposal';
}}
function closeModal() {{
    document.getElementById('proposal-modal').classList.remove('active');
}}
function copyLetter() {{
    if (window._currentProposal) {{
        navigator.clipboard.writeText(window._currentProposal.cover_letter);
        const btn = event.target;
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = 'Copy Letter', 1500);
    }}
}}
</script>
</head>
<body>
<h1>🎯 Job Hunter Dashboard</h1>
<p class="subtitle">OpenClaw Fleet — Auto-refreshes every 60s</p>

<div class="stats">
    <div class="stat-card total"><div class="number">{total}</div><div class="label">Total Scored</div></div>
    <div class="stat-card pursue"><div class="number">{pursue}</div><div class="label">PURSUE (95+)</div></div>
    <div class="stat-card maybe"><div class="number">{maybe}</div><div class="label">MAYBE</div></div>
    <div class="stat-card skip"><div class="number">{skip}</div><div class="label">SKIP</div></div>
</div>

<table>
<thead>
    <tr><th>Verdict</th><th>Score</th><th>Connects</th><th>Job Title</th><th>Bid</th><th>Scored</th><th>Link</th><th>Action</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>

<div id="proposal-modal" class="proposal-modal" onclick="if(event.target===this)closeModal()">
    <div class="modal-content">
        <h2 id="modal-title"></h2>
        <div id="modal-meta" class="meta"></div>
        <pre id="modal-letter"></pre>
        <div>
            <button class="modal-close" onclick="closeModal()">Close</button>
            <button class="modal-copy" onclick="copyLetter()">Copy Letter</button>
        </div>
    </div>
</div>

<div class="footer">Ridge Cell Repair LLC — Powered by OpenClaw job-hunter agent</div>
</body>
</html>"#,
        total = jobs.len(),
        pursue = pursue_count,
        maybe = maybe_count,
        skip = skip_count,
        rows = rows,
    );

    axum::response::Html(html)
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config.clone());

    let soul = openclaw_sdk::load_soul(&config.agent_id)
        .unwrap_or_else(|| "You are an expert job application strategist.".to_string());

    let submissions: Arc<Mutex<Vec<serde_json::Value>>> = Arc::new(Mutex::new(Vec::new()));
    let scored_jobs: Arc<Mutex<Vec<ScoredJob>>> = Arc::new(Mutex::new(load_results().await));
    info!(loaded = scored_jobs.lock().await.len(), "loaded persisted scored jobs");

    let app_state = AppState {
        agent: Arc::new(agent.clone()),
        soul: soul.clone(),
        submissions: submissions.clone(),
        scored_jobs: scored_jobs.clone(),
    };

    let routes = Router::new()
        .route("/submit", post(submit_endpoint))
        .route("/submissions", get(submissions_endpoint))
        .route("/cover-letter", post(cover_letter_endpoint))
        .route("/resume-match", post(resume_match_endpoint))
        .route("/check-login", get(check_login_endpoint))
        .route("/propose", post(propose_endpoint))
        .route("/results", get(results_endpoint))
        .route("/dashboard", get(dashboard_endpoint))
        .with_state(app_state);

    let handler = JobHunterHandler {
        soul,
        submissions,
        scored_jobs,
    };

    agent.run(handler, routes).await
}
