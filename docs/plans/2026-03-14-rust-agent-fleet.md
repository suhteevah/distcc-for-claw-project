# OpenClaw Rust Agent Fleet — Full Rewrite Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite all 7 existing Python agents in Rust and add 2 new agents (legal-team, coder), creating a 9-agent Rust fleet with a shared SDK crate.

**Architecture:** Cargo workspace with a shared `openclaw-sdk` library crate and 9 binary crates (one per agent). Each agent is a thin axum HTTP server that registers with Core, polls for tasks via the SDK, dispatches to handler functions, and reports results. All LLM inference routes through Core's `/api/v1/llm/complete` endpoint — agents never talk to Ollama/llama.cpp directly.

**Tech Stack:** Rust 1.77+, axum 0.7, tokio, reqwest, serde/serde_json, tracing, metrics-exporter-prometheus. Multi-stage Docker build with `rust:1.77-slim` builder → `debian:bookworm-slim` runtime.

---

## Architecture Overview

```
openclaw-rust-agents/
├── Cargo.toml                    # Workspace root
├── Dockerfile                    # Multi-stage build for all agents
├── sdk/                          # openclaw-sdk library crate
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs                # AgentConfig, Task, LLMClient, HeartbeatReporter, OpenClawAgent
├── agents/
│   ├── seo-auditor/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── lead-responder/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── content-mill/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── proposal-gen/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── job-hunter/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── client-dashboard/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── wow-economy/
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── legal-team/              # NEW
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── coder/                   # NEW
│       ├── Cargo.toml
│       └── src/main.rs
├── .env.example
└── docker-compose.yml            # Updated with Rust services
```

## Core Protocol (What the SDK Implements)

The OpenClaw Core API that agents talk to:

```
POST /api/v1/agents/register        — Register agent (id, port, capabilities, max_concurrent, llm_tier)
GET  /api/v1/tasks/poll/{agent_id}  — Poll for tasks (204 = none, 200 = Task JSON)
POST /api/v1/tasks/{task_id}/complete — Report success (body: {result: {...}})
POST /api/v1/tasks/{task_id}/fail    — Report failure (body: {error: "..."})
POST /api/v1/agents/{id}/heartbeat   — Heartbeat (status, tasks_completed, tasks_in_progress, last_error, timestamp)
POST /api/v1/llm/complete            — LLM completion (prompt, tier, model, system, max_tokens, temperature, json_mode)
POST /api/v1/llm/chat                — Chat completion (messages, tier, model, max_tokens, temperature)
```

All requests carry `Authorization: Bearer {OPENCLAW_API_KEY}` header.

## Agent Port Assignments

| Agent | Port | Capabilities |
|-------|------|-------------|
| seo-auditor | 8001 | seo_audit, lighthouse_scan, keyword_research, competitor_analysis |
| lead-responder | 8002 | lead_classify, email_draft, upwork_respond, inbox_scan |
| content-mill | 8003 | blog_post, social_media, email_campaign, seo_content |
| proposal-gen | 8004 | upwork_proposal, consulting_sow, pricing |
| job-hunter | 8005 | job_scan, resume_match, cover_letter, application_track, upwork_submit |
| client-dashboard | 8006 | weekly_report, monthly_report, seo_tracking, client_health |
| wow-economy | 8007 | tsm_import, arbitrage_scan, crafting_profit, market_trend |
| legal-team | 8008 | contract_review, legal_draft, compliance_research, dispute_letter |
| coder | 8009 | code_review, code_generation, bug_fix, refactor, documentation |

## Environment Variables (Per Agent .env)

```ini
AGENT_ID=seo-auditor
AGENT_PORT=8001
AGENT_CAPABILITIES=seo_audit,lighthouse_scan,keyword_research,competitor_analysis
LLM_TIER=heavy
MAX_CONCURRENT_TASKS=2
LOG_LEVEL=verbose
```

Global `.env` (already exists, shared):
```ini
OPENCLAW_API_KEY=openclaw-fleet-key-2026
OPENCLAW_API_URL=http://core:9000
LLM_BACKEND_TYPE=openai
LLM_MODEL_HEAVY=gemini-2.5-flash
LLM_API_KEY_HEAVY=AIzaSy...
POSTGRES_DB=openclaw
POSTGRES_USER=openclaw
POSTGRES_PASSWORD=openclaw2026cnc
REDIS_URL=redis://redis:6379/0
```

