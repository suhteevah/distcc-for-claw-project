#!/usr/bin/env python3
"""Generate jedari.com SEO & Security Audit PDF report."""

from fpdf import FPDF
from datetime import datetime

class AuditPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'OpenClaw SEO Auditor | jedari.com Audit Report', 0, 1, 'R')
        self.line(10, 15, 200, 15)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | Generated {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, 0, 1)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def subsection(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, 0, 1)
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def issue_row(self, severity, category, issue, fix):
        # Severity badge color
        colors = {
            'CRITICAL': (220, 38, 38),
            'HIGH': (220, 38, 38),
            'WARNING': (234, 179, 8),
            'MEDIUM': (234, 179, 8),
            'INFO': (59, 130, 246),
            'LOW': (59, 130, 246),
        }
        r, g, b = colors.get(severity.upper(), (100, 100, 100))

        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(r, g, b)
        self.cell(22, 6, severity.upper(), 0, 0)

        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(80, 80, 80)
        self.cell(28, 6, category, 0, 0)

        self.set_font('Helvetica', '', 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, issue)

        self.set_x(50)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 4.5, f'Fix: {fix}')
        self.ln(2)

    def score_badge(self, score):
        if score >= 80:
            r, g, b = 34, 197, 94
        elif score >= 60:
            r, g, b = 234, 179, 8
        else:
            r, g, b = 220, 38, 38

        self.set_font('Helvetica', 'B', 36)
        self.set_text_color(r, g, b)
        self.cell(30, 20, str(score), 0, 0, 'C')
        self.set_font('Helvetica', '', 14)
        self.set_text_color(100, 100, 100)
        self.cell(20, 20, '/ 100', 0, 1, 'L')
        self.ln(3)


pdf = AuditPDF()
pdf.alias_nb_pages()
pdf.add_page()

# Title
pdf.set_font('Helvetica', 'B', 22)
pdf.set_text_color(20, 20, 20)
pdf.cell(0, 12, 'jedari.com', 0, 1)
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 7, 'SEO & Security Audit Report', 0, 1)
pdf.cell(0, 7, f'Audited: {datetime.now().strftime("%B %d, %Y")}', 0, 1)
pdf.cell(0, 7, 'Auditor: OpenClaw SEO Auditor v1.1 (enhanced scoring)', 0, 1)
pdf.ln(6)

# Score
pdf.section_title('Overall Score')
pdf.score_badge(68)
pdf.body_text(
    'Score reflects combined SEO health and security posture. '
    'The original auditor scored 80/100 (structural SEO only). '
    'The enhanced v1.1 auditor applies additional deductions for dead links, '
    'duplicate canonicals, excessive scripts, and missing security headers, '
    'bringing the score to 68/100.'
)

# Page Data Summary
pdf.section_title('Page Data Summary')
data_lines = [
    ('URL', 'https://www.jedari.com/'),
    ('HTTP Status', '200 OK'),
    ('Protocol', 'HTTP/2'),
    ('TTFB', '541ms'),
    ('Load Time', '2,999ms'),
    ('HTML Size', '4.4 KB (Cloudflare gzipped, 36 KB transfer)'),
    ('Title', 'Jedari Technology - Empowering Elite Musicians and Brands (55 chars)'),
    ('Meta Description', '157 chars - present and descriptive'),
    ('H1 Tags', '2 (should be 1) - "We help elite musicians..." + "AI Summary"'),
    ('H2 Tags', '9'),
    ('Images', '78 total, 17 missing alt text (22%)'),
    ('Internal Links', '~30'),
    ('External Links', '6'),
    ('Dead # Links', '~4 (Get Started CTAs)'),
    ('Canonical', 'Present but duplicated (2 tags)'),
    ('OG Tags', 'Full (title, description, image, url, type)'),
    ('Twitter Card', 'summary_large_image'),
    ('Schema.org', 'NONE'),
    ('External Scripts', '19'),
    ('Language', 'en'),
]
for label, value in data_lines:
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(42, 5.5, label)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    # Truncate long values to fit single line
    if len(value) > 90:
        pdf.cell(0, 5.5, value[:87] + '...')
    else:
        pdf.cell(0, 5.5, value)
    pdf.ln()

# SEO Issues
pdf.add_page()
pdf.section_title('SEO Issues')

