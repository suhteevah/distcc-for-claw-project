use std::sync::Arc;
use std::time::Duration;

use anyhow::{Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::get,
    Router,
};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;
use tracing::{error, info, warn};

// ---------------------------------------------------------------------------
// AgentConfig
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
pub struct AgentConfig {
    pub agent_id: String,
    pub port: u16,
    pub capabilities: Vec<String>,
    pub core_url: String,
    pub api_key: String,
    pub heartbeat_interval: u64,
    pub max_concurrent_tasks: usize,
    pub log_level: String,
    pub llm_tier: String,
}

impl AgentConfig {
    /// Read all configuration from environment variables.
    pub fn from_env() -> Result<Self> {
        let agent_id = std::env::var("AGENT_ID")
            .context("AGENT_ID env var required")?;
        let port = std::env::var("AGENT_PORT")
            .unwrap_or_else(|_| "8080".to_string())
            .parse::<u16>()
            .context("AGENT_PORT must be a valid port number")?;
        let capabilities = std::env::var("AGENT_CAPABILITIES")
            .unwrap_or_default()
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();
        let core_url = std::env::var("OPENCLAW_API_URL")
            .unwrap_or_else(|_| "http://localhost:8000".to_string());
        let api_key = std::env::var("OPENCLAW_API_KEY")
            .unwrap_or_default();
        let heartbeat_interval = std::env::var("HEARTBEAT_INTERVAL")
            .unwrap_or_else(|_| "30".to_string())
            .parse::<u64>()
            .context("HEARTBEAT_INTERVAL must be a number")?;
        let max_concurrent_tasks = std::env::var("MAX_CONCURRENT_TASKS")
            .unwrap_or_else(|_| "1".to_string())
            .parse::<usize>()
            .context("MAX_CONCURRENT_TASKS must be a number")?;
        let log_level = std::env::var("LOG_LEVEL")
            .unwrap_or_else(|_| "info".to_string());
        let llm_tier = std::env::var("LLM_TIER")
            .unwrap_or_else(|_| "standard".to_string());

        Ok(Self {
            agent_id,
            port,
            capabilities,
            core_url,
            api_key,
            heartbeat_interval,
            max_concurrent_tasks,
            log_level,
            llm_tier,
        })
    }
}

// ---------------------------------------------------------------------------
// Task
// ---------------------------------------------------------------------------

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
    #[serde(default)]
    pub result: Option<serde_json::Value>,
    #[serde(default)]
    pub error: Option<String>,
}

fn default_priority() -> String { "normal".into() }
fn default_status() -> String { "pending".into() }

// ---------------------------------------------------------------------------
// LlmClient
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LlmResponse {
    pub text: String,
    pub tokens_used: u32,
    pub model: String,
    pub backend: String,
}

