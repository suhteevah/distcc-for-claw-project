use std::sync::Arc;

use anyhow::{Context, Result};
use axum::{
    extract::State,
    http::StatusCode,
    response::{IntoResponse, Json},
    routing::post,
    Router,
};
use serde::{Deserialize, Serialize};
use tracing::{error, info};

use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SYSTEM_PROMPT: &str = "\
You are an expert software engineer. Write clean, idiomatic code. \
Prefer Rust, C, and low-level languages when appropriate. \
Follow YAGNI and DRY principles. Include proper error handling. \
All generated code must be production-ready with tests where applicable.";

// ---------------------------------------------------------------------------
// Data types — Code Review
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ReviewIssue {
    severity: String,  // critical, warning, info
    category: String,  // bug, security, style, performance
    description: String,
    line_hint: Option<String>,
    suggestion: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ReviewResult {
    issues: Vec<ReviewIssue>,
    summary: String,
    overall_quality: u8,
}

#[derive(Debug, Deserialize)]
struct ReviewRequest {
    code: String,
    language: String,
    #[serde(default)]
    context: Option<String>,
}

// ---------------------------------------------------------------------------
// Data types — Code Generation
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GenerateResult {
    code: String,
    language: String,
    tests: String,
    explanation: String,
    dependencies: Vec<String>,
}

#[derive(Debug, Deserialize)]
struct GenerateRequest {
    spec: String,
    language: String,
    #[serde(default)]
    constraints: Option<Vec<String>>,
}

// ---------------------------------------------------------------------------
// Data types — Bug Fix
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct BugFixResult {
    fixed_code: String,
    explanation: String,
    diff_summary: String,
}

#[derive(Debug, Deserialize)]
struct BugFixRequest {
    code: String,
    language: String,
    #[serde(default)]
    error_message: Option<String>,
    description: String,
}

// ---------------------------------------------------------------------------
// Data types — Refactor
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct RefactorResult {
    refactored_code: String,
    changes_made: Vec<String>,
    before_after_comparison: String,
}

#[derive(Debug, Deserialize)]
struct RefactorRequest {
    code: String,
    language: String,
    goals: Vec<String>,
}

// ---------------------------------------------------------------------------
// Data types — Documentation
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
struct DocumentationResult {
    #[serde(skip_serializing_if = "Option::is_none")]
    documented_code: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    doc_text: Option<String>,
    doc_type: String,
}

#[derive(Debug, Deserialize)]
struct DocumentationRequest {
    code: String,
    language: String,
    doc_type: String, // inline_comments, readme, api_docs, architecture
}

// ---------------------------------------------------------------------------
// LLM helpers — robust JSON extraction from LLM responses
// ---------------------------------------------------------------------------

/// Extract JSON from an LLM response that may contain markdown fences.
///
/// Handles multiple edge cases:
/// - ```json ... ``` wrapping
/// - Nested ``` inside JSON string values (code fields)
/// - Raw JSON without fences
/// - Brace-matching for reliable extraction
fn extract_json(text: &str) -> String {
    let trimmed = text.trim();

    // Strategy 1: Find ```json fence and use brace-matching to find the end
    if let Some(start) = trimmed.find("```json") {
        let after_fence = &trimmed[start + 7..];
        // Skip whitespace/newline after ```json
        let after_ws = after_fence.trim_start();
        if let Some(json) = extract_balanced_json(after_ws) {
            return json;
        }
    }

    // Strategy 2: Find first { and brace-match to closing }
    if let Some(json) = extract_balanced_json(trimmed) {
        return json;
    }

    // Strategy 3: Find first { and last } (greedy)
    if let Some(start) = trimmed.find('{') {
        if let Some(end) = trimmed.rfind('}') {
            return trimmed[start..=end].to_string();
        }
    }

    trimmed.to_string()
}

/// Extract a balanced JSON object by tracking braces, respecting string literals.
fn extract_balanced_json(text: &str) -> Option<String> {
    let chars: Vec<char> = text.chars().collect();
    let start = chars.iter().position(|&c| c == '{')?;

    let mut depth = 0i32;
    let mut in_string = false;
    let mut escape_next = false;

    for i in start..chars.len() {
        let c = chars[i];

        if escape_next {
            escape_next = false;
            continue;
        }

        if c == '\\' && in_string {
            escape_next = true;
            continue;
        }

        if c == '"' {
            in_string = !in_string;
            continue;
        }

        if !in_string {
            match c {
                '{' => depth += 1,
                '}' => {
                    depth -= 1;
                    if depth == 0 {
                        let json: String = chars[start..=i].iter().collect();
                        return Some(json);
                    }
                }
                _ => {}
            }
        }
    }

    None
}

/// Call the LLM and parse the response as a typed JSON result.
/// If JSON parsing fails, falls back to returning the raw text in a
/// structured error response rather than failing entirely.
async fn llm_json<T: serde::de::DeserializeOwned>(
    agent: &OpenClawAgent,
    prompt: &str,
    max_tokens: u32,
    temperature: f32,
) -> Result<T> {
    let response = agent
        .llm
        .complete(
            prompt,
            Some("heavy"),
            Some(SYSTEM_PROMPT),
            Some(max_tokens),
            Some(temperature),
            true,
        )
        .await
        .context("LLM request failed")?;

    let json_str = extract_json(&response.text);

    // First try: parse as-is
    if let Ok(parsed) = serde_json::from_str::<T>(&json_str) {
        return Ok(parsed);
    }

    // Second try: unescape any double-escaped sequences
    let unescaped = json_str
        .replace("\\\\n", "\\n")
        .replace("\\\\t", "\\t")
        .replace("\\\\\"", "\\\"");
    if let Ok(parsed) = serde_json::from_str::<T>(&unescaped) {
        return Ok(parsed);
    }

    // Third try: if it's a GenerateResult-like thing, try to build it manually
    // by extracting fields from the raw JSON value
    if let Ok(raw_value) = serde_json::from_str::<serde_json::Value>(&json_str) {
        if let Ok(parsed) = serde_json::from_value::<T>(raw_value) {
            return Ok(parsed);
        }
    }

    // Final: return a helpful error with a truncated preview
    let preview_len = response.text.len().min(1000);
    anyhow::bail!(
        "Failed to parse LLM response as JSON after 3 attempts.\n\
         Response length: {} chars\n\
         Extracted JSON length: {} chars\n\
         Preview:\n{}",
        response.text.len(),
        json_str.len(),
        &response.text[..preview_len]
    )
}

/// Call the LLM and return the raw text (no JSON parsing).
/// Used when the output is naturally text (like generated code or documents).
async fn llm_text(
    agent: &OpenClawAgent,
    prompt: &str,
    max_tokens: u32,
    temperature: f32,
) -> Result<String> {
    let response = agent
        .llm
        .complete(
            prompt,
            Some("heavy"),
            Some(SYSTEM_PROMPT),
            Some(max_tokens),
            Some(temperature),
            false,
        )
        .await
        .context("LLM request failed")?;

    Ok(response.text)
}

// ---------------------------------------------------------------------------
// Task implementations
// ---------------------------------------------------------------------------

async fn run_code_review(agent: &OpenClawAgent, req: &ReviewRequest) -> Result<ReviewResult> {
    info!(language = %req.language, code_len = req.code.len(), "starting code review");

    let context_section = match &req.context {
        Some(ctx) => format!("\nContext: {}\n", ctx),
        None => String::new(),
    };

    let prompt = format!(
        r#"Review the following {lang} code and identify issues.
{context}
Code:
```{lang}
{code}
```

Respond with a JSON object with this exact schema:
{{
  "issues": [
    {{
      "severity": "critical" | "warning" | "info",
      "category": "bug" | "security" | "style" | "performance",
      "description": "what the issue is",
      "line_hint": "the relevant code snippet or line reference, or null",
      "suggestion": "how to fix it"
    }}
  ],
  "summary": "a brief overall assessment of the code",
  "overall_quality": <integer 1-10>
}}

Be thorough but fair. Only report real issues, not stylistic preferences unless they harm readability. Rate 1-10 where 10 is flawless production code."#,
        lang = req.language,
        code = req.code,
        context = context_section,
    );

    llm_json::<ReviewResult>(agent, &prompt, 8192, 0.3).await
}

async fn run_code_generation(
    agent: &OpenClawAgent,
    req: &GenerateRequest,
) -> Result<GenerateResult> {
    info!(language = %req.language, "starting code generation");

    let constraints_section = match &req.constraints {
        Some(c) if !c.is_empty() => {
            let items: Vec<String> = c.iter().map(|s| format!("- {}", s)).collect();
            format!("\nConstraints:\n{}\n", items.join("\n"))
        }
        _ => String::new(),
    };

    // Two-phase approach: generate code as structured text with clear delimiters,
    // then parse into our result struct. This avoids JSON-escaping code strings
    // which causes LLMs to produce broken JSON for large code blocks.
    let prompt = format!(
        r#"Generate {lang} code based on the following specification.

Specification:
{spec}
{constraints}
Structure your response with these EXACT section headers on their own lines:

===IMPLEMENTATION===
(write the complete implementation code here)

===TESTS===
(write complete test code that validates the implementation)

===EXPLANATION===
(brief explanation of design decisions and how it works)

===DEPENDENCIES===
(comma-separated list of required packages/crates, or "none")

Write production-quality code with proper error handling. Include comprehensive tests that cover edge cases."#,
        lang = req.language,
        spec = req.spec,
        constraints = constraints_section,
    );

    let raw = llm_text(agent, &prompt, 8192, 0.4).await?;

    // Parse the sectioned response
    let code = extract_section(&raw, "===IMPLEMENTATION===", "===TESTS===")
        .unwrap_or_else(|| extract_code_block(&raw));
    let tests = extract_section(&raw, "===TESTS===", "===EXPLANATION===")
        .unwrap_or_default();
    let explanation = extract_section(&raw, "===EXPLANATION===", "===DEPENDENCIES===")
        .unwrap_or_default();
    let deps_raw = extract_section(&raw, "===DEPENDENCIES===", "")
        .unwrap_or_default();

    let dependencies: Vec<String> = if deps_raw.to_lowercase().contains("none") || deps_raw.trim().is_empty() {
        vec![]
    } else {
        deps_raw
            .split(',')
            .map(|s| s.trim().trim_matches('`').to_string())
            .filter(|s| !s.is_empty() && s != "none")
            .collect()
    };

    Ok(GenerateResult {
        code: strip_code_fences(&code),
        language: req.language.clone(),
        tests: strip_code_fences(&tests),
        explanation: explanation.trim().to_string(),
        dependencies,
    })
}

/// Extract text between two section markers.
fn extract_section(text: &str, start_marker: &str, end_marker: &str) -> Option<String> {
    let start = text.find(start_marker)?;
    let after = &text[start + start_marker.len()..];
    let content = if end_marker.is_empty() || !after.contains(end_marker) {
        after.to_string()
    } else {
        let end = after.find(end_marker)?;
        after[..end].to_string()
    };
    Some(content.trim().to_string())
}

/// Extract the first code block from text (fallback if section markers missing).
fn extract_code_block(text: &str) -> String {
    if let Some(start) = text.find("```") {
        let after = &text[start + 3..];
        // Skip language identifier
        let after_lang = if let Some(nl) = after.find('\n') {
            &after[nl + 1..]
        } else {
            after
        };
        if let Some(end) = after_lang.find("```") {
            return after_lang[..end].trim().to_string();
        }
    }
    text.to_string()
}

/// Strip markdown code fences from a string if present.
fn strip_code_fences(text: &str) -> String {
    let trimmed = text.trim();
    if trimmed.starts_with("```") {
        let after = if let Some(nl) = trimmed.find('\n') {
            &trimmed[nl + 1..]
        } else {
            trimmed
        };
        if after.ends_with("```") {
            return after[..after.len() - 3].trim().to_string();
        }
        return after.to_string();
    }
    trimmed.to_string()
}

async fn run_bug_fix(agent: &OpenClawAgent, req: &BugFixRequest) -> Result<BugFixResult> {
    info!(language = %req.language, "starting bug fix");

    let error_section = match &req.error_message {
        Some(e) => format!("\nError message:\n{}\n", e),
        None => String::new(),
    };

    let prompt = format!(
        r#"Fix the bug in the following {lang} code.

Problem description: {description}
{error}
Buggy code:
```{lang}
{code}
```

Respond with a JSON object with this exact schema:
{{
  "fixed_code": "the complete corrected code",
  "explanation": "what was wrong and exactly how it was fixed",
  "diff_summary": "concise summary of the changes made (e.g. 'Changed line 15: replaced == with === in null check')"
}}

Preserve the original code structure as much as possible. Only change what is necessary to fix the bug. The fixed code must be complete and runnable."#,
        lang = req.language,
        description = req.description,
        code = req.code,
        error = error_section,
    );

    llm_json::<BugFixResult>(agent, &prompt, 6144, 0.2).await
}

async fn run_refactor(agent: &OpenClawAgent, req: &RefactorRequest) -> Result<RefactorResult> {
    info!(language = %req.language, goals = ?req.goals, "starting refactor");

    let goals_list: Vec<String> = req.goals.iter().map(|g| format!("- {}", g)).collect();

    let prompt = format!(
        r#"Refactor the following {lang} code according to the specified goals.

Refactoring goals:
{goals}

Original code:
```{lang}
{code}
```

Respond with a JSON object with this exact schema:
{{
  "refactored_code": "the complete refactored code",
  "changes_made": ["description of change 1", "description of change 2", ...],
  "before_after_comparison": "a narrative comparison explaining what changed and why each change improves the code"
}}

Preserve external behavior (same inputs produce same outputs). The refactored code must be complete and runnable. Each entry in changes_made should describe one specific transformation applied."#,
        lang = req.language,
        code = req.code,
        goals = goals_list.join("\n"),
    );

    llm_json::<RefactorResult>(agent, &prompt, 8192, 0.3).await
}

async fn run_documentation(
    agent: &OpenClawAgent,
    req: &DocumentationRequest,
) -> Result<DocumentationResult> {
    info!(language = %req.language, doc_type = %req.doc_type, "starting documentation");

    let (instruction, schema) = match req.doc_type.as_str() {
        "inline_comments" => (
            "Add comprehensive inline comments to the code. Comment complex logic, \
             function purposes, parameter meanings, and non-obvious behavior. \
             Do not over-comment trivial operations.",
            r#"{
  "documented_code": "the complete code with added inline comments",
  "doc_text": null,
  "doc_type": "inline_comments"
}"#,
        ),
        "readme" => (
            "Generate a README document for this code. Include: overview, installation, \
             usage examples, API reference (if applicable), and any important notes.",
            r#"{
  "documented_code": null,
  "doc_text": "the complete README content in markdown",
  "doc_type": "readme"
}"#,
        ),
        "api_docs" => (
            "Generate API documentation for this code. Document all public functions, \
             structs, enums, traits, methods, parameters, return types, and error conditions. \
             Use the language's standard doc format.",
            r#"{
  "documented_code": null,
  "doc_text": "the complete API documentation",
  "doc_type": "api_docs"
}"#,
        ),
        "architecture" => (
            "Generate an architecture document for this code. Describe the overall design, \
             component relationships, data flow, key abstractions, and design patterns used.",
            r#"{
  "documented_code": null,
  "doc_text": "the complete architecture document in markdown",
  "doc_type": "architecture"
}"#,
        ),
        other => (
            "Generate appropriate documentation for this code based on the requested type.",
            // Fallback — we build it dynamically below
            "",
        ),
    };

    let schema_str = if schema.is_empty() {
        format!(
            r#"{{
  "documented_code": null,
  "doc_text": "the documentation content",
  "doc_type": "{}"
}}"#,
            req.doc_type
        )
    } else {
        schema.to_string()
    };

    let prompt = format!(
        r#"Generate documentation for the following {lang} code.

Documentation type: {doc_type}

Instructions: {instruction}

Code:
```{lang}
{code}
```

Respond with a JSON object with this exact schema:
{schema}

Write clear, accurate documentation that would help a developer understand and use this code."#,
        lang = req.language,
        doc_type = req.doc_type,
        instruction = instruction,
        code = req.code,
        schema = schema_str,
    );

    llm_json::<DocumentationResult>(agent, &prompt, 6144, 0.4).await
}

