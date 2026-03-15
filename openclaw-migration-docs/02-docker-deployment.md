# OpenClaw Docker Deployment Reference

*Scraped from https://docs.openclaw.ai/install/docker — March 2026*

## Quick Start
```bash
./docker-setup.sh
```

## Key Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENCLAW_IMAGE` | Pre-built image (e.g., `ghcr.io/openclaw/openclaw:latest`) |
| `OPENCLAW_DOCKER_APT_PACKAGES` | Space-separated system packages |
| `OPENCLAW_EXTENSIONS` | Pre-install extension dependencies |
| `OPENCLAW_EXTRA_MOUNTS` | Comma-separated Docker bind mounts |
| `OPENCLAW_HOME_VOLUME` | Named volume for persistent `/home/node` |
| `OPENCLAW_SANDBOX` | Enable Docker sandbox |
| `OPENCLAW_DOCKER_SOCKET` | Override Docker socket path |
| `OPENCLAW_GATEWAY_BIND` | Bind mode: `lan`, `loopback`, `custom`, `tailnet`, `auto` |

## Docker Compose Services

Standard `docker-compose.yml` includes:
- **openclaw-gateway**: Main application on port 18789
- **openclaw-cli**: CLI container sharing gateway network namespace

## Volume Mounts & Persistence

**Bind Mounts:**
- `~/.openclaw/` → `/home/node/.openclaw`
- `~/.openclaw/workspace` → `/home/node/.openclaw/workspace`

## Health Checks

**Unauthenticated:**
```bash
curl -fsS http://127.0.0.1:18789/healthz  # Liveness
curl -fsS http://127.0.0.1:18789/readyz   # Readiness
```

Docker image includes built-in `HEALTHCHECK` pinging `/healthz`.

## Image Tags
```
ghcr.io/openclaw/openclaw:main       # Latest from main
ghcr.io/openclaw/openclaw:latest     # Latest stable
ghcr.io/openclaw/openclaw:<version>  # Specific release
```

## Container User
Runs as non-root `node` user (uid 1000). Fix permissions:
```bash
sudo chown -R 1000:1000 /path/to/config /path/to/workspace
```

## Base Image
`node:24-bookworm`

## Default CMD
```
node dist/index.js --allow-unconfigured
```

## Manual Flow
```bash
docker build -t openclaw:local -f Dockerfile .
docker compose run --rm openclaw-cli onboard
docker compose up -d openclaw-gateway
```