---

## Task 1: Scaffold Cargo Workspace + SDK Crate

**Files:**
- Create: `openclaw-rust-agents/Cargo.toml` (workspace root)
- Create: `openclaw-rust-agents/sdk/Cargo.toml`
- Create: `openclaw-rust-agents/sdk/src/lib.rs`

**Step 1: Create workspace root Cargo.toml**

```toml
[workspace]
resolver = "2"
members = [
    "sdk",
    "agents/seo-auditor",
    "agents/lead-responder",
    "agents/content-mill",
    "agents/proposal-gen",
    "agents/job-hunter",
    "agents/client-dashboard",
    "agents/wow-economy",
    "agents/legal-team",
    "agents/coder",
]

[workspace.dependencies]
openclaw-sdk = { path = "sdk" }
axum = "0.7"
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
metrics = "0.23"
metrics-exporter-prometheus = "0.15"
chrono = { version = "0.4", features = ["serde"] }
anyhow = "1"
thiserror = "1"
```

**Step 2: Create SDK crate Cargo.toml**

```toml
[package]
name = "openclaw-sdk"
version = "1.0.0"
edition = "2021"

[dependencies]
axum = { workspace = true }
tokio = { workspace = true }
reqwest = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
tracing = { workspace = true }
chrono = { workspace = true }
anyhow = { workspace = true }
thiserror = { workspace = true }
metrics = { workspace = true }
metrics-exporter-prometheus = { workspace = true }
```

**Step 3: Implement SDK lib.rs**

The SDK must implement these types/traits:
- `AgentConfig` — reads from env vars
- `Task` — deserializes from Core JSON
- `LlmClient` — sends completion/chat requests to Core
- `HeartbeatReporter` — background tokio task, 30s interval
- `OpenClawAgent` — main struct: register(), poll_task(), complete_task(), fail_task(), run_loop()
- `build_app()` — helper that creates axum Router with /health, /metrics, / endpoints
- `TaskHandler` trait — `async fn handle(&self, agent: &OpenClawAgent, task: Task) -> Result<serde_json::Value>`

