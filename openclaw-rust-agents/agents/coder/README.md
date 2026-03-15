# Coder

Expert software engineering agent. Handles code review, generation, bug fixing, refactoring, and documentation. Writes clean, idiomatic, production-ready code with proper error handling and tests. Prefers Rust and C for systems work.

## Port: 8009
## LLM Tier: heavy

## Capabilities
- `code_review` — Severity-based issue reporting with line references
- `code_generation` — Two-phase generation with section markers
- `bug_fix` — Root cause diagnosis and fix generation
- `refactor` — Code restructuring for clarity and performance
- `documentation` — Inline docs, API docs, README content

## API Endpoints

### POST /review
Review code for issues.
- **Request:** `{ "code": "string", "language": "string", "context": "string" }`
- **Response:** `{ "issues": [{ "severity": "critical|warning|info", "line": u32, "message": "string", "suggestion": "string" }], "summary": "string", "overall_quality": "string" }`

### POST /generate
Generate code from a specification.
- **Request:** `{ "spec": "string", "language": "string", "context": "string" }`
- **Response (section markers):**
```
===IMPLEMENTATION===
[generated code]
===TESTS===
[test code]
===EXPLANATION===
[what the code does and why]
===DEPENDENCIES===
[required crates/packages]
```

### POST /fix
Diagnose and fix a bug.
- **Request:** `{ "code": "string", "bug_description": "string", "error_output": "string", "language": "string" }`
- **Response:** `{ "fixed_code": "string", "root_cause": "string", "explanation": "string" }`

### POST /refactor
Refactor existing code.
- **Request:** `{ "code": "string", "goals": ["string"], "language": "string" }`
- **Response:** `{ "refactored_code": "string", "changes": [{ "description": "string", "reason": "string" }] }`

### POST /docs
Generate documentation.
- **Request:** `{ "code": "string", "doc_type": "inline|api|readme", "language": "string" }`
- **Response:** `{ "documentation": "string", "doc_type": "string" }`

## Task Types
- `code_review` — Analyzes code and returns severity-rated issues (critical/warning/info) with line numbers and fix suggestions.
- `code_generation` — Two-phase approach: LLM generates code using section markers (`===IMPLEMENTATION===`, `===TESTS===`, `===EXPLANATION===`, `===DEPENDENCIES===`) instead of JSON mode, which breaks on large code responses. Agent parses sections from raw text.
- `bug_fix` — Takes buggy code + error description, returns fixed code with root cause analysis.
- `refactor` — Restructures code based on stated goals (performance, readability, maintainability). Explains each change.
- `documentation` — Generates inline comments, API documentation, or README content from source code.

## Key Implementation Detail
Uses `extract_balanced_json()` for proper brace-matched JSON extraction when parsing structured data from LLM responses. Code generation deliberately avoids JSON mode because large code blocks with escaping cause JSON parsing failures.

## System Prompt
> You are an expert software engineer. Write clean, idiomatic code. Prefer Rust, C, and low-level languages when appropriate. Follow YAGNI and DRY principles. Include proper error handling. All generated code must be production-ready with tests where applicable.

## Dependencies
- `openclaw-sdk` (workspace) — Agent SDK, task queue, LLM client
- `axum` (workspace) — HTTP server
- `tokio` (workspace) — Async runtime
- `serde` / `serde_json` (workspace) — Serialization
- `tracing` (workspace) — Structured logging
- `chrono` (workspace) — Date/time handling
- `anyhow` (workspace) — Error handling
- `async-trait` (workspace) — Async trait support

## Configuration
| Variable | Description |
|----------|-------------|
| `AGENT_ID` | `coder` |
| `AGENT_PORT` | `8009` |
| `AGENT_CAPABILITIES` | `code_review,code_generation,bug_fix,refactor,documentation` |
| `LLM_TIER` | `heavy` |
| `MAX_CONCURRENT_TASKS` | `2` |
| `LOG_LEVEL` | `info` |
