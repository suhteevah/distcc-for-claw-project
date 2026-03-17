use std::sync::Arc;
use std::time::Instant;

use anyhow::{Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::post,
    Router,
};
use chrono::Utc;
use scraper::{Html, Selector};
use serde::{Deserialize, Serialize};
use tracing::{error, info};

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct PageData {
    url: String,
    status_code: u16,
    redirect_chain: Vec<String>,
    title: Option<String>,
    title_length: usize,
    meta_description: Option<String>,
    meta_description_length: usize,
    h1_count: usize,
    h1_texts: Vec<String>,
    h2_count: usize,
    h2_texts: Vec<String>,
    image_count: usize,
    images_missing_alt: usize,
    internal_links: usize,
    external_links: usize,
    has_canonical: bool,
    canonical_url: Option<String>,
    robots_meta: Option<String>,
    has_og_tags: bool,
    has_schema: bool,
    word_count: usize,
    html_size_kb: f64,
    load_time_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct SeoIssue {
    severity: String,
    category: String,
    issue: String,
    fix: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct AuditResult {
    url: String,
    score: i32,
    summary: String,
    page_data: PageData,
    issues: Vec<SeoIssue>,
    recommendations: Vec<String>,
    audited_at: String,
}

#[derive(Debug, Deserialize)]
struct AuditRequest {
    url: String,
}

// ---------------------------------------------------------------------------
// fetch_page
// ---------------------------------------------------------------------------

async fn fetch_page(url: &str) -> Result<PageData> {
    let client = reqwest::Client::builder()
        .redirect(reqwest::redirect::Policy::limited(10))
        .timeout(std::time::Duration::from_secs(30))
        .user_agent("OpenClaw-SEO-Auditor/1.0")
        .build()
        .context("failed to build HTTP client")?;

    let start = Instant::now();
    let response = client.get(url).send().await.context("failed to fetch URL")?;
    let load_time_ms = start.elapsed().as_millis() as u64;

    let status_code = response.status().as_u16();

    // Collect redirect chain from the response URL vs original
    let final_url = response.url().to_string();
    let redirect_chain = if final_url != url {
        vec![url.to_string(), final_url.clone()]
    } else {
        vec![]
    };

    let html_text = response.text().await.context("failed to read response body")?;
    let html_size_kb = html_text.len() as f64 / 1024.0;

    let document = Html::parse_document(&html_text);

    // Parse the base domain for internal/external link classification
    let base_host = reqwest::Url::parse(url)
        .ok()
        .and_then(|u| u.host_str().map(|h| h.to_string()))
        .unwrap_or_default();

    // Title
    let title_sel = Selector::parse("title").unwrap();
    let title = document
        .select(&title_sel)
        .next()
        .map(|el| el.text().collect::<String>().trim().to_string());
    let title_length = title.as_ref().map(|t| t.len()).unwrap_or(0);

    // Meta description
    let meta_sel = Selector::parse(r#"meta[name="description"]"#).unwrap();
    let meta_description = document
        .select(&meta_sel)
        .next()
        .and_then(|el| el.value().attr("content").map(|s| s.trim().to_string()));
    let meta_description_length = meta_description.as_ref().map(|d| d.len()).unwrap_or(0);

    // H1
    let h1_sel = Selector::parse("h1").unwrap();
    let h1_texts: Vec<String> = document
        .select(&h1_sel)
        .map(|el| el.text().collect::<String>().trim().to_string())
        .collect();
    let h1_count = h1_texts.len();

    // H2
    let h2_sel = Selector::parse("h2").unwrap();
    let h2_texts: Vec<String> = document
        .select(&h2_sel)
        .map(|el| el.text().collect::<String>().trim().to_string())
        .collect();
    let h2_count = h2_texts.len();

    // Images
    let img_sel = Selector::parse("img").unwrap();
    let images: Vec<_> = document.select(&img_sel).collect();
    let image_count = images.len();
    let images_missing_alt = images
        .iter()
        .filter(|el| {
            let alt = el.value().attr("alt").unwrap_or("").trim();
            alt.is_empty()
        })
        .count();

    // Links
    let a_sel = Selector::parse("a[href]").unwrap();
    let mut internal_links = 0usize;
    let mut external_links = 0usize;
    for el in document.select(&a_sel) {
        if let Some(href) = el.value().attr("href") {
            let href = href.trim();
            if href.starts_with('#') || href.is_empty() {
                continue;
            }
            if href.starts_with('/') || href.starts_with("./") || href.starts_with("../") {
                internal_links += 1;
            } else if let Ok(parsed) = reqwest::Url::parse(href) {
                if parsed.host_str().map(|h| h == base_host).unwrap_or(false) {
                    internal_links += 1;
                } else {
                    external_links += 1;
                }
            } else {
                // Relative link without scheme
                internal_links += 1;
            }
        }
    }

    // Canonical
    let canonical_sel = Selector::parse(r#"link[rel="canonical"]"#).unwrap();
    let canonical_el = document.select(&canonical_sel).next();
    let has_canonical = canonical_el.is_some();
    let canonical_url = canonical_el.and_then(|el| el.value().attr("href").map(|s| s.to_string()));

    // Robots meta
    let robots_sel = Selector::parse(r#"meta[name="robots"]"#).unwrap();
    let robots_meta = document
        .select(&robots_sel)
        .next()
        .and_then(|el| el.value().attr("content").map(|s| s.to_string()));

    // Open Graph tags
    let og_sel = Selector::parse(r#"meta[property^="og:"]"#).unwrap();
    let has_og_tags = document.select(&og_sel).next().is_some();

    // Schema.org (JSON-LD or microdata)
    let schema_ld_sel = Selector::parse(r#"script[type="application/ld+json"]"#).unwrap();
    let has_schema_ld = document.select(&schema_ld_sel).next().is_some();
    let itemscope_sel = Selector::parse("[itemscope]").unwrap();
    let has_microdata = document.select(&itemscope_sel).next().is_some();
    let has_schema = has_schema_ld || has_microdata;

    // Word count (visible text in body)
    let body_sel = Selector::parse("body").unwrap();
    let word_count = document
        .select(&body_sel)
        .next()
        .map(|body| {
            let text: String = body.text().collect();
            text.split_whitespace().count()
        })
        .unwrap_or(0);

    Ok(PageData {
        url: url.to_string(),
        status_code,
        redirect_chain,
        title,
        title_length,
        meta_description,
        meta_description_length,
        h1_count,
        h1_texts,
        h2_count,
        h2_texts,
        image_count,
        images_missing_alt,
        internal_links,
        external_links,
        has_canonical,
        canonical_url,
        robots_meta,
        has_og_tags,
        has_schema,
        word_count,
        html_size_kb,
        load_time_ms,
    })
}

// ---------------------------------------------------------------------------
// score_page
// ---------------------------------------------------------------------------

fn score_page(page: &PageData) -> (i32, Vec<SeoIssue>) {
    let mut score: i32 = 100;
    let mut issues: Vec<SeoIssue> = Vec::new();

    // Title checks
    match &page.title {
        None => {
            score -= 15;
            issues.push(SeoIssue {
                severity: "critical".into(),
                category: "title".into(),
                issue: "Page has no title tag".into(),
                fix: "Add a descriptive <title> tag between 30-60 characters".into(),
            });
        }
        Some(t) if t.len() < 30 => {
            score -= 5;
            issues.push(SeoIssue {
                severity: "warning".into(),
                category: "title".into(),
                issue: format!("Title is too short ({} chars)", t.len()),
                fix: "Expand the title to at least 30 characters with relevant keywords".into(),
            });
        }
        Some(t) if t.len() > 60 => {
            score -= 3;
            issues.push(SeoIssue {
                severity: "info".into(),
                category: "title".into(),
                issue: format!("Title is too long ({} chars)", t.len()),
                fix: "Shorten the title to 60 characters or fewer to avoid truncation in SERPs"
                    .into(),
            });
        }
        _ => {}
    }

    // Meta description checks
    match &page.meta_description {
        None => {
            score -= 10;
            issues.push(SeoIssue {
                severity: "critical".into(),
                category: "meta_description".into(),
                issue: "Page has no meta description".into(),
                fix: "Add a meta description between 120-160 characters summarizing the page"
                    .into(),
            });
        }
        Some(d) if d.to_lowercase().contains("lorem ipsum") => {
            score -= 20;
            issues.push(SeoIssue {
                severity: "critical".into(),
                category: "meta_description".into(),
                issue: "Meta description contains placeholder text (lorem ipsum)".into(),
                fix: "Replace placeholder text with a real meta description".into(),
            });
        }
        Some(d) if d.len() < 120 => {
            score -= 5;
            issues.push(SeoIssue {
                severity: "warning".into(),
                category: "meta_description".into(),
                issue: format!("Meta description is too short ({} chars)", d.len()),
                fix: "Expand the meta description to at least 120 characters".into(),
            });
        }
        _ => {}
    }

    // H1 checks
    if page.h1_count == 0 {
        score -= 10;
        issues.push(SeoIssue {
            severity: "critical".into(),
            category: "headings".into(),
            issue: "Page has no H1 tag".into(),
            fix: "Add exactly one H1 tag with the primary keyword for the page".into(),
        });
    } else if page.h1_count > 1 {
        score -= 5;
        issues.push(SeoIssue {
            severity: "warning".into(),
            category: "headings".into(),
            issue: format!("Page has {} H1 tags (should be exactly 1)", page.h1_count),
            fix: "Use only one H1 tag per page; demote extras to H2 or lower".into(),
        });
    }

    // Images missing alt
    if page.images_missing_alt > 0 {
        let deduction = std::cmp::min(10, (page.images_missing_alt * 2) as i32);
        score -= deduction;
        issues.push(SeoIssue {
            severity: "warning".into(),
            category: "images".into(),
            issue: format!(
                "{} of {} images are missing alt text",
                page.images_missing_alt, page.image_count
            ),
            fix: "Add descriptive alt attributes to all images for accessibility and SEO".into(),
        });
    }

    // Word count
    if page.word_count < 300 {
        score -= 10;
        issues.push(SeoIssue {
            severity: "warning".into(),
            category: "content".into(),
            issue: format!(
                "Page has thin content ({} words, minimum recommended is 300)",
                page.word_count
            ),
            fix: "Add more substantive content to the page (aim for 300+ words)".into(),
        });
    }

    // Canonical
    if !page.has_canonical {
        score -= 5;
        issues.push(SeoIssue {
            severity: "info".into(),
            category: "canonical".into(),
            issue: "Page has no canonical URL".into(),
            fix: "Add a <link rel=\"canonical\"> tag to prevent duplicate content issues".into(),
        });
    }

    // OG tags
    if !page.has_og_tags {
        score -= 5;
        issues.push(SeoIssue {
            severity: "info".into(),
            category: "social".into(),
            issue: "Page has no Open Graph tags".into(),
            fix: "Add og:title, og:description, og:image, and og:url meta tags for social sharing"
                .into(),
        });
    }

    // Schema
    if !page.has_schema {
        score -= 5;
        issues.push(SeoIssue {
            severity: "info".into(),
            category: "structured_data".into(),
            issue: "Page has no structured data (Schema.org)".into(),
            fix: "Add JSON-LD structured data to help search engines understand page content"
                .into(),
        });
    }

    // Load time
    if page.load_time_ms > 3000 {
        score -= 10;
        issues.push(SeoIssue {
            severity: "warning".into(),
            category: "performance".into(),
            issue: format!("Page load time is slow ({}ms)", page.load_time_ms),
            fix: "Optimize page load time to under 3 seconds (compress assets, use caching, reduce server response time)".into(),
        });
    }

    // Status code
    if page.status_code != 200 {
        score -= 20;
        issues.push(SeoIssue {
            severity: "critical".into(),
            category: "http_status".into(),
            issue: format!("Page returned HTTP {} (expected 200)", page.status_code),
            fix: "Ensure the page returns a 200 OK status code".into(),
        });
    }

    // Clamp score
    score = score.max(0);

    (score, issues)
}

// ---------------------------------------------------------------------------
// generate_analysis
// ---------------------------------------------------------------------------

async fn generate_analysis(
    agent: &OpenClawAgent,
    page: &PageData,
    score: i32,
    issues: &[SeoIssue],
    soul: &str,
) -> Result<String> {
    let issues_summary: Vec<String> = issues
        .iter()
        .map(|i| format!("- [{}] {}: {}", i.severity.to_uppercase(), i.category, i.issue))
        .collect();

    let prompt = format!(
        r#"You are an SEO expert. Analyze the following page audit data and provide a 3-paragraph executive summary.

URL: {}
SEO Score: {}/100
Status Code: {}
Title: {}
Meta Description: {}
H1 Tags: {} (count: {})
H2 Tags: {} (count: {})
Images: {} total, {} missing alt text
Internal Links: {}
External Links: {}
Word Count: {}
HTML Size: {:.1} KB
Load Time: {}ms
Has Canonical: {}
Has OG Tags: {}
Has Schema: {}

Issues Found:
{}

Paragraph 1: Overall assessment of the page's SEO health and the score meaning.
Paragraph 2: The most critical issues found and their potential impact on search rankings.
Paragraph 3: Prioritized action items to improve the score.

Write concisely and professionally. Do not use bullet points or headers — just three flowing paragraphs."#,
        page.url,
        score,
        page.status_code,
        page.title.as_deref().unwrap_or("(none)"),
        page.meta_description.as_deref().unwrap_or("(none)"),
        page.h1_texts.join(", "),
        page.h1_count,
        page.h2_texts.join(", "),
        page.h2_count,
        page.image_count,
        page.images_missing_alt,
        page.internal_links,
        page.external_links,
        page.word_count,
        page.html_size_kb,
        page.load_time_ms,
        page.has_canonical,
        page.has_og_tags,
        page.has_schema,
        issues_summary.join("\n"),
    );

    let response = agent
        .groq()
        .complete(&prompt, Some(openclaw_sdk::GroqModel::Smart), Some(soul), Some(4096), Some(0.4))
        .await
        .context("LLM analysis generation failed")?;

    Ok(response.text)
}

// ---------------------------------------------------------------------------
// run_audit (shared logic for task handler and direct API)
// ---------------------------------------------------------------------------

async fn run_audit(agent: &OpenClawAgent, url: &str, soul: &str) -> Result<AuditResult> {
    info!(url = %url, "starting SEO audit");

    let page_data = fetch_page(url).await.context("failed to fetch page")?;
    let (score, issues) = score_page(&page_data);

    let summary = match generate_analysis(agent, &page_data, score, &issues, soul).await {
        Ok(s) => s,
        Err(e) => {
            error!(error = %e, "LLM analysis failed, using fallback summary");
            let critical_count = issues.iter().filter(|i| i.severity == "critical").count();
            let warning_count = issues.iter().filter(|i| i.severity == "warning").count();
            format!(
                "SEO audit completed with a score of {}/100. Found {} critical issues and {} warnings. \
                 Unable to generate detailed AI analysis at this time.",
                score, critical_count, warning_count
            )
        }
    };

    let recommendations: Vec<String> = issues.iter().map(|i| i.fix.clone()).collect();

    Ok(AuditResult {
        url: url.to_string(),
        score,
        summary,
        page_data,
        issues,
        recommendations,
        audited_at: Utc::now().to_rfc3339(),
    })
}

// ---------------------------------------------------------------------------
// TaskHandler
// ---------------------------------------------------------------------------

struct SeoHandler {
    soul: Arc<String>,
}

#[async_trait::async_trait]
impl TaskHandler for SeoHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        if task.task_type != "seo_audit" {
            anyhow::bail!("unsupported task_type: {}", task.task_type);
        }

        let url = task
            .payload
            .get("url")
            .and_then(|v| v.as_str())
            .context("task payload missing 'url' field")?;

        let result = run_audit(agent, url, &self.soul).await?;
        serde_json::to_value(result).context("failed to serialize audit result")
    }
}

// ---------------------------------------------------------------------------
// Direct API endpoint
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct AppState {
    agent: Arc<OpenClawAgent>,
    soul: Arc<String>,
}

async fn audit_endpoint(
    State(state): State<AppState>,
    Json(req): Json<AuditRequest>,
) -> impl IntoResponse {
    match run_audit(&state.agent, &req.url, &state.soul).await {
        Ok(result) => (StatusCode::OK, Json(serde_json::to_value(result).unwrap())).into_response(),
        Err(e) => {
            let body = serde_json::json!({
                "error": format!("{:#}", e),
            });
            (StatusCode::INTERNAL_SERVER_ERROR, Json(body)).into_response()
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

    let soul = openclaw_sdk::load_soul(&config.agent_id).unwrap_or_else(|| {
        "You are an SEO expert. Analyze page audit data and provide actionable recommendations."
            .to_string()
    });
    let soul = Arc::new(soul);

    let state = AppState {
        agent: Arc::new(agent.clone()),
        soul: soul.clone(),
    };
    let routes = Router::new()
        .route("/audit", post(audit_endpoint))
        .with_state(state);

    agent.run(SeoHandler { soul }, routes).await
}