```rust
// sdk/src/lib.rs — Full implementation

use anyhow::{Context, Result};
use axum::{extract::State, routing::get, Json, Router};
use chrono::Utc;
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing::{debug, error, info, warn};

// ═══════════════════════════════════════
// Configuration
// ═══════════════════════════════════════

#[derive(Debug, Clone)]
pub struct AgentConfig {
    pub agent_id: String,
    pub agent_port: u16,
    pub capabilities: Vec<String>,
    pub core_url: String,
    pub api_key: String,
    pub heartbeat_interval_secs: u64,
    pub max_concurrent: u32,
    pub log_level: String,
    pub llm_tier: String,
}

impl AgentConfig {
    pub fn from_env() -> Self {
        Self {
            agent_id: std::env::var("AGENT_ID").unwrap_or_else(|_| "unknown".into()),
            agent_port: std::env::var("AGENT_PORT")
                .unwrap_or_else(|_| "8000".into())
                .parse()
                .unwrap_or(8000),
            capabilities: std::env::var("AGENT_CAPABILITIES")
                .unwrap_or_default()
                .split(',')
                .filter(|s| !s.is_empty())
                .map(String::from)
                .collect(),
            core_url: std::env::var("OPENCLAW_API_URL")
                .unwrap_or_else(|_| "http://core:9000".into()),
            api_key: std::env::var("OPENCLAW_API_KEY").unwrap_or_default(),
            heartbeat_interval_secs: std::env::var("HEARTBEAT_INTERVAL")
                .unwrap_or_else(|_| "30".into())
                .parse()
                .unwrap_or(30),
            max_concurrent: std::env::var("MAX_CONCURRENT_TASKS")
                .unwrap_or_else(|_| "2".into())
                .parse()
                .unwrap_or(2),
            log_level: std::env::var("LOG_LEVEL").unwrap_or_else(|_| "info".into()),
            llm_tier: std::env::var("LLM_TIER").unwrap_or_else(|_| "fast".into()),
        }
    }
}

// ═══════════════════════════════════════
// Task Model
// ═══════════════════════════════════════

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub agent_id: String,
    pub task_type: String,
    pub payload: serde_json::Value,
    #[serde(default = "default_priority")]
    pub priority: String,
    #[serde(default = "default_status")]
    pub status: String,
    #[serde(default)]
    pub created_at: String,
    pub result: Option<serde_json::Value>,
    pub error: Option<String>,
}

fn default_priority() -> String { "normal".into() }
fn default_status() -> String { "pending".into() }

// ═══════════════════════════════════════
// LLM Client
// ═══════════════════════════════════════

#[derive(Clone)]
pub struct LlmClient {
    http: Client,
    core_url: String,
    api_key: String,
    default_tier: String,
}

#[derive(Debug, Serialize)]
struct LlmRequest {
    prompt: String,
    tier: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    model: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    system: Option<String>,
    max_tokens: u32,
    temperature: f32,
    json_mode: bool,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct LlmResponse {
    pub text: String,
    #[serde(default)]
    pub tokens_used: u64,
    #[serde(default)]
    pub model: String,
    #[serde(default)]
    pub backend: String,
}

impl LlmClient {
    pub fn new(core_url: &str, api_key: &str, default_tier: &str) -> Self {
        Self {
            http: Client::builder()
                .timeout(std::time::Duration::from_secs(300))
                .build()
                .expect("failed to build HTTP client"),
            core_url: core_url.to_string(),
            api_key: api_key.to_string(),
            default_tier: default_tier.to_string(),
        }
    }

    pub async fn complete(
        &self,
        prompt: &str,
        tier: Option<&str>,
        system: Option<&str>,
        max_tokens: u32,
        temperature: f32,
        json_mode: bool,
    ) -> Result<LlmResponse> {
        let req = LlmRequest {
            prompt: prompt.to_string(),
            tier: tier.unwrap_or(&self.default_tier).to_string(),
            model: None,
            system: system.map(String::from),
            max_tokens,
            temperature,
            json_mode,
        };

        info!(tier = %req.tier, max_tokens, "LLM completion request");

        let resp = self.http
            .post(format!("{}/api/v1/llm/complete", self.core_url))
            .header("Authorization", format!("Bearer {}", self.api_key))
            .json(&req)
            .send()
            .await
            .context("LLM request failed")?;

        let status = resp.status();
        if !status.is_success() {
            let body = resp.text().await.unwrap_or_default();
            anyhow::bail!("LLM HTTP {status}: {body}");
        }

        let data: LlmResponse = resp.json().await.context("Failed to parse LLM response")?;
        info!(tokens_used = data.tokens_used, backend = %data.backend, "LLM response received");
        Ok(data)
    }
}

// ═══════════════════════════════════════
// Heartbeat Reporter
// ═══════════════════════════════════════

#[derive(Debug, Default)]
pub struct AgentStats {
    pub tasks_completed: u64,
    pub tasks_in_progress: u64,
    pub last_error: Option<String>,
}

pub type SharedStats = Arc<Mutex<AgentStats>>;

fn spawn_heartbeat(
    http: Client,
    core_url: String,
    api_key: String,
    agent_id: String,
    interval_secs: u64,
    stats: SharedStats,
) {
    tokio::spawn(async move {
        let mut interval = tokio::time::interval(
            std::time::Duration::from_secs(interval_secs),
        );
        loop {
            interval.tick().await;
            let s = stats.lock().await;
            let payload = serde_json::json!({
                "status": "healthy",
                "tasks_completed": s.tasks_completed,
                "tasks_in_progress": s.tasks_in_progress,
                "last_error": s.last_error,
                "timestamp": Utc::now().to_rfc3339(),
            });
            drop(s);

            match http
                .post(format!("{}/api/v1/agents/{}/heartbeat", core_url, agent_id))
                .header("Authorization", format!("Bearer {}", api_key))
                .json(&payload)
                .send()
                .await
            {
                Ok(_) => debug!("heartbeat sent"),
                Err(e) => warn!("heartbeat failed: {e}"),
            }
        }
    });
}

// ═══════════════════════════════════════
// Task Handler Trait
// ═══════════════════════════════════════

#[async_trait::async_trait]
pub trait TaskHandler: Send + Sync + 'static {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value>;
}

// ═══════════════════════════════════════
// Main Agent
// ═══════════════════════════════════════

#[derive(Clone)]
pub struct OpenClawAgent {
    pub config: AgentConfig,
    pub llm: LlmClient,
    pub stats: SharedStats,
    http: Client,
}

impl OpenClawAgent {
    pub fn new(config: AgentConfig) -> Self {
        let http = Client::builder()
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .expect("failed to build HTTP client");

        let llm = LlmClient::new(&config.core_url, &config.api_key, &config.llm_tier);
        let stats = Arc::new(Mutex::new(AgentStats::default()));

        Self { config, llm, stats, http }
    }

    pub async fn register(&self) -> Result<()> {
        let payload = serde_json::json!({
            "agent_id": self.config.agent_id,
            "port": self.config.agent_port,
            "capabilities": self.config.capabilities,
            "max_concurrent": self.config.max_concurrent,
            "llm_tier": self.config.llm_tier,
        });

        match self.http
            .post(format!("{}/api/v1/agents/register", self.config.core_url))
            .header("Authorization", format!("Bearer {}", self.config.api_key))
            .json(&payload)
            .send()
            .await
        {
            Ok(resp) if resp.status().is_success() => {
                info!("registered with Core");
                Ok(())
            }
            Ok(resp) => {
                warn!("registration returned {}, running standalone", resp.status());
                Ok(())
            }
            Err(e) => {
                warn!("registration failed: {e}, running standalone");
                Ok(())
            }
        }
    }

    pub async fn poll_task(&self) -> Option<Task> {
        match self.http
            .get(format!(
                "{}/api/v1/tasks/poll/{}",
                self.config.core_url, self.config.agent_id
            ))
            .header("Authorization", format!("Bearer {}", self.config.api_key))
            .send()
            .await
        {
            Ok(resp) if resp.status().as_u16() == 204 => None,
            Ok(resp) if resp.status().is_success() => {
                match resp.json::<Task>().await {
                    Ok(task) => {
                        info!(task_id = %task.id, task_type = %task.task_type, "task received");
                        let mut s = self.stats.lock().await;
                        s.tasks_in_progress += 1;
                        Some(task)
                    }
                    Err(e) => {
                        error!("failed to parse task: {e}");
                        None
                    }
                }
            }
            _ => None,
        }
    }

    pub async fn complete_task(&self, task_id: &str, result: serde_json::Value) -> Result<()> {
        self.http
            .post(format!(
                "{}/api/v1/tasks/{}/complete",
                self.config.core_url, task_id
            ))
            .header("Authorization", format!("Bearer {}", self.config.api_key))
            .json(&serde_json::json!({ "result": result }))
            .send()
            .await
            .context("failed to report task completion")?;

        let mut s = self.stats.lock().await;
        s.tasks_completed += 1;
        s.tasks_in_progress = s.tasks_in_progress.saturating_sub(1);
        info!(task_id, total = s.tasks_completed, "task completed");
        Ok(())
    }

    pub async fn fail_task(&self, task_id: &str, error: &str) -> Result<()> {
        self.http
            .post(format!(
                "{}/api/v1/tasks/{}/fail",
                self.config.core_url, task_id
            ))
            .header("Authorization", format!("Bearer {}", self.config.api_key))
            .json(&serde_json::json!({ "error": error }))
            .send()
            .await
            .context("failed to report task failure")?;

        let mut s = self.stats.lock().await;
        s.tasks_in_progress = s.tasks_in_progress.saturating_sub(1);
        s.last_error = Some(error.to_string());
        error!(task_id, error, "task failed");
        Ok(())
    }

    /// Start the agent: register, heartbeat, task loop, HTTP server.
    pub async fn run<H: TaskHandler>(self, handler: H, extra_routes: Router) -> Result<()> {
        // Init tracing
        tracing_subscriber::fmt()
            .with_env_filter(
                tracing_subscriber::EnvFilter::try_from_default_env()
                    .unwrap_or_else(|_| format!("{}=debug,tower_http=info", self.config.agent_id.replace('-', "_")).into()),
            )
            .json()
            .init();

        info!(
            agent_id = %self.config.agent_id,
            port = self.config.agent_port,
            capabilities = ?self.config.capabilities,
            "starting agent"
        );

        // Register with Core
        self.register().await?;

        // Start heartbeat
        spawn_heartbeat(
            self.http.clone(),
            self.config.core_url.clone(),
            self.config.api_key.clone(),
            self.config.agent_id.clone(),
            self.config.heartbeat_interval_secs,
            self.stats.clone(),
        );

        // Build HTTP server
        let agent_for_health = self.clone();
        let health_route = get(move || {
            let a = agent_for_health.clone();
            async move {
                let s = a.stats.lock().await;
                Json(serde_json::json!({
                    "agent_id": a.config.agent_id,
                    "status": "healthy",
                    "tasks_completed": s.tasks_completed,
                    "tasks_in_progress": s.tasks_in_progress,
                }))
            }
        });

        let agent_id = self.config.agent_id.clone();
        let root_route = get(move || async move {
            Json(serde_json::json!({
                "agent": agent_id,
                "version": "1.0.0",
                "docs": "/health",
            }))
        });

        // Prometheus metrics
        let metrics_route = get(|| async {
            // Render prometheus metrics
            let handle = metrics_exporter_prometheus::PrometheusBuilder::new()
                .build_recorder();
            // Simplified — real impl uses global recorder
            "# HELP openclaw_agent Agent metrics\n"
        });

        let app = Router::new()
            .route("/health", health_route)
            .route("/", root_route)
            .route("/metrics", metrics_route)
            .merge(extra_routes);

        let port = self.config.agent_port;
        let handler = Arc::new(handler);

        // Spawn task polling loop
        let agent_loop = self.clone();
        let handler_loop = handler.clone();
        tokio::spawn(async move {
            loop {
                match agent_loop.poll_task().await {
                    Some(task) => {
                        let task_id = task.id.clone();
                        match handler_loop.handle(&agent_loop, &task).await {
                            Ok(result) => {
                                let _ = agent_loop.complete_task(&task_id, result).await;
                            }
                            Err(e) => {
                                let _ = agent_loop.fail_task(&task_id, &e.to_string()).await;
                            }
                        }
                    }
                    None => tokio::time::sleep(std::time::Duration::from_secs(2)).await,
                }
            }
        });

        // Start HTTP server
        let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{port}"))
            .await
            .context("failed to bind")?;
        info!(port, "HTTP server listening");
        axum::serve(listener, app).await.context("server error")?;

        Ok(())
    }
}
```

