use std::sync::Arc;

use anyhow::{Context, Result};
use async_trait::async_trait;
use axum::{
    extract::State,
    http::StatusCode,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::{Datelike, Local, Timelike, Utc};
use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use tracing::{error, info, warn};

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const HIMALAYA_BIN: &str = "/usr/local/bin/himalaya";
const HIMALAYA_CONFIG: &str = "/opt/openclaw/himalaya/config.toml";
const OUTPUT_DIR: &str = "/opt/openclaw/gateway-config/workspace-mailclaw";
const ACCOUNTS: &[&str] = &["ridgecell", "suhteevah", "mmichels"];
const PAGE_SIZE: usize = 10;
const PREVIEW_LINES: usize = 30;
const FETCH_INTERVAL_SECS: u64 = 1500; // 25 minutes

// Upwork job classification keywords
const HOT_KEYWORDS: &[&str] = &[
    "claude", "anthropic", "llm", "gpt", "openai", "ai agent", "ai automation",
    "rust developer", "rust engineer", "rust programming",
    "full-stack", "fullstack", "full stack",
    "chatbot", "rag", "retrieval augmented", "langchain", "langgraph",
    "mcp", "model context protocol",
];
const WARM_KEYWORDS: &[&str] = &[
    "machine learning", "deep learning", "nlp", "natural language",
    "python", "typescript", "react", "next.js", "nextjs",
    "api development", "backend", "microservices",
    "automation", "web scraping", "data pipeline",
    "devops", "docker", "kubernetes",
];
const COLD_KEYWORDS: &[&str] = &[
    "wordpress", "shopify", "wix", "squarespace",
    "data entry", "virtual assistant", "social media manager",
    "graphic design", "logo design", "video editing",
    "seo only", "link building",
];

// ---------------------------------------------------------------------------
// Data structures
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
struct MailClawData {
    accounts: Vec<AccountData>,
    upwork_jobs: Vec<UpworkJob>,
    triage_summary: String,
    fetched_at: String,
    errors: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct AccountData {
    name: String,
    envelopes: Vec<EmailEnvelope>,
    previews: Vec<EmailPreview>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct EmailEnvelope {
    id: String,
    from: String,
    subject: String,
    date: String,
    raw_line: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct EmailPreview {
    id: String,
    body_preview: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct UpworkJob {
    title: String,
    description: String,
    job_url: Option<String>,
    budget: Option<String>,
    rating: String, // HOT, WARM, COLD
    match_reasons: Vec<String>,
    account: String,
    email_id: String,
}

// ---------------------------------------------------------------------------
// App state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct MailClawState {
    agent: Arc<OpenClawAgent>,
    data: Arc<RwLock<MailClawData>>,
}

// ---------------------------------------------------------------------------
// Himalaya interaction
// ---------------------------------------------------------------------------

async fn run_himalaya(args: &[&str]) -> Result<String> {
    let output = tokio::process::Command::new(HIMALAYA_BIN)
        .arg("-c")
        .arg(HIMALAYA_CONFIG)
        .args(args)
        .output()
        .await
        .context("failed to spawn himalaya")?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("himalaya {} failed: {}", args.join(" "), stderr);
    }

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

async fn fetch_envelopes(account: &str) -> Result<Vec<EmailEnvelope>> {
    let page_size = PAGE_SIZE.to_string();
    let output = run_himalaya(&[
        "envelope", "list", "-a", account, "--page-size", &page_size,
    ])
    .await?;

    let mut envelopes = Vec::new();
    for line in output.lines() {
        // Parse the table format: | ID | FLAGS | SUBJECT | FROM | DATE |
        let parts: Vec<&str> = line.split('|').collect();
        if parts.len() >= 5 {
            let id = parts[1].trim().to_string();
            if id.is_empty() || id == "ID" || !id.chars().next().map_or(false, |c| c.is_ascii_digit()) {
                continue;
            }
            let subject = parts.get(3).map(|s| s.trim()).unwrap_or("").to_string();
            let from = parts.get(4).map(|s| s.trim()).unwrap_or("").to_string();
            let date = parts.get(5).map(|s| s.trim()).unwrap_or("").to_string();

            envelopes.push(EmailEnvelope {
                id,
                from,
                subject,
                date,
                raw_line: line.to_string(),
            });
        }
    }

    Ok(envelopes)
}

async fn fetch_preview(account: &str, email_id: &str) -> Result<EmailPreview> {
    let output = run_himalaya(&["message", "read", "-a", account, email_id]).await?;

    let preview: String = output
        .lines()
        .take(PREVIEW_LINES)
        .collect::<Vec<_>>()
        .join("\n");

    Ok(EmailPreview {
        id: email_id.to_string(),
        body_preview: preview,
    })
}

// ---------------------------------------------------------------------------
// Upwork job extraction + classification
// ---------------------------------------------------------------------------

fn is_upwork_notification(envelope: &EmailEnvelope) -> bool {
    envelope.from.contains("Upwork") && envelope.subject.contains("New job:")
}

fn extract_job_title(subject: &str) -> String {
    subject
        .strip_prefix("New job: ")
        .or_else(|| subject.strip_prefix("New job:"))
        .unwrap_or(subject)
        .trim()
        .to_string()
}

fn extract_job_url(body: &str) -> Option<String> {
    for line in body.lines() {
        if let Some(start) = line.find("https://www.upwork.com/jobs/~") {
            let url_part = &line[start..];
            let end = url_part
                .find(|c: char| c.is_whitespace() || c == '"' || c == '\'' || c == '>')
                .unwrap_or(url_part.len());
            return Some(url_part[..end].to_string());
        }
    }
    None
}

fn extract_description(body: &str) -> String {
    for line in body.lines() {
        let trimmed = line.trim();
        if trimmed.len() > 60
            && !trimmed.starts_with("http")
            && !trimmed.starts_with('|')
            && !trimmed[..20.min(trimmed.len())].contains(':')
        {
            return trimmed[..500.min(trimmed.len())].to_string();
        }
    }
    String::new()
}

fn classify_job(title: &str, description: &str) -> (String, Vec<String>) {
    let text = format!("{} {}", title, description).to_lowercase();
    let mut reasons = Vec::new();

    // Check for COLD first (auto-reject)
    for kw in COLD_KEYWORDS {
        if text.contains(kw) {
            reasons.push(format!("cold: matches '{}'", kw));
            return ("COLD".to_string(), reasons);
        }
    }

    // Check HOT keywords
    let mut hot_count = 0;
    for kw in HOT_KEYWORDS {
        if text.contains(kw) {
            hot_count += 1;
            reasons.push(format!("hot: matches '{}'", kw));
        }
    }

    if hot_count >= 2 {
        return ("HOT".to_string(), reasons);
    }

    // Check WARM keywords
    let mut warm_count = 0;
    for kw in WARM_KEYWORDS {
        if text.contains(kw) {
            warm_count += 1;
            reasons.push(format!("warm: matches '{}'", kw));
        }
    }

    if hot_count >= 1 {
        return ("HOT".to_string(), reasons);
    }

    if warm_count >= 2 {
        return ("WARM".to_string(), reasons);
    }

    if warm_count >= 1 {
        reasons.push("single warm keyword match".to_string());
        return ("WARM".to_string(), reasons);
    }

    reasons.push("no keyword matches".to_string());
    ("COLD".to_string(), reasons)
}

// ---------------------------------------------------------------------------
// Generate triage summary text
// ---------------------------------------------------------------------------

fn generate_triage_summary(data: &MailClawData) -> String {
    let mut out = String::new();
    let now = &data.fetched_at;
    out.push_str(&format!("=== MailClaw Triage — {} ===\n\n", now));

    // Per-account summary
    for acct in &data.accounts {
        out.push_str(&format!("### {} ({} emails)\n", acct.name, acct.envelopes.len()));
        for env in &acct.envelopes {
            let marker = if is_upwork_notification(env) { "[UW]" } else { "    " };
            out.push_str(&format!("  {} {} — {}\n", marker, env.from, env.subject));
        }
        out.push('\n');
    }

    // Upwork jobs section
    let hot: Vec<_> = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").collect();
    let warm: Vec<_> = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").collect();
    let cold: Vec<_> = data.upwork_jobs.iter().filter(|j| j.rating == "COLD").collect();

    out.push_str(&format!(
        ">>> UPWORK JOBS: {} total ({} HOT, {} WARM, {} COLD)\n\n",
        data.upwork_jobs.len(), hot.len(), warm.len(), cold.len()
    ));

    for job in &hot {
        out.push_str(&format!("[HOT] {}\n", job.title));
        for reason in &job.match_reasons {
            out.push_str(&format!("      {}\n", reason));
        }
        if let Some(url) = &job.job_url {
            out.push_str(&format!("      {}\n", url));
        }
        out.push('\n');
    }

    for job in &warm {
        out.push_str(&format!("[WARM] {}\n", job.title));
        for reason in &job.match_reasons {
            out.push_str(&format!("       {}\n", reason));
        }
        out.push('\n');
    }

    if !cold.is_empty() {
        out.push_str(&format!("[COLD] {} jobs skipped\n\n", cold.len()));
    }

    if !data.errors.is_empty() {
        out.push_str(">>> ERRORS\n");
        for e in &data.errors {
            out.push_str(&format!("! {}\n", e));
        }
        out.push('\n');
    }

    out.push_str("=== End Triage ===\n");
    out
}

// ---------------------------------------------------------------------------
// Core fetch routine
// ---------------------------------------------------------------------------

async fn fetch_all_mail() -> MailClawData {
    let mut data = MailClawData::default();
    let mut errors = Vec::new();
    let mut all_upwork_jobs = Vec::new();

    for account in ACCOUNTS {
        let mut acct_data = AccountData {
            name: account.to_string(),
            envelopes: Vec::new(),
            previews: Vec::new(),
        };

        // Fetch envelopes
        match fetch_envelopes(account).await {
            Ok(envelopes) => {
                // Find Upwork job notifications
                for env in &envelopes {
                    if is_upwork_notification(env) {
                        // Read full body for URL extraction
                        let (description, job_url) = match fetch_preview(account, &env.id).await {
                            Ok(preview) => {
                                let url = extract_job_url(&preview.body_preview);
                                let desc = extract_description(&preview.body_preview);
                                (desc, url)
                            }
                            Err(e) => {
                                warn!(account = account, id = %env.id, error = %e, "failed to read job email body");
                                (String::new(), None)
                            }
                        };

                        let title = extract_job_title(&env.subject);
                        let (rating, reasons) = classify_job(&title, &description);

                        all_upwork_jobs.push(UpworkJob {
                            title,
                            description: if description.is_empty() {
                                env.subject.clone()
                            } else {
                                description
                            },
                            job_url,
                            budget: None,
                            rating,
                            match_reasons: reasons,
                            account: account.to_string(),
                            email_id: env.id.clone(),
                        });
                    }
                }

                // Fetch previews for recent non-Upwork emails (top 5)
                let non_upwork: Vec<_> = envelopes
                    .iter()
                    .filter(|e| !is_upwork_notification(e))
                    .take(5)
                    .collect();

                for env in &non_upwork {
                    match fetch_preview(account, &env.id).await {
                        Ok(preview) => acct_data.previews.push(preview),
                        Err(e) => warn!(account = account, id = %env.id, error = %e, "failed to read email preview"),
                    }
                }

                acct_data.envelopes = envelopes;
            }
            Err(e) => {
                errors.push(format!("{}: {}", account, e));
            }
        }

        data.accounts.push(acct_data);
    }

    data.upwork_jobs = all_upwork_jobs;
    data.errors = errors;
    data.fetched_at = Utc::now().to_rfc3339();
    data.triage_summary = generate_triage_summary(&data);
    data
}

async fn save_mailclaw_files(data: &MailClawData) -> Result<()> {
    tokio::fs::create_dir_all(OUTPUT_DIR).await.context("create mailclaw output dir")?;

    // Save latest-emails.txt (same format the gateway/LLM expects)
    let mut emails_txt = format!("=== Email Fetch {} ===\n", data.fetched_at);
    for acct in &data.accounts {
        emails_txt.push_str(&format!("\n### Account: {} ###\n", acct.name));
        emails_txt.push_str("--- Recent Envelopes ---\n");
        for env in &acct.envelopes {
            emails_txt.push_str(&format!("{}\n", env.raw_line));
        }
        emails_txt.push('\n');
        for preview in &acct.previews {
            emails_txt.push_str(&format!("--- Message {} Preview ---\n", preview.id));
            emails_txt.push_str(&preview.body_preview);
            emails_txt.push_str("\n...\n\n");
        }
    }
    emails_txt.push_str("=== End of Email Fetch ===\n");
    tokio::fs::write(format!("{}/latest-emails.txt", OUTPUT_DIR), &emails_txt).await?;

    // Save hot-jobs.json (same format job-hunter reads)
    let hot_warm_jobs: Vec<_> = data
        .upwork_jobs
        .iter()
        .filter(|j| j.rating == "HOT" || j.rating == "WARM")
        .map(|j| {
            serde_json::json!({
                "title": j.title,
                "description": j.description,
                "job_url": j.job_url,
                "budget": j.budget,
                "rating": j.rating,
            })
        })
        .collect();

    let jobs_json = serde_json::json!({
        "timestamp": data.fetched_at,
        "jobs": hot_warm_jobs,
    });
    tokio::fs::write(
        format!("{}/hot-jobs.json", OUTPUT_DIR),
        serde_json::to_string_pretty(&jobs_json)?,
    )
    .await?;

    // Save triage summary (for LLM narrator to read)
    tokio::fs::write(
        format!("{}/triage-summary.txt", OUTPUT_DIR),
        &data.triage_summary,
    )
    .await?;

    // Save full data as JSON
    tokio::fs::write(
        format!("{}/mailclaw-data.json", OUTPUT_DIR),
        serde_json::to_string_pretty(&data)?,
    )
    .await?;

    info!(
        jobs = data.upwork_jobs.len(),
        hot = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count(),
        warm = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count(),
        "MailClaw files saved to {}",
        OUTPUT_DIR
    );

    Ok(())
}

// ---------------------------------------------------------------------------
// Discord webhook — rich embeds, zero LLM cost
// ---------------------------------------------------------------------------

const DISCORD_WEBHOOK_ENV: &str = "DISCORD_MAILCLAW_WEBHOOK";

fn build_mailclaw_embeds(data: &MailClawData) -> Vec<serde_json::Value> {
    let mut embeds = Vec::new();

    // Summary embed
    let total_emails: usize = data.accounts.iter().map(|a| a.envelopes.len()).sum();
    let hot_count = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count();
    let warm_count = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count();
    let cold_count = data.upwork_jobs.iter().filter(|j| j.rating == "COLD").count();

    // Account summaries
    let mut account_fields = Vec::new();
    for acct in &data.accounts {
        let upwork_count = acct.envelopes.iter().filter(|e| is_upwork_notification(e)).count();
        let other_count = acct.envelopes.len() - upwork_count;
        let notable: Vec<String> = acct.envelopes.iter()
            .filter(|e| !is_upwork_notification(e))
            .take(3)
            .map(|e| format!("• {} — *{}*", e.from, e.subject.chars().take(50).collect::<String>()))
            .collect();
        let value = format!(
            "📨 {} emails ({} Upwork, {} other)\n{}",
            acct.envelopes.len(), upwork_count, other_count,
            if notable.is_empty() { String::new() } else { notable.join("\n") }
        );
        account_fields.push(serde_json::json!({
            "name": format!("📧 {}", acct.name),
            "value": value,
            "inline": false,
        }));
    }

    embeds.push(serde_json::json!({
        "title": format!("📬 MailClaw Triage — {} emails", total_emails),
        "color": 3447003, // blue
        "fields": account_fields,
    }));

    // HOT jobs embed (red, attention-grabbing)
    if hot_count > 0 {
        let hot_text: String = data.upwork_jobs.iter()
            .filter(|j| j.rating == "HOT")
            .map(|j| {
                let url = j.job_url.as_deref().unwrap_or("#");
                let reasons = j.match_reasons.join(", ");
                format!("🔥 **[{}]({})**\n└ {}", j.title, url, reasons)
            })
            .collect::<Vec<_>>()
            .join("\n\n");
        embeds.push(serde_json::json!({
            "title": format!("🎯 {} HOT Jobs", hot_count),
            "description": hot_text,
            "color": 15548997, // red
        }));
    }

    // WARM jobs embed (yellow)
    if warm_count > 0 {
        let warm_text: String = data.upwork_jobs.iter()
            .filter(|j| j.rating == "WARM")
            .map(|j| {
                let url = j.job_url.as_deref().unwrap_or("#");
                let reasons = j.match_reasons.join(", ");
                format!("🟡 **[{}]({})**\n└ {}", j.title, url, reasons)
            })
            .collect::<Vec<_>>()
            .join("\n\n");
        embeds.push(serde_json::json!({
            "title": format!("⚡ {} WARM Jobs", warm_count),
            "description": warm_text,
            "color": 16776960, // yellow
        }));
    }

    // Cold summary (just a count, no details)
    if cold_count > 0 {
        if let Some(last) = embeds.last_mut() {
            let fields = last.get_mut("fields").and_then(|f| f.as_array_mut());
            if let Some(fields) = fields {
                fields.push(serde_json::json!({
                    "name": "❄️ Cold",
                    "value": format!("{} jobs filtered out", cold_count),
                    "inline": true,
                }));
            }
        }
    }

    // Footer on last embed
    if let Some(last) = embeds.last_mut() {
        last["footer"] = serde_json::json!({ "text": "openclaw-mailclaw • Rust • Zero LLM tokens" });
        last["timestamp"] = serde_json::json!(data.fetched_at);
    }

    embeds
}

async fn post_mailclaw_to_discord(http: &reqwest::Client, data: &MailClawData) -> Result<()> {
    let webhook_url = match std::env::var(DISCORD_WEBHOOK_ENV) {
        Ok(url) => url,
        Err(_) => {
            info!("No {} set, skipping Discord webhook post", DISCORD_WEBHOOK_ENV);
            return Ok(());
        }
    };

    let embeds = build_mailclaw_embeds(data);

    let body = serde_json::json!({
        "username": "MailClaw",
        "avatar_url": "https://cdn.discordapp.com/embed/avatars/1.png",
        "embeds": embeds,
    });

    let http_client = reqwest::Client::new();
    let resp = http_client.post(&webhook_url)
        .json(&body)
        .send()
        .await
        .context("Discord webhook post failed")?;

    if !resp.status().is_success() {
        let status = resp.status();
        let text = resp.text().await.unwrap_or_default();
        anyhow::bail!("Discord webhook returned {}: {}", status, text);
    }

    info!("Posted mailclaw embeds to Discord webhook");
    Ok(())
}

// ---------------------------------------------------------------------------
// Morning digest + evening wrap-up embeds (replace gateway 7B crons)
// ---------------------------------------------------------------------------

fn build_morning_digest_embeds(data: &MailClawData) -> Vec<serde_json::Value> {
    let mut embeds = Vec::new();
    let total_emails: usize = data.accounts.iter().map(|a| a.envelopes.len()).sum();
    let hot_count = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count();
    let warm_count = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count();
    let cold_count = data.upwork_jobs.iter().filter(|j| j.rating == "COLD").count();

    // Header embed
    embeds.push(serde_json::json!({
        "title": "☀️ MailClaw Morning Digest",
        "description": format!(
            "**{}** emails across **{}** accounts\n**{}** Upwork jobs detected ({} 🔥 HOT, {} ⚡ WARM, {} ❄️ COLD)",
            total_emails, data.accounts.len(), data.upwork_jobs.len(), hot_count, warm_count, cold_count
        ),
        "color": 3447003, // blue
    }));

    // Per-account breakdown
    for acct in &data.accounts {
        let upwork_count = acct.envelopes.iter().filter(|e| is_upwork_notification(e)).count();
        let notable: Vec<String> = acct.envelopes.iter()
            .filter(|e| !is_upwork_notification(e))
            .take(5)
            .map(|e| format!("• **{}** — {}", e.from, e.subject.chars().take(60).collect::<String>()))
            .collect();
        let mut desc = format!("📨 {} emails ({} Upwork notifications)\n", acct.envelopes.len(), upwork_count);
        if !notable.is_empty() {
            desc.push_str(&notable.join("\n"));
        }
        embeds.push(serde_json::json!({
            "title": format!("📧 {}", acct.name),
            "description": desc,
            "color": 5793266, // teal
        }));
    }

    // HOT jobs with full details
    for job in data.upwork_jobs.iter().filter(|j| j.rating == "HOT") {
        let url = job.job_url.as_deref().unwrap_or("#");
        let reasons = job.match_reasons.join(", ");
        let desc_preview = if job.description.len() > 200 {
            format!("{}...", &job.description[..200])
        } else {
            job.description.clone()
        };
        embeds.push(serde_json::json!({
            "title": format!("🔥 HOT: {}", job.title),
            "description": format!("[Apply →]({})\n\n> {}\n\n**Matched:** {}", url, desc_preview, reasons),
            "color": 15548997, // red
        }));
    }

    // WARM jobs summary
    let warm_jobs: Vec<_> = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").collect();
    if !warm_jobs.is_empty() {
        let warm_lines: Vec<String> = warm_jobs.iter().map(|j| {
            let url = j.job_url.as_deref().unwrap_or("#");
            format!("⚡ [{}]({}) — {}", j.title, url, j.match_reasons.join(", "))
        }).collect();
        embeds.push(serde_json::json!({
            "title": format!("⚡ {} WARM Jobs", warm_jobs.len()),
            "description": warm_lines.join("\n"),
            "color": 16776960, // yellow
        }));
    }

    // Footer
    if let Some(last) = embeds.last_mut() {
        last["footer"] = serde_json::json!({ "text": "Morning Digest • openclaw-mailclaw • Zero LLM tokens" });
        last["timestamp"] = serde_json::json!(data.fetched_at);
    }

    // Discord limits 10 embeds per message — truncate if needed
    embeds.truncate(10);
    embeds
}

fn build_evening_wrapup_embeds(data: &MailClawData) -> Vec<serde_json::Value> {
    let mut embeds = Vec::new();
    let total_emails: usize = data.accounts.iter().map(|a| a.envelopes.len()).sum();
    let hot_count = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count();
    let warm_count = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count();

    // Compact summary
    let mut summary_lines = Vec::new();
    for acct in &data.accounts {
        summary_lines.push(format!("**{}**: {} emails", acct.name, acct.envelopes.len()));
    }

    let action_items = if hot_count > 0 {
        let hot_titles: Vec<String> = data.upwork_jobs.iter()
            .filter(|j| j.rating == "HOT")
            .map(|j| {
                let url = j.job_url.as_deref().unwrap_or("#");
                format!("🔥 [{}]({})", j.title, url)
            })
            .collect();
        format!("\n\n**⚠️ Action Required — {} HOT jobs need attention:**\n{}", hot_count, hot_titles.join("\n"))
    } else {
        "\n\n✅ No urgent jobs today.".to_string()
    };

    let warm_note = if warm_count > 0 {
        format!("\n📋 {} WARM jobs worth reviewing when you get a chance.", warm_count)
    } else {
        String::new()
    };

    embeds.push(serde_json::json!({
        "title": "🌙 MailClaw Evening Wrap-Up",
        "description": format!(
            "**Today's inbox:** {} emails across {} accounts\n{}{}{}\n\nGoodnight. 🦀",
            total_emails, data.accounts.len(),
            summary_lines.join(" • "),
            action_items,
            warm_note
        ),
        "color": 10181046, // purple
        "footer": { "text": "Evening Wrap-Up • openclaw-mailclaw • Zero LLM tokens" },
        "timestamp": data.fetched_at,
    }));

    embeds
}

async fn post_scheduled_embeds(http: &reqwest::Client, data: &MailClawData, embeds: Vec<serde_json::Value>, label: &str) -> Result<()> {
    let webhook_url = match std::env::var(DISCORD_WEBHOOK_ENV) {
        Ok(url) => url,
        Err(_) => {
            info!("No {} set, skipping {} post", DISCORD_WEBHOOK_ENV, label);
            return Ok(());
        }
    };

    let body = serde_json::json!({
        "username": "MailClaw",
        "avatar_url": "https://cdn.discordapp.com/embed/avatars/1.png",
        "embeds": embeds,
    });

    let resp = http.post(&webhook_url)
        .json(&body)
        .send()
        .await
        .context(format!("{} Discord post failed", label))?;

    if !resp.status().is_success() {
        let status = resp.status();
        let text = resp.text().await.unwrap_or_default();
        anyhow::bail!("{} webhook returned {}: {}", label, status, text);
    }

    info!("{} posted to Discord", label);
    Ok(())
}

// ---------------------------------------------------------------------------
// Background timers
// ---------------------------------------------------------------------------

/// Scheduled digest/wrap-up timer — fires at 6am and 6pm PST
async fn digest_timer(state: MailClawState) {
    let http = reqwest::Client::new();
    let mut last_morning: Option<u32> = None; // day-of-year we last fired morning
    let mut last_evening: Option<u32> = None; // day-of-year we last fired evening

    loop {
        tokio::time::sleep(std::time::Duration::from_secs(60)).await; // check every minute

        let now = Local::now();
        let hour = now.hour();
        let minute = now.minute();
        let day = now.ordinal();

        // Morning digest at 6:00 AM local
        if hour == 6 && minute == 0 && last_morning != Some(day) {
            last_morning = Some(day);
            info!("Morning digest timer fired");
            // Fresh fetch for the digest
            let data = fetch_all_mail().await;
            if let Err(e) = save_mailclaw_files(&data).await {
                error!(error = %e, "failed to save mailclaw files for morning digest");
            }
            let embeds = build_morning_digest_embeds(&data);
            if let Err(e) = post_scheduled_embeds(&http, &data, embeds, "Morning Digest").await {
                error!(error = %e, "Morning Digest post failed");
            }
            *state.data.write().await = data;
        }

        // Evening wrap-up at 6:00 PM local
        if hour == 18 && minute == 0 && last_evening != Some(day) {
            last_evening = Some(day);
            info!("Evening wrap-up timer fired");
            // Use latest data without re-fetching (wrap-up is a summary of the day)
            let data = {
                let d = state.data.read().await;
                d.clone()
            };
            let embeds = build_evening_wrapup_embeds(&data);
            if let Err(e) = post_scheduled_embeds(&http, &data, embeds, "Evening Wrap-Up").await {
                error!(error = %e, "Evening Wrap-Up post failed");
            }
        }
    }
}

/// Regular triage timer — fetches + posts embeds every 25 minutes
async fn mailclaw_timer(state: MailClawState) {
    let http = reqwest::Client::new();

    // Initial fetch on startup
    info!("Running initial email fetch...");
    let data = fetch_all_mail().await;
    if let Err(e) = save_mailclaw_files(&data).await {
        error!(error = %e, "failed to save initial mailclaw files");
    }
    // Post to Discord on startup too
    if let Err(e) = post_mailclaw_to_discord(&http, &data).await {
        warn!(error = %e, "Discord webhook post failed on startup");
    }
    *state.data.write().await = data;
    info!("Initial email fetch complete");

    let interval = std::time::Duration::from_secs(FETCH_INTERVAL_SECS);
    loop {
        tokio::time::sleep(interval).await;
        info!("MailClaw timer fired — fetching emails...");

        let data = fetch_all_mail().await;
        if let Err(e) = save_mailclaw_files(&data).await {
            error!(error = %e, "failed to save mailclaw files");
        }
        // Post rich embeds to Discord — zero LLM tokens
        if let Err(e) = post_mailclaw_to_discord(&http, &data).await {
            warn!(error = %e, "Discord webhook post failed");
        }
        *state.data.write().await = data;
    }
}

// ---------------------------------------------------------------------------
// HTTP handlers
// ---------------------------------------------------------------------------

async fn trigger_handler(State(state): State<MailClawState>) -> impl IntoResponse {
    info!("Manual email fetch triggered");
    let http = reqwest::Client::new();
    let data = fetch_all_mail().await;
    if let Err(e) = save_mailclaw_files(&data).await {
        error!(error = %e, "failed to save mailclaw files");
    }
    // Post embeds to Discord
    if let Err(e) = post_mailclaw_to_discord(&http, &data).await {
        warn!(error = %e, "Discord webhook post failed on trigger");
    }
    let summary = data.triage_summary.clone();
    *state.data.write().await = data;
    (StatusCode::OK, summary)
}

async fn data_handler(State(state): State<MailClawState>) -> impl IntoResponse {
    let data = state.data.read().await;
    Json(data.clone())
}

async fn triage_handler(State(state): State<MailClawState>) -> impl IntoResponse {
    let data = state.data.read().await;
    (
        StatusCode::OK,
        [("content-type", "text/plain")],
        data.triage_summary.clone(),
    )
}

async fn jobs_handler(State(state): State<MailClawState>) -> impl IntoResponse {
    let data = state.data.read().await;
    Json(serde_json::json!({
        "timestamp": data.fetched_at,
        "total": data.upwork_jobs.len(),
        "jobs": data.upwork_jobs,
    }))
}

async fn dashboard_handler(State(state): State<MailClawState>) -> impl IntoResponse {
    let data = state.data.read().await;

    let hot_count = data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count();
    let warm_count = data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count();
    let cold_count = data.upwork_jobs.iter().filter(|j| j.rating == "COLD").count();
    let total_emails: usize = data.accounts.iter().map(|a| a.envelopes.len()).sum();

    let mut jobs_html = String::new();
    for job in &data.upwork_jobs {
        let color = match job.rating.as_str() {
            "HOT" => "#f85149",
            "WARM" => "#d29922",
            _ => "#484f58",
        };
        let url_link = job.job_url.as_deref().unwrap_or("#");
        jobs_html.push_str(&format!(
            r#"<tr>
                <td><span style="color:{};font-weight:bold">{}</span></td>
                <td><a href="{}" target="_blank" style="color:#58a6ff">{}</a></td>
                <td style="font-size:11px;color:#8b949e">{}</td>
                <td style="font-size:11px">{}</td>
            </tr>"#,
            color,
            job.rating,
            url_link,
            job.title.replace('<', "&lt;"),
            job.description.chars().take(80).collect::<String>().replace('<', "&lt;"),
            job.match_reasons.join(", "),
        ));
    }

    let html = format!(
        r#"<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><title>MailClaw Dashboard</title>
<style>
body {{ background: #0d1117; color: #c9d1d9; font-family: 'Cascadia Code', 'Fira Code', monospace; margin: 0; padding: 20px; }}
h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
.stats {{ display: flex; gap: 12px; margin: 16px 0; }}
.stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 20px; text-align: center; }}
.stat .num {{ font-size: 28px; font-weight: bold; }}
.stat .label {{ font-size: 11px; color: #8b949e; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 12px 0; }}
.card h2 {{ color: #58a6ff; margin-top: 0; font-size: 14px; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid #21262d; font-size: 12px; }}
th {{ color: #8b949e; }}
a {{ text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.btn {{ background: #238636; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-family: inherit; }}
.btn:hover {{ background: #2ea043; }}
pre {{ white-space: pre-wrap; font-size: 12px; margin: 0; }}
</style>
</head><body>
<h1>MailClaw Dashboard</h1>
<button class="btn" onclick="fetch('/trigger',{{method:'POST'}}).then(()=>location.reload())">Fetch Now</button>

<div class="stats">
    <div class="stat"><div class="num">{}</div><div class="label">Total Emails</div></div>
    <div class="stat"><div class="num" style="color:#f85149">{}</div><div class="label">HOT Jobs</div></div>
    <div class="stat"><div class="num" style="color:#d29922">{}</div><div class="label">WARM Jobs</div></div>
    <div class="stat"><div class="num" style="color:#484f58">{}</div><div class="label">COLD Jobs</div></div>
</div>

<div class="card">
<h2>Upwork Jobs</h2>
<table>
<tr><th>Rating</th><th>Title</th><th>Description</th><th>Match Reasons</th></tr>
{}
</table>
</div>

<div class="card">
<h2>Triage Summary</h2>
<pre>{}</pre>
</div>

<p style="color:#484f58;font-size:11px;">Last fetch: {} | Interval: {}s</p>
</body></html>"#,
        total_emails,
        hot_count,
        warm_count,
        cold_count,
        jobs_html,
        data.triage_summary.replace('<', "&lt;").replace('>', "&gt;"),
        data.fetched_at,
        FETCH_INTERVAL_SECS,
    );

    Html(html)
}

// ---------------------------------------------------------------------------
// Task handler
// ---------------------------------------------------------------------------

struct MailClawHandler;

#[async_trait]
impl TaskHandler for MailClawHandler {
    async fn handle(&self, _agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "fetch_emails" => {
                let data = fetch_all_mail().await;
                save_mailclaw_files(&data).await?;
                Ok(serde_json::json!({
                    "jobs_found": data.upwork_jobs.len(),
                    "hot": data.upwork_jobs.iter().filter(|j| j.rating == "HOT").count(),
                    "warm": data.upwork_jobs.iter().filter(|j| j.rating == "WARM").count(),
                    "summary": data.triage_summary,
                }))
            }
            other => anyhow::bail!("unknown task type: {}", other),
        }
    }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> Result<()> {
    let config = AgentConfig::from_env().context("failed to read agent config")?;
    let agent = OpenClawAgent::new(config);

    let state = MailClawState {
        agent: Arc::new(agent.clone()),
        data: Arc::new(RwLock::new(MailClawData::default())),
    };

    // Start background timers
    let timer_state = state.clone();
    tokio::spawn(async move {
        mailclaw_timer(timer_state).await;
    });

    // Start digest/wrap-up scheduler (6am + 6pm)
    let digest_state = state.clone();
    tokio::spawn(async move {
        digest_timer(digest_state).await;
    });

    let routes = Router::new()
        .route("/trigger", post(trigger_handler))
        .route("/data", get(data_handler))
        .route("/triage", get(triage_handler))
        .route("/jobs", get(jobs_handler))
        .route("/dashboard", get(dashboard_handler))
        .with_state(state);

    agent.run(MailClawHandler, routes).await
}