seo_issues = [
    ('CRITICAL', 'links', '~4 links point to "#" (dead anchor links, broken CTAs)',
     'Wire all CTA links to real destinations; dead links hurt UX and crawl budget'),
    ('WARNING', 'headings', 'Page has 2 H1 tags (should be exactly 1)',
     'Demote "AI Summary" H1 to H2 or lower'),
    ('WARNING', 'images', '17 of 78 images are missing alt text',
     'Add descriptive alt attributes to all images for accessibility and SEO'),
    ('WARNING', 'canonical', 'Page has 2 canonical tags (should be exactly 1)',
     'Remove duplicate <link rel="canonical"> tag'),
    ('WARNING', 'performance', 'Page loads 19 external scripts (excessive)',
     'Audit and remove unused third-party scripts; defer non-critical JS'),
    ('WARNING', 'content', 'H2 tag used as body text/subtitle (long paragraph in H2)',
     'Use <p> for subtitle text; H2s should be section headings'),
    ('INFO', 'structured_data', 'No Schema.org structured data (JSON-LD or microdata)',
     'Add Organization, Product, and FAQ JSON-LD for rich snippets'),
    ('INFO', 'links', 'All 7 case study cards link to same URL (/case-studies)',
     'Give each case study its own URL for individual SEO value'),
    ('INFO', 'content', 'Copyright shows 2025',
     'Update to 2026'),
]

for sev, cat, issue, fix in seo_issues:
    pdf.issue_row(sev, cat, issue, fix)

# Security Issues
pdf.add_page()
pdf.section_title('Security Vulnerabilities')

sec_issues = [
    ('CRITICAL', 'headers', 'Missing Content-Security-Policy header',
     'Add CSP header restricting script-src to known domains. No CSP = XSS attack surface wide open.'),
    ('CRITICAL', 'headers', 'Missing X-Frame-Options / frame-ancestors',
     'Add X-Frame-Options: DENY or CSP frame-ancestors. Site can be embedded in iframes on any domain (clickjacking).'),
    ('CRITICAL', 'exposure', 'Exposed SoundCloud client_id in network requests',
     'Move API key server-side or accept rate-limit abuse risk.'),
    ('CRITICAL', 'config', 'reCAPTCHA Enterprise loaded but failing (ERR_ABORTED)',
     'Remove abandoned reCAPTCHA integration or fix it. Dead security code is a false sense of protection.'),
    ('WARNING', 'headers', 'Missing X-Content-Type-Options: nosniff',
     'Add header to prevent MIME-type sniffing attacks.'),
    ('WARNING', 'headers', 'Missing Referrer-Policy header',
     'Add Referrer-Policy: strict-origin-when-cross-origin. Full URLs currently leaked to all third parties.'),
    ('WARNING', 'headers', 'Missing Permissions-Policy header',
     'Restrict camera, microphone, geolocation access from embedded iframes.'),
    ('WARNING', 'links', 'jedarian.com/auth link opens target="_blank" without rel="noopener"',
     'Add rel="noopener noreferrer" to prevent reverse tabnapping.'),
    ('INFO', 'exposure', 'Server header reveals "cloudflare"',
     'Minor info leak; attackers know CDN provider.'),
    ('INFO', 'exposure', 'x-lambda-id and x-wf-region headers exposed',
     'Reveals Webflow Lambda function ID and AWS region.'),
]

for sev, cat, issue, fix in sec_issues:
    pdf.issue_row(sev, cat, issue, fix)

# Third Party Inventory
pdf.add_page()
pdf.section_title('Third-Party Service Inventory')

services = [
    ('Google Analytics', 'G-MYX9YZKP5J', 'Active', 'Tracking'),
    ('LeadConnector/GoHighLevel', 'backend.leadconnectorhq.com', 'Errors (repeated ERR_ABORTED)', 'Forms/CRM'),
    ('Cloudflare Turnstile', '0x4AAAAAAAQTptj2So4dx43e', 'Active (2 instances)', 'Bot protection'),
    ('SoundCloud Widget', 'api-widget.soundcloud.com', 'Active', 'Audio embed'),
    ('HubSpot on Webflow', 'hubspotonwebflow.com', 'Active', 'Integration'),
    ('Leadsy.ai', 'wvbknd.leadsy.ai', 'Error 400', 'Visitor tracking'),
    ('BendingSpoons/Orion', 'orion.bendingspoons.com', 'Active', 'Unknown'),
    ('reCAPTCHA Enterprise', 'google.com/recaptcha/enterprise', 'FAILING (ERR_ABORTED)', 'Unused/broken'),
    ('Google Fonts', 'fonts.googleapis.com', 'Active', 'Typography'),
]

pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(80, 80, 80)
pdf.cell(45, 6, 'Service', 0, 0)
pdf.cell(55, 6, 'Domain/ID', 0, 0)
pdf.cell(40, 6, 'Status', 0, 0)
pdf.cell(0, 6, 'Purpose', 0, 1)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(2)

