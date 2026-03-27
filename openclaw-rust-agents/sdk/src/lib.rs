use std::sync::Arc;
use std::time::Duration;
use std::collections::HashMap;

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

pub mod groq;
pub use groq::{GroqClient, Model as GroqModel};

// ---------------------------------------------------------------------------
// Soul (system prompt) loader with SHA-256 integrity verification
// ---------------------------------------------------------------------------

/// Compute SHA-256 hex digest of a byte slice.
fn sha256_hex(data: &[u8]) -> String {
    use std::fmt::Write;
    // Minimal SHA-256 — we inline the constants to avoid adding a crate dep.
    // Uses the standard FIPS 180-4 algorithm.
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ];

    let mut h: [u32; 8] = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ];

    // Pre-processing: padding
    let bit_len = (data.len() as u64) * 8;
    let mut msg = data.to_vec();
    msg.push(0x80);
    while (msg.len() % 64) != 56 {
        msg.push(0x00);
    }
    msg.extend_from_slice(&bit_len.to_be_bytes());

    // Process each 512-bit (64-byte) block
    for chunk in msg.chunks(64) {
        let mut w = [0u32; 64];
        for i in 0..16 {
            w[i] = u32::from_be_bytes([chunk[i*4], chunk[i*4+1], chunk[i*4+2], chunk[i*4+3]]);
        }
        for i in 16..64 {
            let s0 = w[i-15].rotate_right(7) ^ w[i-15].rotate_right(18) ^ (w[i-15] >> 3);
            let s1 = w[i-2].rotate_right(17) ^ w[i-2].rotate_right(19) ^ (w[i-2] >> 10);
            w[i] = w[i-16].wrapping_add(s0).wrapping_add(w[i-7]).wrapping_add(s1);
        }

        let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut hh] = h;
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ ((!e) & g);
            let t1 = hh.wrapping_add(s1).wrapping_add(ch).wrapping_add(K[i]).wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh = g; g = f; f = e; e = d.wrapping_add(t1);
            d = c; c = b; b = a; a = t1.wrapping_add(t2);
        }
        h[0] = h[0].wrapping_add(a); h[1] = h[1].wrapping_add(b);
        h[2] = h[2].wrapping_add(c); h[3] = h[3].wrapping_add(d);
        h[4] = h[4].wrapping_add(e); h[5] = h[5].wrapping_add(f);
        h[6] = h[6].wrapping_add(g); h[7] = h[7].wrapping_add(hh);
    }

    let mut hex = String::with_capacity(64);
    for val in &h {
        write!(hex, "{:08x}", val).unwrap();
    }
    hex
}

/// Load the soul hash manifest from `/opt/openclaw/souls/MANIFEST.sha256`
/// or `SOUL_MANIFEST_PATH` env var. Format: `<sha256>  <agent-id>` per line.
fn load_soul_manifest() -> HashMap<String, String> {
    let manifest_path = std::env::var("SOUL_MANIFEST_PATH")
        .unwrap_or_else(|_| "/opt/openclaw/souls/MANIFEST.sha256".to_string());

    let mut map = HashMap::new();
    if let Ok(contents) = std::fs::read_to_string(&manifest_path) {
        for line in contents.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }
            // Format: "<hash>  <agent-id>" (two spaces, matching sha256sum output)
            if let Some((hash, agent_id)) = line.split_once("  ") {
                map.insert(agent_id.trim().to_string(), hash.trim().to_string());
            }
        }
    }
    map
}

