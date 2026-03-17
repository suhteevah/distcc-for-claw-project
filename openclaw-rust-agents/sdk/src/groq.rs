//! Direct Groq API client for OpenClaw agents.
//!
//! Calls Groq's OpenAI-compatible endpoint directly (no Core proxy).
//! Zero new crate dependencies — uses reqwest + serde already in workspace.
//!
//! # Usage
//! ```no_run
//! let groq = GroqClient::from_env()?;
//! let resp = groq.chat(vec![
//!     ChatMessage { role: "system".into(), content: "You are a helpful assistant.".into() },
//!     ChatMessage { role: "user".into(), content: "Summarize this contract.".into() },
//! ], Model::Smart, None, None).await?;
//! println!("{}", resp.text);
//! ```

use std::time::Duration;

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use tracing::{debug, info, warn};

use crate::{ChatMessage, LlmResponse};

// ---------------------------------------------------------------------------
// Model selection
// ---------------------------------------------------------------------------

/// Model tier selection for Groq inference.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Model {
    /// Llama 3.3 70B — complex reasoning, long analysis, content generation.
    /// ~6K TPM free tier. Use for tasks that need quality.
    Smart,
    /// Llama 3.1 8B — fast decisions, classification, short summaries.
    /// ~30K TPM free tier. Use for high-frequency or simple tasks.
    Fast,
}

impl Model {
    pub fn model_id(&self) -> &'static str {
        match self {
            Model::Smart => "llama-3.3-70b-versatile",
            Model::Fast => "llama-3.1-8b-instant",
        }
    }

    pub fn default_max_tokens(&self) -> u32 {
        match self {
            Model::Smart => 4096,
            Model::Fast => 2048,
        }
    }
}

impl std::fmt::Display for Model {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.model_id())
    }
}

// ---------------------------------------------------------------------------
// Groq API request/response types (OpenAI-compatible)
// ---------------------------------------------------------------------------

#[derive(Debug, Serialize)]
struct GroqChatRequest {
    model: String,
    messages: Vec<GroqMessage>,
    #[serde(skip_serializing_if = "Option::is_none")]
    max_tokens: Option<u32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    temperature: Option<f32>,
    #[serde(skip_serializing_if = "Option::is_none")]
    response_format: Option<ResponseFormat>,
}

#[derive(Debug, Serialize)]
struct GroqMessage {
    role: String,
    content: String,
}

#[derive(Debug, Serialize)]
struct ResponseFormat {
    r#type: String,
}

#[derive(Debug, Deserialize)]
struct GroqChatResponse {
    choices: Vec<GroqChoice>,
    usage: Option<GroqUsage>,
    model: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GroqChoice {
    message: GroqChoiceMessage,
}

#[derive(Debug, Deserialize)]
struct GroqChoiceMessage {
    content: Option<String>,
}

#[derive(Debug, Deserialize)]
struct GroqUsage {
    total_tokens: Option<u32>,
}

#[derive(Debug, Deserialize)]
struct GroqErrorResponse {
    error: Option<GroqErrorDetail>,
}

#[derive(Debug, Deserialize)]
struct GroqErrorDetail {
    message: Option<String>,
    r#type: Option<String>,
}

// ---------------------------------------------------------------------------
// GroqClient
// ---------------------------------------------------------------------------

/// Direct client for the Groq inference API.
///
/// Agents can use this alongside or instead of `LlmClient` (which proxies
/// through Core). This client calls Groq directly — lower latency, no Core
/// dependency, but requires `GROQ_API_KEY` env var.
#[derive(Clone)]
pub struct GroqClient {
    http: reqwest::Client,
    api_key: String,
    base_url: String,
    default_model: Model,
}

impl GroqClient {
    /// Create from explicit parameters.
    pub fn new(api_key: &str, default_model: Model) -> Self {
        let http = reqwest::Client::builder()
            .timeout(Duration::from_secs(120))
            .build()
            .expect("failed to build Groq HTTP client");

        Self {
            http,
            api_key: api_key.to_string(),
            base_url: "https://api.groq.com/openai/v1".to_string(),
            default_model,
        }
    }