**Step 4: Verify it compiles**

```bash
cd openclaw-rust-agents && cargo check -p openclaw-sdk
```

**Step 5: Commit**

```bash
git add -A && git commit -m "feat: scaffold Cargo workspace with openclaw-sdk crate"
```

---

## Task 2: Create First Agent — seo-auditor (Port 8001)

**Files:**
- Create: `openclaw-rust-agents/agents/seo-auditor/Cargo.toml`
- Create: `openclaw-rust-agents/agents/seo-auditor/src/main.rs`

This is the template agent — once this works, all others follow the same pattern.

**Step 1: Create agent Cargo.toml**

```toml
[package]
name = "seo-auditor"
version = "1.0.0"
edition = "2021"

[dependencies]
openclaw-sdk = { workspace = true }
axum = { workspace = true }
tokio = { workspace = true }
reqwest = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
tracing = { workspace = true }
tracing-subscriber = { workspace = true }
chrono = { workspace = true }
anyhow = { workspace = true }
async-trait = "0.1"
scraper = "0.20"          # HTML parsing (replaces BeautifulSoup)
```

**Step 2: Implement main.rs**

Port the Python seo-auditor logic:
- `fetch_page(url)` — uses reqwest + scraper crate for HTML parsing
- `score_page(page_data)` — same scoring algorithm as Python
- `generate_analysis(agent, page_data, score, issues)` — calls agent.llm.complete()
- `SeoHandler` impl TaskHandler — dispatches seo_audit tasks
- Direct API: `POST /audit` endpoint via axum

