use std::sync::Arc;

use anyhow::{Context, Result};
use async_trait::async_trait;
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::post,
    Router,
};
use chrono::Utc;
use openclaw_sdk::{AgentConfig, ChatMessage, GroqModel, OpenClawAgent, Task, TaskHandler};
use serde::{Deserialize, Serialize};
use tracing::{error, info};

// ---------------------------------------------------------------------------
// Shared app state for direct API endpoints
// ---------------------------------------------------------------------------

struct SharedState {
    agent: OpenClawAgent,
    soul: String,
}

type AppState = Arc<SharedState>;

// ---------------------------------------------------------------------------
// Request / response types
// ---------------------------------------------------------------------------

#[derive(Debug, Deserialize)]
struct BlogPostRequest {
    topic: String,
    #[serde(default)]
    keywords: Vec<String>,
    #[serde(default = "default_tone")]
    tone: String,
    #[serde(default = "default_word_count")]
    word_count: u32,
    #[serde(default = "default_target_audience")]
    target_audience: String,
    #[serde(default)]
    include_meta: bool,
}

#[derive(Debug, Deserialize)]
struct SocialMediaRequest {
    topic: String,
    #[serde(default)]
    platforms: Vec<String>,
    #[serde(default = "default_tone")]
    tone: String,
    #[serde(default = "default_true")]
    include_hashtags: bool,
    #[serde(default)]
    cta: Option<String>,
}

#[derive(Debug, Deserialize)]
struct EmailCampaignRequest {
    campaign_type: CampaignType,
    subject_context: String,
    #[serde(default = "default_target_audience")]
    target_audience: String,
    #[serde(default)]
    product_service: Option<String>,
    #[serde(default = "default_num_emails")]
    num_emails: u32,
    #[serde(default = "default_tone")]
    tone: String,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
#[serde(rename_all = "snake_case")]
enum CampaignType {
    Nurture,
    Promo,
    ColdOutreach,
    FollowUp,
}

impl std::fmt::Display for CampaignType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CampaignType::Nurture => write!(f, "nurture"),
            CampaignType::Promo => write!(f, "promo"),
            CampaignType::ColdOutreach => write!(f, "cold_outreach"),
            CampaignType::FollowUp => write!(f, "follow_up"),
        }
    }
}

#[derive(Debug, Deserialize)]
struct SeoContentRequest {
    url: String,
    primary_keyword: String,
    #[serde(default)]
    secondary_keywords: Vec<String>,
    #[serde(default = "default_content_type")]
    content_type: SeoContentType,
    #[serde(default = "default_word_count")]
    word_count: u32,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
#[serde(rename_all = "snake_case")]
enum SeoContentType {
    LandingPage,
    ServicePage,
    AboutPage,
}

impl std::fmt::Display for SeoContentType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            SeoContentType::LandingPage => write!(f, "landing_page"),
            SeoContentType::ServicePage => write!(f, "service_page"),
            SeoContentType::AboutPage => write!(f, "about_page"),
        }
    }
}

#[derive(Debug, Serialize)]
struct ContentResponse {
    content_type: String,
    topic: String,
    body: serde_json::Value,
    word_count: u32,
    generated_at: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    meta: Option<serde_json::Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    model: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    tokens_used: Option<u32>,
}

// ---------------------------------------------------------------------------
// Defaults
// ---------------------------------------------------------------------------

fn default_tone() -> String {
    "professional".into()
}
fn default_word_count() -> u32 {
    1200
}
fn default_target_audience() -> String {
    "small business owners".into()
}
fn default_true() -> bool {
    true
}
fn default_num_emails() -> u32 {
    3
}
fn default_content_type() -> SeoContentType {
    SeoContentType::ServicePage
}

// ---------------------------------------------------------------------------
// Content generation logic
// ---------------------------------------------------------------------------