    /// Create from environment variables.
    ///
    /// - `GROQ_API_KEY` (required)
    /// - `GROQ_MODEL` (optional, "smart" or "fast", default "smart")
    /// - `GROQ_BASE_URL` (optional, for custom endpoints)
    ///
    /// Returns `None` if `GROQ_API_KEY` is not set (agent runs without LLM).
    pub fn from_env() -> Option<Self> {
        let api_key = std::env::var("GROQ_API_KEY").ok()?;
        if api_key.is_empty() {
            return None;
        }

        let default_model = match std::env::var("GROQ_MODEL").unwrap_or_default().as_str() {
            "fast" | "8b" => Model::Fast,
            _ => Model::Smart,
        };

        let mut client = Self::new(&api_key, default_model);

        if let Ok(url) = std::env::var("GROQ_BASE_URL") {
            if !url.is_empty() {
                client.base_url = url;
            }
        }

        info!(model = %client.default_model, "Groq client initialized");
        Some(client)
    }

    /// Simple text completion with a single prompt.
    ///
    /// Wraps the prompt as a user message with an optional system message.
    pub async fn complete(
        &self,
        prompt: &str,
        model: Option<Model>,
        system: Option<&str>,
        max_tokens: Option<u32>,
        temperature: Option<f32>,
    ) -> Result<LlmResponse> {
        let mut messages = Vec::new();
        if let Some(sys) = system {
            messages.push(ChatMessage {
                role: "system".into(),
                content: sys.into(),
            });
        }
        messages.push(ChatMessage {
            role: "user".into(),
            content: prompt.into(),
        });

        self.chat(messages, model, max_tokens, temperature, false).await
    }

    /// Chat completion with full message history.
    pub async fn chat(
        &self,
        messages: Vec<ChatMessage>,
        model: Option<Model>,
        max_tokens: Option<u32>,
        temperature: Option<f32>,
        json_mode: bool,
    ) -> Result<LlmResponse> {
        let model = model.unwrap_or(self.default_model);
        let max_tokens = max_tokens.unwrap_or(model.default_max_tokens());

        let groq_messages: Vec<GroqMessage> = messages
            .iter()
            .map(|m| GroqMessage {
                role: m.role.clone(),
                content: m.content.clone(),
            })
            .collect();

        let response_format = if json_mode {
            Some(ResponseFormat {
                r#type: "json_object".to_string(),
            })
        } else {
            None
        };

        let body = GroqChatRequest {
            model: model.model_id().to_string(),
            messages: groq_messages,
            max_tokens: Some(max_tokens),
            temperature,
            response_format,
        };

        debug!(
            model = model.model_id(),
            msg_count = messages.len(),
            "sending Groq chat request"
        );

        let resp = self
            .http
            .post(format!("{}/chat/completions", self.base_url))
            .bearer_auth(&self.api_key)
            .json(&body)
            .send()
            .await
            .context("Groq API request failed")?;

        let status = resp.status();
        let resp_text = resp.text().await.unwrap_or_default();

        if !status.is_success() {
            // Try to parse error details
            if let Ok(err_resp) = serde_json::from_str::<GroqErrorResponse>(&resp_text) {
                if let Some(err) = err_resp.error {
                    let msg = err.message.unwrap_or_else(|| "unknown error".into());
                    let err_type = err.r#type.unwrap_or_default();

                    // Rate limit — log with warning level
                    if status.as_u16() == 429 {
                        warn!(model = model.model_id(), "Groq rate limit hit: {}", msg);
                    }

                    anyhow::bail!("Groq API {} ({}): {}", status, err_type, msg);
                }
            }
            anyhow::bail!("Groq API returned {}: {}", status, &resp_text[..resp_text.len().min(500)]);
        }

        let parsed: GroqChatResponse = serde_json::from_str(&resp_text)
            .context("failed to parse Groq response")?;

        let text = parsed
            .choices
            .first()
            .and_then(|c| c.message.content.clone())
            .unwrap_or_default();

        let tokens_used = parsed
            .usage
            .and_then(|u| u.total_tokens)
            .unwrap_or(0);

        let actual_model = parsed.model.unwrap_or_else(|| model.model_id().to_string());

        debug!(
            model = %actual_model,
            tokens = tokens_used,
            response_len = text.len(),
            "Groq response received"
        );

        Ok(LlmResponse {
            text,
            tokens_used,
            model: actual_model,
            backend: "groq".into(),
        })
    }

    /// Check if the client is configured and ready.
    pub fn is_available(&self) -> bool {
        !self.api_key.is_empty()
    }

    /// Get the default model tier.
    pub fn default_model(&self) -> Model {
        self.default_model
    }
}

impl std::fmt::Debug for GroqClient {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GroqClient")
            .field("base_url", &self.base_url)
            .field("default_model", &self.default_model)
            .field("api_key", &"***")
            .finish()
    }
}