// ---------------------------------------------------------------------------
// TaskHandler
// ---------------------------------------------------------------------------

struct CoderHandler;

#[async_trait::async_trait]
impl TaskHandler for CoderHandler {
    async fn handle(&self, agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "code_review" => {
                let req: ReviewRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid code_review payload")?;
                let result = run_code_review(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize review result")
            }
            "code_generation" => {
                let req: GenerateRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid code_generation payload")?;
                let result = run_code_generation(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize generation result")
            }
            "bug_fix" => {
                let req: BugFixRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid bug_fix payload")?;
                let result = run_bug_fix(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize bug fix result")
            }
            "refactor" => {
                let req: RefactorRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid refactor payload")?;
                let result = run_refactor(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize refactor result")
            }
            "documentation" => {
                let req: DocumentationRequest = serde_json::from_value(task.payload.clone())
                    .context("invalid documentation payload")?;
                let result = run_documentation(agent, &req).await?;
                serde_json::to_value(result).context("failed to serialize documentation result")
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

async fn review_endpoint(
    State(agent): State<Arc<OpenClawAgent>>,
    Json(req): Json<ReviewRequest>,
) -> impl IntoResponse {
    match run_code_review(&agent, &req).await {
        Ok(result) => (
            StatusCode::OK,
            Json(serde_json::to_value(result).unwrap()),
        )
            .into_response(),
        Err(e) => {
            error!(error = %e, "code review failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn generate_endpoint(
    State(agent): State<Arc<OpenClawAgent>>,
    Json(req): Json<GenerateRequest>,
) -> impl IntoResponse {
    match run_code_generation(&agent, &req).await {
        Ok(result) => (
            StatusCode::OK,
            Json(serde_json::to_value(result).unwrap()),
        )
            .into_response(),
        Err(e) => {
            error!(error = %e, "code generation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn fix_endpoint(
    State(agent): State<Arc<OpenClawAgent>>,
    Json(req): Json<BugFixRequest>,
) -> impl IntoResponse {
    match run_bug_fix(&agent, &req).await {
        Ok(result) => (
            StatusCode::OK,
            Json(serde_json::to_value(result).unwrap()),
        )
            .into_response(),
        Err(e) => {
            error!(error = %e, "bug fix failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn refactor_endpoint(
    State(agent): State<Arc<OpenClawAgent>>,
    Json(req): Json<RefactorRequest>,
) -> impl IntoResponse {
    match run_refactor(&agent, &req).await {
        Ok(result) => (
            StatusCode::OK,
            Json(serde_json::to_value(result).unwrap()),
        )
            .into_response(),
        Err(e) => {
            error!(error = %e, "refactor failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

async fn docs_endpoint(
    State(agent): State<Arc<OpenClawAgent>>,
    Json(req): Json<DocumentationRequest>,
) -> impl IntoResponse {
    match run_documentation(&agent, &req).await {
        Ok(result) => (
            StatusCode::OK,
            Json(serde_json::to_value(result).unwrap()),
        )
            .into_response(),
        Err(e) => {
            error!(error = %e, "documentation failed");
            (
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(serde_json::json!({ "error": format!("{:#}", e) })),
            )
                .into_response()
        }
    }
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let config = AgentConfig::from_env()?;
    let agent = OpenClawAgent::new(config);

    let shared_agent = Arc::new(agent.clone());
    let routes = Router::new()
        .route("/review", post(review_endpoint))
        .route("/generate", post(generate_endpoint))
        .route("/fix", post(fix_endpoint))
        .route("/refactor", post(refactor_endpoint))
        .route("/docs", post(docs_endpoint))
        .with_state(shared_agent);

    agent.run(CoderHandler, routes).await
}
