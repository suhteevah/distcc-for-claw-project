# ══════════════════════════════════════════════════════════════════════════════
# OpenClaw Rust Agent Fleet — Multi-Stage Build
#
# Builds all 9 agent binaries in one layer, then copies a single binary
# into a minimal runtime image. Use build-arg AGENT_NAME to select which.
#
# Usage:
#   docker build --build-arg AGENT_NAME=seo-auditor -t openclaw-seo-auditor .
#   docker build --build-arg AGENT_NAME=legal-team -t openclaw-legal-team .
# ══════════════════════════════════════════════════════════════════════════════

# ── Stage 1: Build ───────────────────────────────────────────────────────────
FROM rust:1.77-slim-bookworm AS builder

RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy manifests first for layer caching
COPY Cargo.toml Cargo.lock* ./
COPY sdk/Cargo.toml sdk/Cargo.toml

# Create dummy lib for sdk to cache dependencies
RUN mkdir -p sdk/src && echo "// dummy" > sdk/src/lib.rs

# Copy all agent Cargo.tomls and create dummy mains
COPY agents/seo-auditor/Cargo.toml agents/seo-auditor/Cargo.toml
COPY agents/lead-responder/Cargo.toml agents/lead-responder/Cargo.toml
COPY agents/content-mill/Cargo.toml agents/content-mill/Cargo.toml
COPY agents/proposal-gen/Cargo.toml agents/proposal-gen/Cargo.toml
COPY agents/job-hunter/Cargo.toml agents/job-hunter/Cargo.toml
COPY agents/client-dashboard/Cargo.toml agents/client-dashboard/Cargo.toml
COPY agents/wow-economy/Cargo.toml agents/wow-economy/Cargo.toml
COPY agents/legal-team/Cargo.toml agents/legal-team/Cargo.toml
COPY agents/coder/Cargo.toml agents/coder/Cargo.toml

RUN for agent in seo-auditor lead-responder content-mill proposal-gen job-hunter client-dashboard wow-economy legal-team coder; do \
    mkdir -p agents/$agent/src && echo "fn main() {}" > agents/$agent/src/main.rs; \
    done

# Build dependencies only (cached layer)
RUN cargo build --release --workspace 2>/dev/null || true

# Now copy real source
COPY sdk/src/ sdk/src/
COPY agents/ agents/

# Touch all main.rs to invalidate cached builds
RUN for agent in seo-auditor lead-responder content-mill proposal-gen job-hunter client-dashboard wow-economy legal-team coder; do \
    touch agents/$agent/src/main.rs; \
    done

# Build all binaries in release mode
RUN cargo build --release --workspace

# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM debian:bookworm-slim

ARG AGENT_NAME
ENV AGENT_BINARY=${AGENT_NAME}

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the specific agent binary
COPY --from=builder /build/target/release/${AGENT_NAME} /usr/local/bin/agent

# Non-root user
RUN groupadd -r openclaw && useradd -r -g openclaw openclaw
USER openclaw

EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:${AGENT_PORT:-8080}/health || exit 1

CMD ["/usr/local/bin/agent"]