The handler struct:

```rust
use openclaw_sdk::{OpenClawAgent, Task, TaskHandler};
use anyhow::Result;
use axum::{routing::post, Json, Router};
use serde::{Deserialize, Serialize};

struct SeoHandler;

#[async_trait::async_trait]
impl TaskHandler for SeoHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        let url = task.payload.get("url")
            .and_then(|v| v.as_str())
            .ok_or_else(|| anyhow::anyhow!("missing 'url' in payload"))?;

        let page_data = fetch_page(url).await?;
        let (score, issues) = score_page(&page_data);
        let analysis = generate_analysis(agent, &page_data, score, &issues).await?;

        Ok(serde_json::json!({
            "url": url,
            "score": score,
            "summary": analysis,
            "page_data": page_data,
            "issues": issues,
            "recommendations": build_recommendations(&issues),
            "audited_at": chrono::Utc::now().to_rfc3339(),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    let config = openclaw_sdk::AgentConfig::from_env();
    let agent = OpenClawAgent::new(config);

    let routes = Router::new()
        .route("/audit", post(audit_handler));

    agent.run(SeoHandler, routes).await
}
```

Port `fetch_page` using `scraper` crate instead of BeautifulSoup:
- Parse title, meta description, H1s, H2s, images, links, canonical, robots, OG tags, schema.org
- Count images missing alt, internal vs external links, word count