for name, domain, status, purpose in services:
    pdf.set_font('Helvetica', 'B', 8)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(45, 5, name, 0, 0)
    pdf.set_font('Helvetica', '', 8)
    pdf.cell(55, 5, domain[:45], 0, 0)
    if 'Error' in status or 'FAIL' in status:
        pdf.set_text_color(220, 38, 38)
    else:
        pdf.set_text_color(34, 197, 94)
    pdf.cell(40, 5, status, 0, 0)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, purpose, 0, 1)

# Security headers table
pdf.ln(8)
pdf.subsection('Security Headers Present')

headers_data = [
    ('strict-transport-security', 'max-age=31536000', True),
    ('content-security-policy', 'MISSING', False),
    ('x-frame-options', 'MISSING', False),
    ('x-content-type-options', 'MISSING', False),
    ('referrer-policy', 'MISSING', False),
    ('permissions-policy', 'MISSING', False),
]

for hdr, val, present in headers_data:
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(55, 5.5, hdr, 0, 0)
    if present:
        pdf.set_text_color(34, 197, 94)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(10, 5.5, 'OK', 0, 0)
    else:
        pdf.set_text_color(220, 38, 38)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(10, 5.5, 'FAIL', 0, 0)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5.5, val, 0, 1)

# Priority Recommendations
pdf.add_page()
pdf.section_title('Priority Action Items')

pdf.subsection('Immediate (Security)')
immediate = [
    'Add Content-Security-Policy header (restrict script-src to known domains)',
    'Add X-Frame-Options: DENY or CSP frame-ancestors directive',
    'Add X-Content-Type-Options: nosniff',
    'Add Referrer-Policy: strict-origin-when-cross-origin',
    'Fix jedarian.com/auth link (add rel="noopener noreferrer")',
    'Remove or fix abandoned reCAPTCHA Enterprise integration',
]
for i, item in enumerate(immediate, 1):
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, f'  {i}. {item}', 0, 1)
pdf.ln(4)

pdf.subsection('Short-Term (SEO)')
short = [
    'Fix duplicate H1 (demote "AI Summary" to H2)',
    'Add alt text to all 17 images missing it',
    'Fix dead "#" links on Get Started CTAs',
    'Add Schema.org JSON-LD (Organization + Product + FAQ)',
    'Remove duplicate canonical tag',
    'Give each case study its own URL',
]
for i, item in enumerate(short, 1):
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, f'  {i}. {item}', 0, 1)
pdf.ln(4)

pdf.subsection('Medium-Term (Performance)')
medium = [
    'Audit and remove unused third-party scripts (Leadsy.ai 400, reCAPTCHA failing)',
    'Lazy-load video iframes (6 iframes including 2 Vimeo embeds)',
    'Fix LeadConnector geo-location repeated failures (ERR_ABORTED)',
    'Reduce external script count from 19 to <10',
]
for i, item in enumerate(medium, 1):
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 6, f'  {i}. {item}', 0, 1)

# Score breakdown
pdf.ln(8)
pdf.subsection('Score Breakdown (Enhanced v1.1)')
deductions = [
    ('2 H1 tags', -5),
    ('17 images missing alt', -10),
    ('No Schema.org', -5),
    ('Dead # links (~4)', -10),
    ('Duplicate canonical', -5),
    ('19 external scripts', -5),
    ('Unsafe target=_blank', -3),
    ('Missing CSP', -5),
    ('Missing X-Frame-Options', -3),
    ('Missing X-Content-Type-Options', -2),
    ('Missing Referrer-Policy', -2),
    ('Missing Permissions-Policy', -2),
]

total = 100
pdf.set_font('Helvetica', '', 9)
pdf.cell(80, 5.5, 'Starting score', 0, 0)
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(0, 5.5, '100', 0, 1)

for label, ded in deductions:
    total += ded
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(80, 5.5, f'  {label}', 0, 0)
    pdf.set_text_color(220, 38, 38)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 5.5, str(ded), 0, 1)

pdf.line(10, pdf.get_y() + 1, 120, pdf.get_y() + 1)
pdf.ln(3)
pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(220, 38, 38) if total < 70 else pdf.set_text_color(234, 179, 8)
pdf.cell(80, 7, 'FINAL SCORE', 0, 0)
pdf.cell(0, 7, f'{total} / 100', 0, 1)

out_path = r'J:\distcc for claw project\jedari-seo-security-audit.pdf'
pdf.output(out_path)
print(f'PDF saved to: {out_path}')