#[derive(Debug, Clone, Serialize)]
struct LlmCompleteRequest {
    prompt: String,
    tier: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    system: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    max_tokens: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    temperature: Option<f32>,
    #[serde(default)]
    json_mode: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct ChatMessage {
    pub role: String,
    pub content: String,
}

#[derive(Debug, Clone, Serialize)]
struct LlmChatRequest {
    messages: Vec<ChatMessage>,
    tier: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    max_tokens: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    temperature: Option<f32>,
}

#[derive(Clone)]
pub struct LlmClient {
    http: reqwest::Client,
    core_url: String,
    api_key: String,
    default_tier: String,
}

impl LlmClient {
    fn new(core_url: &str, api_key: &str, default_tier: &str) -> Self {
        let http = reqwest::Client::builder()
            .timeout(Duration::from_secs(300))
            .build()
            .expect("failed to build LLM HTTP client");
        Self {
            http,
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
        max_tokens: Option<u32>,
        temperature: Option<f32>,
        json_mode: bool,
    ) -> Result<LlmResponse> {
        let body = LlmCompleteRequest {
            prompt: prompt.to_string(),
            tier: tier.unwrap_or(&self.default_tier).to_string(),
            system: system.map(|s| s.to_string()),
            max_tokens,
            temperature,
            json_mode,
        };

        let resp = self
            .http
            .post(format!("{}/api/v1/llm/complete", self.core_url))
            .bearer_auth(&self.api_key)
            .json(&body)
            .send()
            .await
            .context("LLM complete request failed")?;

        let status = resp.status();
        if !status.is_success() {
            let text = resp.text().await.unwrap_or_default();
            anyhow::bail!("LLM complete returned {}: {}", status, text);
        }

        resp.json::<LlmResponse>()
            .await
            .context("failed to parse LLM response")
    }

    pub async fn chat(
        &self,
        messages: Vec<ChatMessage>,
        tier: Option<&str>,
        max_tokens: Option<u32>,
        temperature: Option<f32>,
    ) -> Result<LlmResponse> {
        let body = LlmChatRequest {
            messages,
            tier: tier.unwrap_or(&self.default_tier).to_string(),
            max_tokens,
            temperature,
        };

        let resp = self
            .http
            .post(format!("{}/api/v1/llm/complete", self.core_url))
            .bearer_auth(&self.api_key)
            .json(&body)
            .send()
            .await
            .context("LLM chat request failed")?;

        let status = resp.status();
        if !status.is_success() {
            let text = resp.text().await.unwrap_or_default();
            anyhow::bail!("LLM chat returned {}: {}", status, text);
        }

        resp.json::<LlmResponse>()
            .await
            .context("failed to parse LLM chat response")
    }
}

// ---------------------------------------------------------------------------
// AgentStats
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Default, Serialize)]
pub struct AgentStats {
    pub tasks_completed: u64,
    pub tasks_in_progress: u64,
    pub last_error: Option<String>,
}

pub type SharedStats = Arc<Mutex<AgentStats>>;

// ---------------------------------------------------------------------------
// TaskHandler trait
// ---------------------------------------------------------------------------

#[async_trait::async_trait]
pub trait TaskHandler: Send + Sync + 'static {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value>;
}

// ---------------------------------------------------------------------------
// OpenClawAgent
// ---------------------------------------------------------------------------

#[derive(Clone)]
pub struct OpenClawAgent {
    pub config: AgentConfig,
    pub llm: LlmClient,
    pub stats: SharedStats,
    http: reqwest::Client,
}

impl OpenClawAgent {
    pub fn new(config: AgentConfig) -> Self {
        let llm = LlmClient::new(&config.core_url, &config.api_key, &config.llm_tier);
        let http = reqwest::Client::builder()
            .timeout(Duration::from_secs(30))
            .build()
            .expect("failed to build HTTP client");
        Self {
            config,
            llm,
            stats: Arc::new(Mutex::new(AgentStats::default())),
            http,
        }
    }

    /// Register this agent with the Core API.
    pub async fn register(&self) -> Result<()> {
        let body = serde_json::json!({
            "agent_id": self.config.agent_id,
            "capabilities": self.config.capabilities,
            "port": self.config.port,
            "max_concurrent": self.config.max_concurrent_tasks,
            "llm_tier": self.config.llm_tier,
        });

        let resp = self
            .http
            .post(format!("{}/api/v1/agents/register", self.config.core_url))
            .bearer_auth(&self.config.api_key)
            .json(&body)
            .send()
            .await
            .context("registration request failed")?;

        if !resp.status().is_success() {
            let text = resp.text().await.unwrap_or_default();
            anyhow::bail!("registration returned error: {}", text);
        }

        info!(agent_id = %self.config.agent_id, "registered with Core");
        Ok(())
    }

    /// Poll Core for a pending task. Returns None on 204 or any error.
    pub async fn poll_task(&self) -> Option<Task> {
        let url = format!(
            "{}/api/v1/tasks/poll/{}",
            self.config.core_url, self.config.agent_id
        );

        match self.http.get(&url).bearer_auth(&self.config.api_key).send().await {
            Ok(resp) => {
                if resp.status() == StatusCode::NO_CONTENT {
                    return None;
                }
                if !resp.status().is_success() {
                    warn!(status = %resp.status(), "poll_task non-success status");
                    return None;
                }
                match resp.json::<Task>().await {
                    Ok(task) => Some(task),
                    Err(e) => {
                        warn!(error = %e, "failed to parse polled task");
                        None
                    }
                }
            }
            Err(e) => {
                warn!(error = %e, "poll_task request failed");
                None
            }
        }
    }