/// Load a soul.md file for an agent with SHA-256 integrity verification.
///
/// Search order:
/// 1. `SOUL_PATH` env var (explicit override)
/// 2. `/opt/openclaw/souls/{agent_id}.md`
/// 3. `./soul.md` (local development)
///
/// After loading, verifies the SHA-256 hash against `MANIFEST.sha256`.
/// If the manifest exists and the hash doesn't match, the soul is REJECTED
/// and the function returns None (agent falls back to hardcoded default).
///
/// If no manifest exists (dev mode), loads without verification but logs a warning.
pub fn load_soul(agent_id: &str) -> Option<String> {
    let manifest = load_soul_manifest();

    let paths_to_try: Vec<String> = {
        let mut v = Vec::new();
        if let Ok(path) = std::env::var("SOUL_PATH") {
            v.push(path);
        }
        v.push(format!("/opt/openclaw/souls/{}.md", agent_id));
        v.push("./soul.md".to_string());
        v
    };

    for path in &paths_to_try {
        if let Ok(contents) = std::fs::read_to_string(path) {
            // Normalize: strip \r (Windows line endings), then trim whitespace
            let normalized = contents.replace('\r', "");
            let trimmed = normalized.trim().to_string();
            let hash = sha256_hex(trimmed.as_bytes());

            if let Some(expected_hash) = manifest.get(agent_id) {
                if hash == *expected_hash {
                    // Use eprintln for soul messages — runs before tracing init
                    eprintln!("[SOUL] {} ✓ verified (sha256:{}..{}) from {}",
                        agent_id, &hash[..8], &hash[56..], path);
                    return Some(trimmed);
                } else {
                    eprintln!("[SOUL] {} ✗ INTEGRITY FAILURE — expected {}..{}, got {}..{} — REJECTING from {}",
                        agent_id, &expected_hash[..8], &expected_hash[56..],
                        &hash[..8], &hash[56..], path);
                    return None; // Reject — fall back to hardcoded
                }
            } else if !manifest.is_empty() {
                // Manifest exists but no entry for this agent
                eprintln!("[SOUL] {} ⚠ loaded but not in manifest (sha256:{}..{}) from {}",
                    agent_id, &hash[..8], &hash[56..], path);
                return Some(trimmed);
            } else {
                // No manifest at all (dev mode)
                eprintln!("[SOUL] {} ⚠ loaded UNVERIFIED — no MANIFEST.sha256 found (sha256:{}..{}) from {}",
                    agent_id, &hash[..8], &hash[56..], path);
                return Some(trimmed);
            }
        }
    }

    eprintln!("[SOUL] {} ✗ no soul.md found — using hardcoded fallback", agent_id);
    None
}

/// Generate a MANIFEST.sha256 for all soul files in a directory.
/// Useful for deployment: run once, commit the manifest, then agents verify at startup.
pub fn generate_soul_manifest(souls_dir: &str) -> Result<String> {
    let mut manifest = String::new();
    manifest.push_str("# OpenClaw Soul Manifest — SHA-256 integrity hashes\n");
    manifest.push_str("# Generated by openclaw-sdk::generate_soul_manifest()\n");
    manifest.push_str(&format!("# Date: {}\n", Utc::now().to_rfc3339()));
    manifest.push_str("#\n");

    let mut entries: Vec<(String, String)> = Vec::new();

    for entry in std::fs::read_dir(souls_dir)
        .context(format!("failed to read souls directory: {}", souls_dir))?
    {
        let entry = entry?;
        let path = entry.path();
        if path.extension().map(|e| e == "md").unwrap_or(false) {
            let contents = std::fs::read_to_string(&path)?;
            let normalized = contents.replace('\r', "");
            let trimmed = normalized.trim().to_string();
            let hash = sha256_hex(trimmed.as_bytes());
            let agent_id = path.file_stem().unwrap().to_string_lossy().to_string();
            entries.push((agent_id, hash));
        }
    }

    entries.sort_by(|a, b| a.0.cmp(&b.0));
    for (agent_id, hash) in &entries {
        manifest.push_str(&format!("{}  {}\n", hash, agent_id));
    }

    Ok(manifest)
}

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
    /// Direct Groq client — `None` if `GROQ_API_KEY` is not set.
    /// Agents call `agent.groq()` to get it, which panics if unavailable.
    /// Use `agent.has_groq()` to check first.
    pub groq_client: Option<GroqClient>,
    pub stats: SharedStats,
    http: reqwest::Client,
}

impl OpenClawAgent {
    pub fn new(config: AgentConfig) -> Self {
        let llm = LlmClient::new(&config.core_url, &config.api_key, &config.llm_tier);
        let groq_client = GroqClient::from_env();
        if groq_client.is_some() {
            info!(agent_id = %config.agent_id, "Groq LLM available");
        }
        let http = reqwest::Client::builder()
            .timeout(Duration::from_secs(30))
            .build()
            .expect("failed to build HTTP client");
        Self {
            config,
            llm,
            groq_client,
            stats: Arc::new(Mutex::new(AgentStats::default())),
            http,
        }
    }