async fn generate_blog_post(agent: &OpenClawAgent, soul: &str, req: &BlogPostRequest) -> Result<ContentResponse> {
    let keywords_str = if req.keywords.is_empty() {
        String::new()
    } else {
        format!("\nTarget keywords: {}", req.keywords.join(", "))
    };

    let meta_instruction = if req.include_meta {
        "\n\nAfter the blog post content, add a line containing only \"---META---\" \
         followed by a JSON object with fields: \"title\", \"meta_description\" (max 160 chars), \
         \"slug\", \"excerpt\" (max 300 chars), and \"tags\" (array of strings)."
    } else {
        ""
    };

    let prompt = format!(
        "Write a {word_count}-word blog post about \"{topic}\" for the target audience: {audience}.\n\
         Tone: {tone}.{keywords}{meta}\n\n\
         Write the complete blog post now.",
        word_count = req.word_count,
        topic = req.topic,
        audience = req.target_audience,
        tone = req.tone,
        keywords = keywords_str,
        meta = meta_instruction,
    );

    let resp = agent
        .groq()
        .complete(&prompt, Some(GroqModel::Smart), Some(soul), Some(8192), Some(0.6))
        .await
        .context("blog post LLM generation failed")?;

    let (body_text, meta) = if req.include_meta {
        parse_meta_separator(&resp.text)
    } else {
        (resp.text.clone(), None)
    };

    let actual_word_count = body_text.split_whitespace().count() as u32;

    Ok(ContentResponse {
        content_type: "blog_post".into(),
        topic: req.topic.clone(),
        body: serde_json::Value::String(body_text),
        word_count: actual_word_count,
        generated_at: Utc::now().to_rfc3339(),
        meta,
        model: Some(resp.model),
        tokens_used: Some(resp.tokens_used),
    })
}

async fn generate_social_media(agent: &OpenClawAgent, soul: &str, req: &SocialMediaRequest) -> Result<ContentResponse> {
    let platforms_str = if req.platforms.is_empty() {
        "Twitter, LinkedIn, Instagram".to_string()
    } else {
        req.platforms.join(", ")
    };

    let cta_str = match &req.cta {
        Some(cta) => format!("\nCall to action: {}", cta),
        None => String::new(),
    };

    let prompt = format!(
        "Create social media posts about \"{topic}\" for the following platforms: {platforms}.\n\
         Tone: {tone}.\n\
         Include hashtags: {hashtags}.{cta}\n\n\
         Return a JSON object where each key is the platform name (lowercase) and the value is an object \
         with fields: \"text\" (the post text), \"character_count\" (integer), \
         and \"hashtags\" (array of strings, empty if not requested).",
        topic = req.topic,
        platforms = platforms_str,
        tone = req.tone,
        hashtags = req.include_hashtags,
        cta = cta_str,
    );

    let messages = vec![
        ChatMessage { role: "system".into(), content: soul.to_string() },
        ChatMessage { role: "user".into(), content: prompt },
    ];
    let resp = agent
        .groq()
        .chat(messages, Some(GroqModel::Fast), Some(2048), Some(0.7), true)
        .await
        .context("social media LLM generation failed")?;

    let body: serde_json::Value = serde_json::from_str(&resp.text)
        .unwrap_or_else(|_| serde_json::Value::String(resp.text.clone()));

    let word_count = resp.text.split_whitespace().count() as u32;

    Ok(ContentResponse {
        content_type: "social_media".into(),
        topic: req.topic.clone(),
        body,
        word_count,
        generated_at: Utc::now().to_rfc3339(),
        meta: None,
        model: Some(resp.model),
        tokens_used: Some(resp.tokens_used),
    })
}