    /// Report a task as completed.
    pub async fn complete_task(&self, task_id: &str, result: serde_json::Value) -> Result<()> {
        let body = serde_json::json!({ "result": result });
        self.http
            .post(format!(
                "{}/api/v1/tasks/{}/complete",
                self.config.core_url, task_id
            ))
            .bearer_auth(&self.config.api_key)
            .json(&body)
            .send()
            .await
            .context("complete_task request failed")?;
        Ok(())
    }

    /// Report a task as failed.
    pub async fn fail_task(&self, task_id: &str, error: &str) -> Result<()> {
        let body = serde_json::json!({ "error": error });
        self.http
            .post(format!(
                "{}/api/v1/tasks/{}/fail",
                self.config.core_url, task_id
            ))
            .bearer_auth(&self.config.api_key)
            .json(&body)
            .send()
            .await
            .context("fail_task request failed")?;
        Ok(())
    }

    /// Main entrypoint: register, start heartbeat, poll loop, and HTTP server.
    ///
    /// `extra_routes` should be a `Router<()>` (no state) containing any
    /// agent-specific routes beyond /health, /, and /metrics.
    pub async fn run<H: TaskHandler>(self, handler: H, extra_routes: Router<()>) -> Result<()> {
        // 1. Init tracing
        tracing_subscriber::fmt()
            .with_env_filter(
                tracing_subscriber::EnvFilter::try_from_default_env()
                    .unwrap_or_else(|_| {
                        tracing_subscriber::EnvFilter::new(&self.config.log_level)
                    }),
            )
            .json()
            .init();

        info!(
            agent_id = %self.config.agent_id,
            port = self.config.port,
            "starting OpenClaw agent"
        );

        // 2. Register with Core (graceful failure)
        match self.register().await {
            Ok(()) => info!("registered with Core successfully"),
            Err(e) => warn!(error = %e, "failed to register with Core, continuing in standalone mode"),
        }

        // 3. Start heartbeat background task
        let hb_agent = self.clone();
        tokio::spawn(async move {
            heartbeat_loop(hb_agent).await;
        });

        // 4. Spawn task polling loop
        let poll_agent = self.clone();
        let handler = Arc::new(handler);
        tokio::spawn(async move {
            task_poll_loop(poll_agent, handler).await;
        });

        // 5. Install Prometheus metrics recorder
        let prom_recorder = metrics_exporter_prometheus::PrometheusBuilder::new()
            .build_recorder();
        let prom_handle = Arc::new(prom_recorder.handle());
        metrics::set_global_recorder(prom_recorder)
            .expect("failed to install Prometheus metrics recorder");

        // Record initial gauge values
        metrics::gauge!("agent_info", "agent_id" => self.config.agent_id.clone()).set(1.0);

        // 6. Build axum Router
        let metrics_handle = prom_handle.clone();
        let app = Router::new()
            .route("/health", get(health_handler))
            .with_state(self.stats.clone())
            .route("/", get(root_handler))
            .route("/metrics", get(move || {
                let h = metrics_handle.clone();
                async move {
                    let output = h.render();
                    (
                        StatusCode::OK,
                        [("content-type", "text/plain; charset=utf-8")],
                        output,
                    )
                }
            }))
            .merge(extra_routes);

        // 7. Start HTTP server
        let addr = format!("0.0.0.0:{}", self.config.port);
        info!(addr = %addr, "HTTP server listening");
        let listener = tokio::net::TcpListener::bind(&addr)
            .await
            .context("failed to bind HTTP listener")?;
        axum::serve(listener, app)
            .await
            .context("HTTP server error")?;

        Ok(())
    }
}