Port `score_page` — identical scoring algorithm (100 - penalties).

Port `generate_analysis` — same LLM prompt, call `agent.llm.complete()`.

**Step 3: Verify it compiles**

```bash
cargo check -p seo-auditor
```

**Step 4: Commit**

```bash
git add agents/seo-auditor/ && git commit -m "feat: port seo-auditor agent to Rust"
```

---

## Task 3: Port lead-responder (Port 8002)

**Files:**
- Create: `agents/lead-responder/Cargo.toml`
- Create: `agents/lead-responder/src/main.rs`

**Key differences from seo-auditor:**
- Has helper modules (classifier, drafter, scorer, gmail) — inline them in Rust
- In-memory approval queue (`DashMap` or `Arc<Mutex<HashMap>>`)
- Gmail integration via IMAP (use `async-imap` + `lettre` crates for IMAP/SMTP)
- Upwork job scoring
- Multiple task types: lead_classify, email_draft, upwork_respond, inbox_scan

**Extra dependencies:**
```toml
async-imap = "0.9"    # IMAP client
lettre = "0.11"        # SMTP client
dashmap = "6"          # Concurrent HashMap for approval queue
```

Port all 4 task handlers:
- `_handle_classify` → LLM-based lead classification
- `_handle_email_draft` → classify + draft + Gmail draft creation + approval queue
- `_handle_upwork_respond` → draft Upwork response + approval queue
- `_handle_inbox_scan` → list unread, classify each, score Upwork jobs, draft real leads

Direct API endpoints: `/classify`, `/draft`, `/upwork`, `/scan`, `/leads/pending`, `/leads/approve/{id}`, `/leads/reject/{id}`, `/jobs/viable`, `/jobs/score`

**Commit:** `feat: port lead-responder agent to Rust`

---

## Task 4: Port content-mill (Port 8003)

**Files:**
- Create: `agents/content-mill/Cargo.toml`
- Create: `agents/content-mill/src/main.rs`

Straightforward LLM-heavy agent. 4 task types:
- blog_post → generate_blog_post() (heavy tier, 8192 tokens, temp 0.6)
- social_media → generate_social_media() (fast tier, json_mode)
- email_campaign → generate_email_campaign() (heavy tier, json_mode)
- seo_content → generate_seo_content() (heavy tier)

Port all prompts exactly. Handle the `---META---` separator for blog posts.

**Commit:** `feat: port content-mill agent to Rust`

---

## Task 5: Port proposal-gen (Port 8004)

**Files:**
- Create: `agents/proposal-gen/Cargo.toml`
- Create: `agents/proposal-gen/src/main.rs`

Has helper modules: portfolio.rs, pricing.rs, proposal.rs, sow.rs — inline in Rust.

3 task types: upwork_proposal, consulting_sow, pricing

Portfolio context and SERVICE_CATEGORIES are static data — define as `const` or `lazy_static`.

Pricing calculation is pure math (no LLM) — straightforward port.

**Commit:** `feat: port proposal-gen agent to Rust`

---

