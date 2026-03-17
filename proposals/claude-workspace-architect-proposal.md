# Proposal: AI Systems Architect — Claude AI Workspace
**Job**: AI Systems Architect Needed to Build Claude AI Workspace for Analytics, Automation, and Research
**Client**: Philadelphia, US — Member since 2017, $4.4K spent, 30 hires
**Rate**: Hourly, Expert, 1-3 months, <30hrs/week
**Proposals**: 20-50 submitted

---

## Cover Letter

I've already built exactly what you're describing — not as a concept, but as a production system running right now on my own fleet.

My system, OpenClaw, runs Claude as the central brain coordinating 10 specialized AI agents across a multi-machine setup (Linux server, Mac, Windows workstations). It handles the full pipeline you outlined: user directive → Claude → tools/skills/workflows → outputs. Agents handle SEO auditing, content generation, job scoring, legal document drafting, code review, email triage, and daily briefings — all orchestrated through a Python FastAPI core with PostgreSQL, Redis, and real-time Grafana dashboards.

Your Mac Mini architecture maps directly to what I've already solved:

**Workspace Architecture** — I'd set up Claude Code on the Mac Mini as the persistent workspace with structured project contexts, instruction layers (I use SHA-256 locked "soul" files for each agent's personality and rules), and a task dispatch system accessible from your MacBook Pro and Desktop via Tailscale mesh VPN or LAN.

**Core Capabilities** — Your skills list (document analysis, research, data processing, summarization, dashboards, task planning) maps 1:1 to capabilities I've already built as reusable agent modules. I'd port and adapt these for your use cases rather than building from scratch.

**Analytics Environment** — This is where it gets interesting. I'd wire up a Python data stack (Pandas, Polars, DuckDB for fast local analytics) with Claude as the reasoning layer — you describe what you want analyzed, Claude writes and executes the processing pipeline, generates Streamlit dashboards or reports. Sports and financial analytics are data-heavy but structurally similar: ingest → transform → model → visualize. I'd build template workflows for each.

**Tech stack alignment** — Python, FastAPI, PostgreSQL, DuckDB, Streamlit, VS Code, GitHub — I use all of these daily. My agents are built in Rust for performance, but your workflows would be Python-first for accessibility.

I'm not a prompt engineer. I'm a systems architect who builds AI infrastructure. Happy to screen share a live demo of OpenClaw running — seeing a working system is worth more than any proposal.

— Matt Gates, Ridge Cell Repair LLC

---

## Suggested Rate: $75–95/hr

## Key Differentiator
You have 20-50 proposals. Most will be from prompt engineers who'll set up a Claude project with some custom instructions. You need someone who's built the persistent workspace + agent orchestration + data pipeline architecture you described. That's a very short list, and I'm on it.