// ---------------------------------------------------------------------------
// Background loops
// ---------------------------------------------------------------------------

async fn heartbeat_loop(agent: OpenClawAgent) {
    let interval = Duration::from_secs(agent.config.heartbeat_interval);
    loop {
        tokio::time::sleep(interval).await;

        let stats = agent.stats.lock().await;
        let body = serde_json::json!({
            "status": "running",
            "tasks_completed": stats.tasks_completed,
            "tasks_in_progress": stats.tasks_in_progress,
            "last_error": stats.last_error,
            "timestamp": Utc::now(),
        });
        drop(stats);

        let url = format!(
            "{}/api/v1/agents/{}/heartbeat",
            agent.config.core_url, agent.config.agent_id
        );

        match agent
            .http
            .post(&url)
            .bearer_auth(&agent.config.api_key)
            .json(&body)
            .send()
            .await
        {
            Ok(resp) if resp.status().is_success() => {
                tracing::trace!("heartbeat sent");
            }
            Ok(resp) => {
                warn!(status = %resp.status(), "heartbeat non-success");
            }
            Err(e) => {
                warn!(error = %e, "heartbeat failed");
            }
        }
    }
}

async fn task_poll_loop<H: TaskHandler>(agent: OpenClawAgent, handler: Arc<H>) {
    loop {
        match agent.poll_task().await {
            Some(task) => {
                info!(task_id = %task.id, task_type = %task.task_type, "received task");

                {
                    let mut stats = agent.stats.lock().await;
                    stats.tasks_in_progress += 1;
                }
                metrics::gauge!("openclaw_tasks_in_progress").set(1.0);

                let start = std::time::Instant::now();
                match handler.handle(&agent, &task).await {
                    Ok(result) => {
                        let elapsed = start.elapsed().as_secs_f64();
                        metrics::counter!("openclaw_tasks_total", "status" => "completed", "type" => task.task_type.clone()).increment(1);
                        metrics::histogram!("openclaw_task_duration_seconds", "type" => task.task_type.clone()).record(elapsed);

                        if let Err(e) = agent.complete_task(&task.id, result).await {
                            error!(task_id = %task.id, error = %e, "failed to report task completion");
                        }
                        let mut stats = agent.stats.lock().await;
                        stats.tasks_in_progress = stats.tasks_in_progress.saturating_sub(1);
                        stats.tasks_completed += 1;
                        metrics::gauge!("openclaw_tasks_in_progress").set(stats.tasks_in_progress as f64);
                        metrics::gauge!("openclaw_tasks_completed_total").set(stats.tasks_completed as f64);
                    }
                    Err(e) => {
                        let err_msg = format!("{:#}", e);
                        error!(task_id = %task.id, error = %err_msg, "task failed");
                        metrics::counter!("openclaw_tasks_total", "status" => "failed", "type" => task.task_type.clone()).increment(1);

                        if let Err(report_err) = agent.fail_task(&task.id, &err_msg).await {
                            error!(task_id = %task.id, error = %report_err, "failed to report task failure");
                        }
                        let mut stats = agent.stats.lock().await;
                        stats.tasks_in_progress = stats.tasks_in_progress.saturating_sub(1);
                        stats.last_error = Some(err_msg);
                        metrics::gauge!("openclaw_tasks_in_progress").set(stats.tasks_in_progress as f64);
                    }
                }
            }
            None => {
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// HTTP handlers
// ---------------------------------------------------------------------------

async fn health_handler(State(stats): State<SharedStats>) -> impl IntoResponse {
    let stats = stats.lock().await;
    Json(serde_json::json!({
        "status": "healthy",
        "tasks_completed": stats.tasks_completed,
        "tasks_in_progress": stats.tasks_in_progress,
    }))
}

async fn root_handler() -> impl IntoResponse {
    Json(serde_json::json!({
        "service": "openclaw-agent",
        "version": env!("CARGO_PKG_VERSION"),
    }))
}

// metrics handler is inlined as a closure in run() to avoid state type conflicts