async fn generate_email_campaign(agent: &OpenClawAgent, soul: &str, req: &EmailCampaignRequest) -> Result<ContentResponse> {
    let product_str = match &req.product_service {
        Some(ps) => format!("\nProduct/Service: {}", ps),
        None => String::new(),
    };

    let prompt = format!(
        "Create a {campaign_type} email campaign consisting of {num_emails} emails.\n\
         Subject/Context: {subject_context}\n\
         Target audience: {target_audience}\n\
         Tone: {tone}{product}\n\n\
         Return a JSON object with a field \"emails\" containing an array of objects, \
         each with fields: \"sequence_number\" (integer starting at 1), \
         \"subject_line\" (string), \"preview_text\" (string, max 90 chars), \
         \"body_html\" (string with HTML email body), \
         \"body_text\" (string with plain text version), \
         \"send_delay_days\" (integer, days after previous email), \
         and \"notes\" (string with strategy notes for this email).",
        campaign_type = req.campaign_type,
        num_emails = req.num_emails,
        subject_context = req.subject_context,
        target_audience = req.target_audience,
        tone = req.tone,
        product = product_str,
    );

    let messages = vec![
        ChatMessage { role: "system".into(), content: soul.to_string() },
        ChatMessage { role: "user".into(), content: prompt },
    ];
    let resp = agent
        .groq()
        .chat(messages, Some(GroqModel::Smart), Some(8192), Some(0.6), true)
        .await
        .context("email campaign LLM generation failed")?;

    let body: serde_json::Value = serde_json::from_str(&resp.text)
        .unwrap_or_else(|_| serde_json::Value::String(resp.text.clone()));

    let word_count = resp.text.split_whitespace().count() as u32;

    Ok(ContentResponse {
        content_type: "email_campaign".into(),
        topic: req.subject_context.clone(),
        body,
        word_count,
        generated_at: Utc::now().to_rfc3339(),
        meta: None,
        model: Some(resp.model),
        tokens_used: Some(resp.tokens_used),
    })
}

