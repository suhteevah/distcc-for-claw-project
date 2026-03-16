#!/bin/bash
# Pre-fetch emails for MailClaw + extract Upwork jobs for job-hunter pipeline
HIMALAYA="/usr/local/bin/himalaya -c /opt/openclaw/himalaya/config.toml"
OUTPUT="/opt/openclaw/gateway-config/workspace-mailclaw/latest-emails.txt"
JOBS_JSON="/opt/openclaw/gateway-config/workspace-mailclaw/hot-jobs.json"

echo "=== Email Fetch $(date -Iseconds) ===" > "$OUTPUT"

for ACCOUNT in ridgecell suhteevah mmichels; do
    echo "" >> "$OUTPUT"
    echo "### Account: $ACCOUNT ###" >> "$OUTPUT"
    echo "--- Recent Envelopes ---" >> "$OUTPUT"
    $HIMALAYA envelope list -a "$ACCOUNT" --page-size 10 2>/dev/null >> "$OUTPUT"
    echo "" >> "$OUTPUT"

    IDS=$($HIMALAYA envelope list -a "$ACCOUNT" --page-size 5 2>/dev/null | grep -oE '^\s*[0-9]+' | head -5)
    for ID in $IDS; do
        echo "--- Message $ID Preview ---" >> "$OUTPUT"
        $HIMALAYA message read -a "$ACCOUNT" "$ID" 2>/dev/null | head -30 >> "$OUTPUT"
        echo "..." >> "$OUTPUT"
        echo "" >> "$OUTPUT"
    done
done

echo "=== End of Email Fetch ===" >> "$OUTPUT"

# Extract Upwork jobs to JSON (with job URLs from email bodies)
python3 << 'PYEOF'
import json, re, subprocess
from datetime import datetime

OUTPUT = "/opt/openclaw/gateway-config/workspace-mailclaw/latest-emails.txt"
JOBS_JSON = "/opt/openclaw/gateway-config/workspace-mailclaw/hot-jobs.json"
HIMALAYA = "/usr/local/bin/himalaya -c /opt/openclaw/himalaya/config.toml"

# Step 1: Parse envelope table for Upwork job email IDs + titles
job_emails = []
with open(OUTPUT) as f:
    current_account = "ridgecell"
    for line in f:
        if "### Account:" in line:
            m = re.search(r"### Account: (\w+)", line)
            if m:
                current_account = m.group(1)
        if "Upwork Notification" in line and "New job:" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                email_id = parts[1].strip()
                title = parts[3].strip()
                title = re.sub(r"^New job:\s*", "", title).strip()
                if title and title != "SUBJECT" and email_id.isdigit():
                    job_emails.append({
                        "email_id": email_id,
                        "account": current_account,
                        "title": title,
                    })

# Step 2: For each job email, read body to extract Upwork job URL
jobs = []
for je in job_emails:
    job_url = None
    description = je["title"]
    try:
        cmd = f'{HIMALAYA} message read -a {je["account"]} {je["email_id"]}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        body = result.stdout
        # Extract job URL from "View job details:" line or any upwork.com/jobs/ link
        url_match = re.search(r'https://www\.upwork\.com/jobs/~\S+', body)
        if url_match:
            job_url = url_match.group(0)
            # Clean trailing punctuation
            job_url = re.sub(r'[>\s"\']+$', '', job_url)
        # Try to get a better description from the email body
        # First non-empty line that's not a header/link/label
        for bline in body.split('\n'):
            bline = bline.strip()
            if len(bline) > 60 and not bline.startswith('http') and not bline.startswith('|') and ':' not in bline[:20]:
                description = bline[:500]
                break
    except Exception as e:
        print(f"  Warning: could not read email {je['email_id']}: {e}")

    jobs.append({
        "title": je["title"],
        "description": description,
        "job_url": job_url,
        "budget": None,
        "rating": "HOT"
    })

with open(JOBS_JSON, "w") as f:
    json.dump({"timestamp": datetime.utcnow().isoformat() + "Z", "jobs": jobs}, f, indent=2)

print(f"Extracted {len(jobs)} Upwork jobs ({sum(1 for j in jobs if j['job_url'])} with URLs)")
PYEOF