## Task 6: Port job-hunter (Port 8005)

**Files:**
- Create: `agents/job-hunter/Cargo.toml`
- Create: `agents/job-hunter/src/main.rs`

**Special case:** Uses Playwright for browser automation.

**Options:**
1. **chromiumoxide** crate (Rust CDP client) — headless Chrome control
2. **fantoccini** crate (WebDriver client)
3. Shell out to `playwright` CLI

Recommend **chromiumoxide** — native Rust, async, CDP protocol. Add Chrome/Chromium to Dockerfile.

Task types: upwork_submit, upwork_bulk_submit, check_login

Submission tracking via in-memory Vec.

**Extra dependencies:**
```toml
chromiumoxide = { version = "0.7", features = ["tokio-runtime"] }
```

**Commit:** `feat: port job-hunter agent to Rust`

---

## Task 7: Port client-dashboard (Port 8006)

**Files:**
- Create: `agents/client-dashboard/Cargo.toml`
- Create: `agents/client-dashboard/src/main.rs`

In-memory client store + report list. 4 task types:
- weekly_report, monthly_report → LLM generation
- client_health → pure data query
- seo_tracking → calls seo-auditor's `/audit` endpoint via HTTP

Cross-agent HTTP call pattern: `reqwest::Client::post("http://openclaw-seo-auditor:8001/audit")`

**Commit:** `feat: port client-dashboard agent to Rust`

---

## Task 8: Port wow-economy (Port 8007)

**Files:**
- Create: `agents/wow-economy/Cargo.toml`
- Create: `agents/wow-economy/src/main.rs`

4 task types: tsm_import, arbitrage_scan, crafting_profit, market_trend

Uses PostgreSQL — add `sqlx` dependency:
```toml
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres", "chrono"] }
```

**Commit:** `feat: port wow-economy agent to Rust`

---

## Task 9: Build NEW legal-team Agent (Port 8008)

**Files:**
- Create: `agents/legal-team/Cargo.toml`
- Create: `agents/legal-team/src/main.rs`

**Capabilities:** contract_review, legal_draft, compliance_research, dispute_letter

**Task handlers:**

1. `contract_review` — Takes contract text, uses LLM to identify risks, missing clauses, unfavorable terms. Returns structured analysis with severity ratings.

2. `legal_draft` — Takes parameters (type: NDA/service_agreement/freelance_contract, parties, terms), generates draft legal document using LLM with legal system prompt.

3. `compliance_research` — Takes business type + jurisdiction, uses LLM to research applicable regulations, licenses, requirements.

4. `dispute_letter` — Takes dispute context (amount, counterparty, issue), generates professional dispute/collections letter.

All use LLM tier: `heavy` (needs reasoning).

**System prompt pattern:**
```
You are a legal assistant for Ridge Cell Repair LLC. You provide legal document drafts
and analysis for review by qualified counsel. Always include a disclaimer that output
is not legal advice and should be reviewed by an attorney.
```

**Direct API:** `/review`, `/draft`, `/compliance`, `/dispute`

**Commit:** `feat: add legal-team agent (new)`

---

## Task 10: Build NEW coder Agent (Port 8009)

**Files:**
- Create: `agents/coder/Cargo.toml`
- Create: `agents/coder/src/main.rs`

**Capabilities:** code_review, code_generation, bug_fix, refactor, documentation

**Task handlers:**

1. `code_review` — Takes code + language, returns structured review (bugs, security issues, style, suggestions) with severity.

2. `code_generation` — Takes spec/description + language + constraints, generates code with tests.

3. `bug_fix` — Takes buggy code + error/description, returns fixed code with explanation.

4. `refactor` — Takes code + goals (performance/readability/DRY), returns refactored code.

5. `documentation` — Takes code, generates doc comments, README sections, API docs.

All use LLM tier: `heavy`.

**System prompt pattern:**
```
You are an expert software engineer. Write clean, idiomatic code. Prefer Rust, C,
and low-level languages. Follow YAGNI and DRY principles. Include error handling.
All code must compile and include tests.
```

**Direct API:** `/review`, `/generate`, `/fix`, `/refactor`, `/docs`

**Commit:** `feat: add coder agent (new)`

---

## Task 11: Dockerfile — Multi-Stage Build