    /// Get the Groq client. Panics if `GROQ_API_KEY` is not set.
    pub fn groq(&self) -> &GroqClient {
        self.groq_client
            .as_ref()
            .expect("Groq client not available — set GROQ_API_KEY env var")
    }

    /// Check if Groq is available.
    pub fn has_groq(&self) -> bool {
        self.groq_client.is_some()
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

        // 2.5 Post startup status to Discord blackboard
        let caps = self.config.capabilities.join(", ");
        if let Err(e) = post_discord_status(
            "DISCORD_WEBHOOK",
            &self.config.agent_id,
            "🟢 Online",
            &format!("Port {} | Capabilities: {}", self.config.port, caps),
            DISCORD_GREEN,
        ).await {
            warn!(error = %e, "failed to post startup status to Discord");
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
            Ok(resp) if resp.status() == StatusCode::NOT_FOUND => {
                warn!("heartbeat 404 — agent not registered, re-registering");
                match agent.register().await {
                    Ok(()) => info!("re-registered with Core after heartbeat 404"),
                    Err(e) => warn!(error = %e, "re-registration failed"),
                }
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

                        // Post task completion to Discord blackboard
                        let _ = post_discord_status(
                            "DISCORD_WEBHOOK",
                            &agent.config.agent_id,
                            "✅ Task Complete",
                            &format!("Type: `{}` | Duration: {:.1}s | Total: {}", task.task_type, elapsed, stats.tasks_completed),
                            DISCORD_GREEN,
                        ).await;
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
                        stats.last_error = Some(err_msg.clone());
                        metrics::gauge!("openclaw_tasks_in_progress").set(stats.tasks_in_progress as f64);

                        // Post task failure to Discord blackboard
                        let _ = post_discord_status(
                            "DISCORD_WEBHOOK",
                            &agent.config.agent_id,
                            "❌ Task Failed",
                            &format!("Type: `{}`\n```\n{}\n```", task.task_type, &err_msg[..err_msg.len().min(500)]),
                            DISCORD_RED,
                        ).await;
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

// ---------------------------------------------------------------------------
// Discord webhook helper — zero LLM cost blackboard posting
// ---------------------------------------------------------------------------

/// Post rich embeds to a Discord webhook. Reads URL from the given env var.
/// Returns Ok(()) silently if env var is not set.
pub async fn post_discord_embeds(
    env_var: &str,
    username: &str,
    embeds: Vec<serde_json::Value>,
) -> Result<()> {
    let webhook_url = match std::env::var(env_var) {
        Ok(url) if !url.is_empty() => url,
        _ => return Ok(()),
    };

    let http = reqwest::Client::builder()
        .timeout(Duration::from_secs(10))
        .build()
        .context("failed to build webhook HTTP client")?;

    let body = serde_json::json!({
        "username": username,
        "embeds": embeds,
    });

    let resp = http.post(&webhook_url)
        .json(&body)
        .send()
        .await
        .context("Discord webhook POST failed")?;

    if !resp.status().is_success() {
        let status = resp.status();
        let text = resp.text().await.unwrap_or_default();
        anyhow::bail!("Discord webhook returned {}: {}", status, text);
    }

    info!("Posted {} embed(s) to Discord", embeds.len());
    Ok(())
}

/// Post a simple status message embed (green=online, red=error, yellow=warning)
pub async fn post_discord_status(
    env_var: &str,
    agent_name: &str,
    status: &str,
    details: &str,
    color: u32,
) -> Result<()> {
    let embed = serde_json::json!({
        "title": format!("{} — {}", agent_name, status),
        "description": details,
        "color": color,
        "timestamp": Utc::now().to_rfc3339(),
        "footer": { "text": format!("openclaw-{} • Rust", agent_name.to_lowercase()) },
    });
    post_discord_embeds(env_var, agent_name, vec![embed]).await
}

// Common Discord embed colors
pub const DISCORD_GREEN: u32 = 3066993;
pub const DISCORD_RED: u32 = 15548997;
pub const DISCORD_YELLOW: u32 = 16776960;
pub const DISCORD_BLUE: u32 = 3447003;
pub const DISCORD_GOLD: u32 = 15844367;
pub const DISCORD_GRAY: u32 = 10070709;
pub const DISCORD_ORANGE: u32 = 15105570;