async fn generate_seo_content(agent: &OpenClawAgent, soul: &str, req: &SeoContentRequest) -> Result<ContentResponse> {
    let secondary_str = if req.secondary_keywords.is_empty() {
        String::new()
    } else {
        format!("\nSecondary keywords: {}", req.secondary_keywords.join(", "))
    };

    let prompt = format!(
        "Write SEO-optimized {content_type} content (~{word_count} words) for the URL: {url}\n\
         Primary keyword: \"{primary_keyword}\"{secondary}\n\n\
         Requirements:\n\
         - Include the primary keyword in the H1, first paragraph, and at least 2 subheadings\n\
         - Keyword density: 1-2% for primary keyword\n\
         - Use semantic variations and LSI keywords naturally\n\
         - Include internal linking placeholders as [INTERNAL_LINK: anchor text]\n\
         - Structure with proper heading hierarchy (H1, H2, H3)\n\
         - Include a compelling meta description (max 160 chars) at the top\n\
         - Write for both users and search engines\n\n\
         Write the complete page content now.",
        content_type = req.content_type,
        word_count = req.word_count,
        url = req.url,
        primary_keyword = req.primary_keyword,
        secondary = secondary_str,
    );

    let resp = agent
        .groq()
        .complete(&prompt, Some(GroqModel::Smart), Some(soul), Some(6144), Some(0.5))
        .await
        .context("SEO content LLM generation failed")?;

    let word_count = resp.text.split_whitespace().count() as u32;

    Ok(ContentResponse {
        content_type: "seo_content".into(),
        topic: req.primary_keyword.clone(),
        body: serde_json::Value::String(resp.text),
        word_count,
        generated_at: Utc::now().to_rfc3339(),
        meta: None,
        model: Some(resp.model),
        tokens_used: Some(resp.tokens_used),
    })
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Parse the "---META---" separator from blog post output.
/// Returns (body_text, Option<meta_json>).
fn parse_meta_separator(text: &str) -> (String, Option<serde_json::Value>) {
    if let Some(idx) = text.find("---META---") {
        let body = text[..idx].trim().to_string();
        let meta_str = text[idx + "---META---".len()..].trim();
        // Try to parse the meta JSON; if it fails, try extracting a JSON block
        let meta = serde_json::from_str::<serde_json::Value>(meta_str)
            .or_else(|_| {
                // Try to find JSON within code fences
                let cleaned = meta_str
                    .trim_start_matches("```json")
                    .trim_start_matches("```")
                    .trim_end_matches("```")
                    .trim();
                serde_json::from_str::<serde_json::Value>(cleaned)
            })
            .ok();
        (body, meta)
    } else {
        (text.to_string(), None)
    }
}

// ---------------------------------------------------------------------------
// Task handler (for poll-based task processing)
// ---------------------------------------------------------------------------

struct ContentMillHandler {
    soul: String,
}

#[async_trait]
impl TaskHandler for ContentMillHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "blog_post" => {
                let req: BlogPostRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid blog_post payload")?;
                let result = generate_blog_post(agent, &self.soul, &req).await?;
                serde_json::to_value(result).context("failed to serialize blog_post result")
            }
            "social_media" => {
                let req: SocialMediaRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid social_media payload")?;
                let result = generate_social_media(agent, &self.soul, &req).await?;
                serde_json::to_value(result).context("failed to serialize social_media result")
            }
            "email_campaign" => {
                let req: EmailCampaignRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid email_campaign payload")?;
                let result = generate_email_campaign(agent, &self.soul, &req).await?;
                serde_json::to_value(result).context("failed to serialize email_campaign result")
            }
            "seo_content" => {
                let req: SeoContentRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid seo_content payload")?;
                let result = generate_seo_content(agent, &self.soul, &req).await?;
                serde_json::to_value(result).context("failed to serialize seo_content result")
            }
            other => {
                anyhow::bail!("unknown task type: {}", other);
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Direct API endpoint handlers
// ---------------------------------------------------------------------------

async fn blog_handler(
    State(state): State<AppState>,
    Json(req): Json<BlogPostRequest>,
) -> impl IntoResponse {
    info!(topic = %req.topic, "POST /blog");
    match generate_blog_post(&state.agent, &state.soul, &req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => {
            error!(error = %e, "blog generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn social_handler(
    State(state): State<AppState>,
    Json(req): Json<SocialMediaRequest>,
) -> impl IntoResponse {
    info!(topic = %req.topic, "POST /social");
    match generate_social_media(&state.agent, &state.soul, &req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => {
            error!(error = %e, "social media generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn email_campaign_handler(
    State(state): State<AppState>,
    Json(req): Json<EmailCampaignRequest>,
) -> impl IntoResponse {
    info!(context = %req.subject_context, campaign_type = %req.campaign_type, "POST /email-campaign");
    match generate_email_campaign(&state.agent, &state.soul, &req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => {
            error!(error = %e, "email campaign generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn seo_content_handler(
    State(state): State<AppState>,
    Json(req): Json<SeoContentRequest>,
) -> impl IntoResponse {
    info!(keyword = %req.primary_keyword, url = %req.url, "POST /seo-content");
    match generate_seo_content(&state.agent, &state.soul, &req).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => {
            error!(error = %e, "SEO content generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> Result<()> {
    // Override defaults for this agent
    if std::env::var("AGENT_ID").is_err() {
        std::env::set_var("AGENT_ID", "content-mill");
    }
    if std::env::var("AGENT_PORT").is_err() {
        std::env::set_var("AGENT_PORT", "8003");
    }
    if std::env::var("AGENT_CAPABILITIES").is_err() {
        std::env::set_var("AGENT_CAPABILITIES", "blog_post,social_media,email_campaign,seo_content");
    }

    let config = AgentConfig::from_env().context("failed to load agent config")?;
    let soul = openclaw_sdk::load_soul(&config.agent_id)
        .unwrap_or_else(|| "You are an expert content writer for Ridge Cell Repair LLC.".to_string());
    info!(agent_id = %config.agent_id, soul_len = soul.len(), "loaded soul");

    let agent = OpenClawAgent::new(config);
    let app_state: AppState = Arc::new(SharedState {
        agent: agent.clone(),
        soul: soul.clone(),
    });

    let extra_routes = Router::new()
        .route("/blog", post(blog_handler))
        .route("/social", post(social_handler))
        .route("/email-campaign", post(email_campaign_handler))
        .route("/seo-content", post(seo_content_handler))
        .with_state(app_state);

    agent.run(ContentMillHandler { soul }, extra_routes).await
}
