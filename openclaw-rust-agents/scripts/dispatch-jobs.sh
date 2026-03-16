#!/bin/bash
# Reads hot-jobs.json and dispatches to job-hunter via core API
CORE_URL="http://localhost:9000"
API_KEY="openclaw-fleet-key-2026"
JOBS_FILE="/opt/openclaw/gateway-config/workspace-mailclaw/hot-jobs.json"

if [ ! -f "$JOBS_FILE" ]; then
    echo "No hot-jobs.json found, skipping"
    exit 0
fi

# Check if file was modified in last 35 min (fresh)
if [ "$(find "$JOBS_FILE" -mmin +35 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "hot-jobs.json is stale (>35 min old), skipping"
    exit 0
fi

python3 << 'PYEOF'
import json, urllib.request, sys

CORE_URL = "http://localhost:9000"
API_KEY = "openclaw-fleet-key-2026"
JOBS_FILE = "/opt/openclaw/gateway-config/workspace-mailclaw/hot-jobs.json"

with open(JOBS_FILE) as f:
    data = json.load(f)

jobs = data.get("jobs", [])
if not jobs:
    print("No jobs to dispatch")
    sys.exit(0)

print(f"Dispatching {len(jobs)} jobs to job-hunter...")

for job in jobs:
    payload = {
        "agent_id": "job-hunter",
        "task_type": "score_job",
        "payload": {
            "job_title": job.get("title", ""),
            "job_description": job.get("description", job.get("title", "")),
            "budget_range": job.get("budget"),
            "job_url": job.get("job_url"),
            "source": "upwork"
        }
    }
    req = urllib.request.Request(
        f"{CORE_URL}/api/v1/tasks",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        print(f"  -> {job.get('title','')[:60]} => {result.get('task_id','?')}")
    except Exception as e:
        print(f"  FAILED: {job.get('title','')[:60]} => {e}", file=sys.stderr)

print("Done")
PYEOF