**Files:**
- Create: `openclaw-rust-agents/Dockerfile`

```dockerfile
# ══════════════════════════════════════════
# Stage 1: Build all agents
# ══════════════════════════════════════════
FROM rust:1.77-slim-bookworm AS builder

RUN apt-get update && apt-get install -y \
    pkg-config libssl-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY Cargo.toml Cargo.lock ./
COPY sdk/ sdk/
COPY agents/ agents/

# Build all binaries in release mode
RUN cargo build --release --workspace

# ══════════════════════════════════════════
# Stage 2: Runtime (one image per agent via build arg)
# ══════════════════════════════════════════
FROM debian:bookworm-slim AS runtime

ARG AGENT_NAME
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/target/release/${AGENT_NAME} /usr/local/bin/agent

EXPOSE 8000
CMD ["/usr/local/bin/agent"]
```

Usage in compose: `build: { args: { AGENT_NAME: seo-auditor } }`

**Commit:** `feat: add multi-stage Dockerfile for Rust agents`

---

## Task 12: Update docker-compose.yml

**Files:**
- Modify: `docker-compose.yml` on CNC-Server

Replace all 7 Python agent service blocks with Rust equivalents. Add 2 new agents. Each service:

```yaml
seo-auditor:
  build:
    context: ../openclaw-rust-agents  # or wherever the Rust workspace lives
    dockerfile: Dockerfile
    args:
      AGENT_NAME: seo-auditor
  container_name: openclaw-seo-auditor
  restart: unless-stopped
  dns: [8.8.8.8, 1.1.1.1]
  ports: ["8001:8001"]
  env_file:
    - .env
    - ./agents/seo-auditor/.env
  depends_on:
    core:
      condition: service_healthy
  volumes:
    - agent-outputs:/outputs
  logging:
    driver: "json-file"
    options: { max-size: "50m", max-file: "3" }
```

Add legal-team (8008) and coder (8009) service blocks.

**Special cases:**
- job-hunter: needs `chromium` in runtime image, `mem_limit: 1g`, browser data volume
- wow-economy: needs `DATABASE_URL` env var

**Commit:** `feat: update docker-compose for Rust agent fleet`

---

## Task 13: Deploy + Rolling Migration

**Step 1: SCP Rust workspace to CNC-Server**
```bash
scp -r openclaw-rust-agents/ root@192.168.168.100:/opt/openclaw/
```

**Step 2: Build all agents on CNC-Server**
```bash
ssh root@192.168.168.100 'cd /opt/openclaw/openclaw-rust-agents && podman compose build'
```

**Step 3: Rolling deploy — one agent at a time**
```bash
# Stop Python agent, start Rust agent
docker compose stop seo-auditor
docker compose up -d seo-auditor  # Now using Rust build
curl http://localhost:8001/health   # Verify

# Repeat for each agent...
```

**Step 4: Verify all 9 agents healthy**
```bash
for port in 8001 8002 8003 8004 8005 8006 8007 8008 8009; do
  echo -n "Port $port: "
  curl -s http://localhost:$port/health | jq -r '.status'
done
```

**Step 5: Monitor Core registration**
```bash
curl http://localhost:9000/api/v1/status | jq '.agents'
```

**Commit:** `feat: deploy Rust agent fleet to CNC-Server`

---

## Task 14: Cleanup

- Remove Python agent directories (backup first)
- Update MEMORY.md with new Rust architecture
- Verify Prometheus scraping works with new `/metrics` endpoints
- Run a test task through each agent via Core API

---

## Rollback Plan

If any Rust agent fails in production:
1. `docker compose stop {agent}`
2. Restore Python Dockerfile reference in compose
3. `docker compose up -d {agent}`

Python source remains on disk until full verification period (7 days).

---

## Size Comparison (Expected)

| | Python (per agent) | Rust (per agent) |
|---|---|---|
| Docker image | ~200MB | ~15MB |
| RAM at idle | ~80MB | ~5MB |
| Startup time | ~3s | <100ms |
| Total fleet (9) | ~1.8GB images, ~720MB RAM | ~135MB images, ~45MB RAM |

This matters on CNC-Server (8GB RAM total, also running GTX 980 rpc-server + gateway).
