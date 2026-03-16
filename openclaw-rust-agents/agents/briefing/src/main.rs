use std::sync::Arc;

use anyhow::{Context, Result};
use async_trait::async_trait;
use axum::{
    extract::State,
    http::StatusCode,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use chrono::{Local, TimeZone, Utc};
use openclaw_sdk::{AgentConfig, OpenClawAgent, Task, TaskHandler};
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use tracing::{error, info, warn};

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const DATA_DIR: &str = "/opt/openclaw/gateway-config/briefing-data";
const MEMORY_PATH: &str = "/opt/openclaw/gateway-config/memory/MEMORY.md";
const DISCORD_WEBHOOK_ENV: &str = "DISCORD_BRIEFING_WEBHOOK";
const CHICO_LAT: f64 = 39.7285;
const CHICO_LON: f64 = -121.8375;

// ---------------------------------------------------------------------------
// Data structures
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
struct BriefingData {
    weather: Option<WeatherData>,
    markets: Option<MarketsData>,
    crypto: Option<CryptoData>,
    news: Vec<NewsItem>,
    tasks: Vec<String>,
    generated_at: String,
    errors: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct WeatherData {
    temp_f: f64,
    feels_like_f: f64,
    condition: String,
    humidity: u32,
    wind_mph: f64,
    high_f: f64,
    low_f: f64,
    forecast: Vec<ForecastDay>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ForecastDay {
    day: String,
    high_f: f64,
    low_f: f64,
    condition: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct MarketsData {
    sp500: Option<MarketQuote>,
    nasdaq: Option<MarketQuote>,
    dow: Option<MarketQuote>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct MarketQuote {
    name: String,
    price: String,
    change: String,
    change_pct: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CryptoData {
    btc_usd: Option<CryptoPrice>,
    eth_usd: Option<CryptoPrice>,
    sol_usd: Option<CryptoPrice>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CryptoPrice {
    symbol: String,
    price: f64,
    change_24h: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct NewsItem {
    title: String,
    source: String,
    url: String,
}

// ---------------------------------------------------------------------------
// App state
// ---------------------------------------------------------------------------

#[derive(Clone)]
struct BriefingState {
    agent: Arc<OpenClawAgent>,
    data: Arc<RwLock<BriefingData>>,
    http: reqwest::Client,
}

// ---------------------------------------------------------------------------
// Data fetchers
// ---------------------------------------------------------------------------

async fn fetch_weather(http: &reqwest::Client) -> Result<WeatherData> {
    // wttr.in JSON format — no API key needed
    let url = format!("https://wttr.in/Chico,CA?format=j1");
    let resp = http.get(&url)
        .header("User-Agent", "openclaw-briefing/1.0")
        .send()
        .await
        .context("wttr.in request failed")?;

    let body: serde_json::Value = resp.json().await.context("wttr.in parse failed")?;

    let current = &body["current_condition"][0];
    let today_forecast = &body["weather"][0];

    let temp_f = current["temp_F"].as_str().unwrap_or("0").parse::<f64>().unwrap_or(0.0);
    let feels_like_f = current["FeelsLikeF"].as_str().unwrap_or("0").parse::<f64>().unwrap_or(0.0);
    let condition = current["weatherDesc"][0]["value"].as_str().unwrap_or("Unknown").to_string();
    let humidity = current["humidity"].as_str().unwrap_or("0").parse::<u32>().unwrap_or(0);
    let wind_mph = current["windspeedMiles"].as_str().unwrap_or("0").parse::<f64>().unwrap_or(0.0);
    let high_f = today_forecast["maxtempF"].as_str().unwrap_or("0").parse::<f64>().unwrap_or(0.0);
    let low_f = today_forecast["mintempF"].as_str().unwrap_or("0").parse::<f64>().unwrap_or(0.0);

    let mut forecast = Vec::new();
    if let Some(days) = body["weather"].as_array() {
        let day_names = ["Today", "Tomorrow", "Day After"];
        for (i, day) in days.iter().take(3).enumerate() {
            forecast.push(ForecastDay {
                day: day_names.get(i).unwrap_or(&"").to_string(),
                high_f: day["maxtempF"].as_str().unwrap_or("0").parse().unwrap_or(0.0),
                low_f: day["mintempF"].as_str().unwrap_or("0").parse().unwrap_or(0.0),
                condition: day["hourly"][4]["weatherDesc"][0]["value"]
                    .as_str()
                    .unwrap_or("Unknown")
                    .to_string(),
            });
        }
    }

    Ok(WeatherData {
        temp_f,
        feels_like_f,
        condition,
        humidity,
        wind_mph,
        high_f,
        low_f,
        forecast,
    })
}

async fn fetch_crypto(http: &reqwest::Client) -> Result<CryptoData> {
    // CoinGecko free API — no key needed
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true";
    let resp = http.get(url)
        .header("User-Agent", "openclaw-briefing/1.0")
        .send()
        .await
        .context("coingecko request failed")?;

    let body: serde_json::Value = resp.json().await.context("coingecko parse failed")?;

    let make_price = |id: &str, sym: &str| -> Option<CryptoPrice> {
        let coin = body.get(id)?;
        Some(CryptoPrice {
            symbol: sym.to_string(),
            price: coin["usd"].as_f64().unwrap_or(0.0),
            change_24h: coin["usd_24h_change"].as_f64().unwrap_or(0.0),
        })
    };

    Ok(CryptoData {
        btc_usd: make_price("bitcoin", "BTC"),
        eth_usd: make_price("ethereum", "ETH"),
        sol_usd: make_price("solana", "SOL"),
    })
}

async fn fetch_news(http: &reqwest::Client) -> Result<Vec<NewsItem>> {
    // Use Google News RSS — no API key needed
    let url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en";
    let resp = http.get(url)
        .header("User-Agent", "openclaw-briefing/1.0")
        .send()
        .await
        .context("google news rss request failed")?;

    let body = resp.text().await.context("google news rss body failed")?;

    // Simple XML parsing — pull out <item><title> and <link> and <source>
    let mut items = Vec::new();
    for item_chunk in body.split("<item>").skip(1).take(10) {
        let title = extract_xml_tag(item_chunk, "title").unwrap_or_default();
        let link = extract_xml_tag(item_chunk, "link").unwrap_or_default();
        let source = extract_xml_tag(item_chunk, "source").unwrap_or_else(|| "Unknown".into());

        if !title.is_empty() {
            items.push(NewsItem {
                title: html_decode(&title),
                source,
                url: link,
            });
        }
    }

    Ok(items)
}

fn extract_xml_tag(xml: &str, tag: &str) -> Option<String> {
    let open = format!("<{}", tag);
    let close = format!("</{}>", tag);
    let start = xml.find(&open)?;
    let after_open = &xml[start..];
    // Find the end of the opening tag
    let content_start = after_open.find('>')? + 1;
    let content = &after_open[content_start..];
    let end = content.find(&close)?;
    Some(content[..end].trim().to_string())
}

fn html_decode(s: &str) -> String {
    s.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", "\"")
        .replace("&#39;", "'")
        .replace("&#x27;", "'")
}

async fn fetch_markets(http: &reqwest::Client) -> Result<MarketsData> {
    // Use Yahoo Finance CSV endpoint — no key needed
    // Fallback: just report what we can
    let symbols = [("^GSPC", "S&P 500"), ("^IXIC", "NASDAQ"), ("^DJI", "Dow Jones")];
    let mut sp500 = None;
    let mut nasdaq = None;
    let mut dow = None;

    for (symbol, name) in &symbols {
        match fetch_yahoo_quote(http, symbol, name).await {
            Ok(quote) => {
                match *symbol {
                    "^GSPC" => sp500 = Some(quote),
                    "^IXIC" => nasdaq = Some(quote),
                    "^DJI" => dow = Some(quote),
                    _ => {}
                }
            }
            Err(e) => warn!(symbol = symbol, error = %e, "failed to fetch market quote"),
        }
    }

    Ok(MarketsData { sp500, nasdaq, dow })
}

async fn fetch_yahoo_quote(http: &reqwest::Client, symbol: &str, name: &str) -> Result<MarketQuote> {
    let url = format!(
        "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=1d",
        symbol
    );
    let resp = http.get(&url)
        .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        .send()
        .await
        .context("yahoo finance request failed")?;

    let body: serde_json::Value = resp.json().await.context("yahoo finance parse failed")?;
    let meta = &body["chart"]["result"][0]["meta"];

    let price = meta["regularMarketPrice"].as_f64().unwrap_or(0.0);
    let prev_close = meta["chartPreviousClose"].as_f64().unwrap_or(price);
    let change = price - prev_close;
    let change_pct = if prev_close > 0.0 { (change / prev_close) * 100.0 } else { 0.0 };

    let sign = if change >= 0.0 { "+" } else { "" };

    Ok(MarketQuote {
        name: name.to_string(),
        price: format!("{:.2}", price),
        change: format!("{}{:.2}", sign, change),
        change_pct: format!("{}{:.2}%", sign, change_pct),
    })
}

fn parse_tasks_from_memory(content: &str) -> Vec<String> {
    let mut tasks = Vec::new();
    let mut in_tasks_section = false;

    for line in content.lines() {
        if line.contains("## Pending Tasks") || line.contains("## TODO") || line.contains("## Tasks") {
            in_tasks_section = true;
            continue;
        }
        if in_tasks_section {
            if line.starts_with("## ") {
                break; // Next section
            }
            let trimmed = line.trim();
            if trimmed.starts_with("- ") || trimmed.starts_with("* ") {
                tasks.push(trimmed[2..].trim().to_string());
            }
        }
    }
    tasks
}

// ---------------------------------------------------------------------------
// Generate the briefing text file
// ---------------------------------------------------------------------------

fn format_briefing(data: &BriefingData) -> String {
    let now = Local::now();
    let day_name = now.format("%A, %B %-d, %Y").to_string();

    let mut out = String::new();
    out.push_str(&format!("=== Daily Briefing: {} ===\n\n", day_name));

    // Weather
    if let Some(w) = &data.weather {
        out.push_str(">>> WEATHER — Chico, CA\n");
        out.push_str(&format!("Currently: {}F (feels like {}F) — {}\n", w.temp_f, w.feels_like_f, w.condition));
        out.push_str(&format!("High/Low: {}F / {}F | Humidity: {}% | Wind: {} mph\n", w.high_f, w.low_f, w.humidity, w.wind_mph));
        for f in &w.forecast {
            out.push_str(&format!("  {}: {}F/{}F — {}\n", f.day, f.high_f, f.low_f, f.condition));
        }
        out.push('\n');
    }

    // Markets
    if let Some(m) = &data.markets {
        out.push_str(">>> MARKETS\n");
        if let Some(q) = &m.sp500 { out.push_str(&format!("S&P 500: {} ({} {})\n", q.price, q.change, q.change_pct)); }
        if let Some(q) = &m.nasdaq { out.push_str(&format!("NASDAQ:  {} ({} {})\n", q.price, q.change, q.change_pct)); }
        if let Some(q) = &m.dow { out.push_str(&format!("Dow:     {} ({} {})\n", q.price, q.change, q.change_pct)); }
        out.push('\n');
    }

    // Crypto
    if let Some(c) = &data.crypto {
        out.push_str(">>> CRYPTO\n");
        if let Some(p) = &c.btc_usd { out.push_str(&format!("BTC: ${:.0} ({:+.1}%)\n", p.price, p.change_24h)); }
        if let Some(p) = &c.eth_usd { out.push_str(&format!("ETH: ${:.0} ({:+.1}%)\n", p.price, p.change_24h)); }
        if let Some(p) = &c.sol_usd { out.push_str(&format!("SOL: ${:.2} ({:+.1}%)\n", p.price, p.change_24h)); }
        out.push('\n');
    }

    // News
    if !data.news.is_empty() {
        out.push_str(">>> TOP HEADLINES\n");
        for (i, item) in data.news.iter().take(8).enumerate() {
            out.push_str(&format!("{}. {} [{}]\n", i + 1, item.title, item.source));
        }
        out.push('\n');
    }

    // Tasks
    if !data.tasks.is_empty() {
        out.push_str(">>> PENDING TASKS\n");
        for task in &data.tasks {
            out.push_str(&format!("- {}\n", task));
        }
        out.push('\n');
    }

    // Errors (if any data sources failed)
    if !data.errors.is_empty() {
        out.push_str(">>> DATA FETCH ISSUES\n");
        for e in &data.errors {
            out.push_str(&format!("! {}\n", e));
        }
        out.push('\n');
    }

    out.push_str(&format!("Generated: {}\n", data.generated_at));
    out.push_str("=== End Briefing ===\n");
    out
}

// ---------------------------------------------------------------------------
// Core fetch-all routine
// ---------------------------------------------------------------------------

async fn fetch_all_data(http: &reqwest::Client) -> BriefingData {
    let mut data = BriefingData::default();
    let mut errors = Vec::new();

    // Fetch all sources concurrently
    let (weather, crypto, news, markets) = tokio::join!(
        fetch_weather(http),
        fetch_crypto(http),
        fetch_news(http),
        fetch_markets(http),
    );

    match weather {
        Ok(w) => data.weather = Some(w),
        Err(e) => errors.push(format!("Weather: {}", e)),
    }
    match crypto {
        Ok(c) => data.crypto = Some(c),
        Err(e) => errors.push(format!("Crypto: {}", e)),
    }
    match news {
        Ok(n) => data.news = n,
        Err(e) => errors.push(format!("News: {}", e)),
    }
    match markets {
        Ok(m) => data.markets = Some(m),
        Err(e) => errors.push(format!("Markets: {}", e)),
    }

    // Read tasks from MEMORY.md
    match tokio::fs::read_to_string(MEMORY_PATH).await {
        Ok(content) => data.tasks = parse_tasks_from_memory(&content),
        Err(e) => errors.push(format!("MEMORY.md: {}", e)),
    }

    data.errors = errors;
    data.generated_at = Utc::now().to_rfc3339();
    data
}

async fn save_briefing_files(data: &BriefingData) -> Result<()> {
    tokio::fs::create_dir_all(DATA_DIR).await.context("create briefing-data dir")?;

    let briefing_text = format_briefing(data);

    // Save individual files
    if let Some(w) = &data.weather {
        let weather_txt = format!(
            "Chico, CA — {}F (feels {}F), {}, H/L {}F/{}F, Humidity {}%, Wind {} mph",
            w.temp_f, w.feels_like_f, w.condition, w.high_f, w.low_f, w.humidity, w.wind_mph
        );
        tokio::fs::write(format!("{}/weather.txt", DATA_DIR), &weather_txt).await?;
    }

    if let Some(c) = &data.crypto {
        let mut crypto_txt = String::new();
        if let Some(p) = &c.btc_usd { crypto_txt.push_str(&format!("BTC: ${:.0} ({:+.1}%)\n", p.price, p.change_24h)); }
        if let Some(p) = &c.eth_usd { crypto_txt.push_str(&format!("ETH: ${:.0} ({:+.1}%)\n", p.price, p.change_24h)); }
        if let Some(p) = &c.sol_usd { crypto_txt.push_str(&format!("SOL: ${:.2} ({:+.1}%)\n", p.price, p.change_24h)); }
        tokio::fs::write(format!("{}/crypto.txt", DATA_DIR), &crypto_txt).await?;
    }

    if !data.news.is_empty() {
        let news_txt: String = data.news.iter().take(10)
            .enumerate()
            .map(|(i, n)| format!("{}. {} [{}]\n", i + 1, n.title, n.source))
            .collect();
        tokio::fs::write(format!("{}/news.txt", DATA_DIR), &news_txt).await?;
    }

    if let Some(m) = &data.markets {
        let mut markets_txt = String::new();
        if let Some(q) = &m.sp500 { markets_txt.push_str(&format!("S&P 500: {} ({} {})\n", q.price, q.change, q.change_pct)); }
        if let Some(q) = &m.nasdaq { markets_txt.push_str(&format!("NASDAQ:  {} ({} {})\n", q.price, q.change, q.change_pct)); }
        if let Some(q) = &m.dow { markets_txt.push_str(&format!("Dow:     {} ({} {})\n", q.price, q.change, q.change_pct)); }
        tokio::fs::write(format!("{}/markets.txt", DATA_DIR), &markets_txt).await?;
    }

    if !data.tasks.is_empty() {
        let tasks_txt: String = data.tasks.iter().map(|t| format!("- {}\n", t)).collect();
        tokio::fs::write(format!("{}/tasks.txt", DATA_DIR), &tasks_txt).await?;
    }

    // Save the combined briefing
    tokio::fs::write(format!("{}/briefing-ready.txt", DATA_DIR), &briefing_text).await?;

    // Save raw JSON too
    let json = serde_json::to_string_pretty(data)?;
    tokio::fs::write(format!("{}/briefing-data.json", DATA_DIR), &json).await?;

    info!("Briefing files saved to {}", DATA_DIR);
    Ok(())
}

fn build_briefing_embeds(data: &BriefingData) -> Vec<serde_json::Value> {
    let now = Local::now();
    let day_name = now.format("%A, %B %-d, %Y").to_string();
    let mut embeds = Vec::new();

    // Weather embed
    if let Some(w) = &data.weather {
        let mut forecast_lines = String::new();
        for f in &w.forecast {
            forecast_lines.push_str(&format!("{}: **{}°F**/{}°F — {}\n", f.day, f.high_f, f.low_f, f.condition));
        }
        embeds.push(serde_json::json!({
            "title": format!("🌤️ Weather — Chico, CA"),
            "color": 3447003, // blue
            "fields": [
                { "name": "Current", "value": format!("**{}°F** (feels {}°F) — {}", w.temp_f, w.feels_like_f, w.condition), "inline": true },
                { "name": "High / Low", "value": format!("{}°F / {}°F", w.high_f, w.low_f), "inline": true },
                { "name": "Details", "value": format!("💧 {}% humidity | 💨 {} mph wind", w.humidity, w.wind_mph), "inline": true },
                { "name": "Forecast", "value": forecast_lines, "inline": false },
            ],
        }));
    }

    // Markets + Crypto embed
    let mut market_lines = String::new();
    if let Some(m) = &data.markets {
        if let Some(q) = &m.sp500 {
            let emoji = if q.change.starts_with('+') { "🟢" } else { "🔴" };
            market_lines.push_str(&format!("{} **S&P 500** {} ({} {})\n", emoji, q.price, q.change, q.change_pct));
        }
        if let Some(q) = &m.nasdaq {
            let emoji = if q.change.starts_with('+') { "🟢" } else { "🔴" };
            market_lines.push_str(&format!("{} **NASDAQ** {} ({} {})\n", emoji, q.price, q.change, q.change_pct));
        }
        if let Some(q) = &m.dow {
            let emoji = if q.change.starts_with('+') { "🟢" } else { "🔴" };
            market_lines.push_str(&format!("{} **Dow** {} ({} {})\n", emoji, q.price, q.change, q.change_pct));
        }
    }

    let mut crypto_lines = String::new();
    if let Some(c) = &data.crypto {
        if let Some(p) = &c.btc_usd {
            let emoji = if p.change_24h >= 0.0 { "🟢" } else { "🔴" };
            crypto_lines.push_str(&format!("{} **BTC** ${:.0} ({:+.1}%)\n", emoji, p.price, p.change_24h));
        }
        if let Some(p) = &c.eth_usd {
            let emoji = if p.change_24h >= 0.0 { "🟢" } else { "🔴" };
            crypto_lines.push_str(&format!("{} **ETH** ${:.0} ({:+.1}%)\n", emoji, p.price, p.change_24h));
        }
        if let Some(p) = &c.sol_usd {
            let emoji = if p.change_24h >= 0.0 { "🟢" } else { "🔴" };
            crypto_lines.push_str(&format!("{} **SOL** ${:.2} ({:+.1}%)\n", emoji, p.price, p.change_24h));
        }
    }

    if !market_lines.is_empty() || !crypto_lines.is_empty() {
        let mut fields = Vec::new();
        if !market_lines.is_empty() {
            fields.push(serde_json::json!({ "name": "📈 Markets", "value": market_lines, "inline": true }));
        }
        if !crypto_lines.is_empty() {
            fields.push(serde_json::json!({ "name": "₿ Crypto", "value": crypto_lines, "inline": true }));
        }
        embeds.push(serde_json::json!({
            "title": "💰 Markets & Crypto",
            "color": 15844367, // gold
            "fields": fields,
        }));
    }

    // News embed
    if !data.news.is_empty() {
        let news_text: String = data.news.iter().take(6)
            .enumerate()
            .map(|(i, n)| format!("**{}**. {} *— {}*", i + 1, n.title, n.source))
            .collect::<Vec<_>>()
            .join("\n");
        embeds.push(serde_json::json!({
            "title": "📰 Top Headlines",
            "description": news_text,
            "color": 10070709, // gray
        }));
    }

    // Tasks embed (if any)
    if !data.tasks.is_empty() {
        let tasks_text: String = data.tasks.iter()
            .map(|t| format!("• {}", t))
            .collect::<Vec<_>>()
            .join("\n");
        embeds.push(serde_json::json!({
            "title": "📋 Pending Tasks",
            "description": tasks_text,
            "color": 15105570, // orange
        }));
    }

    // Set footer on last embed
    if let Some(last) = embeds.last_mut() {
        last["footer"] = serde_json::json!({ "text": format!("Briefing for {} • Generated by openclaw-briefing", day_name) });
        last["timestamp"] = serde_json::json!(data.generated_at);
    }

    embeds
}

async fn post_to_discord_webhook(http: &reqwest::Client, data: &BriefingData) -> Result<()> {
    let webhook_url = match std::env::var(DISCORD_WEBHOOK_ENV) {
        Ok(url) => url,
        Err(_) => {
            info!("No {} set, skipping Discord webhook post", DISCORD_WEBHOOK_ENV);
            return Ok(());
        }
    };

    let embeds = build_briefing_embeds(data);

    let body = serde_json::json!({
        "username": "Briefing Agent",
        "avatar_url": "https://cdn.discordapp.com/embed/avatars/0.png",
        "embeds": embeds,
    });

    let resp = http.post(&webhook_url)
        .json(&body)
        .send()
        .await
        .context("Discord webhook post failed")?;

    if !resp.status().is_success() {
        let status = resp.status();
        let text = resp.text().await.unwrap_or_default();
        anyhow::bail!("Discord webhook returned {}: {}", status, text);
    }

    info!("Posted briefing embeds to Discord webhook");
    Ok(())
}

// ---------------------------------------------------------------------------
// Background timer — fetch data at 5:50 AM PST daily
// ---------------------------------------------------------------------------

async fn briefing_timer(state: BriefingState) {
    // Also do an initial fetch on startup
    info!("Running initial briefing data fetch...");
    let data = fetch_all_data(&state.http).await;
    if let Err(e) = save_briefing_files(&data).await {
        error!(error = %e, "failed to save initial briefing files");
    }
    *state.data.write().await = data;
    info!("Initial briefing data fetch complete");

    loop {
        let now = Local::now();
        // Next run at 5:50 AM local time
        let target_hour = 5;
        let target_min = 50;

        let today_target = now.date_naive()
            .and_hms_opt(target_hour, target_min, 0)
            .unwrap();
        let today_target = Local::now()
            .timezone()
            .from_local_datetime(&today_target)
            .single()
            .unwrap_or(now);

        let next_run = if now >= today_target {
            // Already past 5:50 today, schedule for tomorrow
            today_target + chrono::Duration::days(1)
        } else {
            today_target
        };

        let wait = (next_run - now).to_std().unwrap_or(std::time::Duration::from_secs(3600));
        info!(next_run = %next_run, wait_secs = wait.as_secs(), "briefing timer scheduled");
        tokio::time::sleep(wait).await;

        info!("Briefing timer fired — fetching data...");
        let data = fetch_all_data(&state.http).await;

        if let Err(e) = save_briefing_files(&data).await {
            error!(error = %e, "failed to save briefing files");
        }

        // Post embeds directly to Discord — zero LLM cost
        if let Err(e) = post_to_discord_webhook(&state.http, &data).await {
            warn!(error = %e, "Discord webhook post failed");
        }

        *state.data.write().await = data;
    }
}

// ---------------------------------------------------------------------------
// HTTP handlers
// ---------------------------------------------------------------------------

async fn trigger_handler(State(state): State<BriefingState>) -> impl IntoResponse {
    info!("Manual briefing trigger received");
    let data = fetch_all_data(&state.http).await;
    if let Err(e) = save_briefing_files(&data).await {
        error!(error = %e, "failed to save briefing files");
    }
    // Post embeds to Discord
    if let Err(e) = post_to_discord_webhook(&state.http, &data).await {
        warn!(error = %e, "Discord webhook post failed on trigger");
    }
    let text = format_briefing(&data);
    *state.data.write().await = data;
    (StatusCode::OK, text)
}

async fn data_handler(State(state): State<BriefingState>) -> impl IntoResponse {
    let data = state.data.read().await;
    Json(data.clone())
}

async fn text_handler(State(state): State<BriefingState>) -> impl IntoResponse {
    let data = state.data.read().await;
    let text = format_briefing(&data);
    (StatusCode::OK, [("content-type", "text/plain")], text)
}

async fn dashboard_handler(State(state): State<BriefingState>) -> impl IntoResponse {
    let data = state.data.read().await;
    let briefing = format_briefing(&data);

    let html = format!(r#"<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><title>Briefing Dashboard</title>
<style>
body {{ background: #0d1117; color: #c9d1d9; font-family: 'Cascadia Code', 'Fira Code', monospace; margin: 0; padding: 20px; }}
h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 12px 0; }}
.card h2 {{ color: #58a6ff; margin-top: 0; font-size: 14px; }}
pre {{ white-space: pre-wrap; word-wrap: break-word; margin: 0; font-size: 13px; }}
.btn {{ background: #238636; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-family: inherit; font-size: 13px; }}
.btn:hover {{ background: #2ea043; }}
.error {{ color: #f85149; }}
.green {{ color: #3fb950; }}
.yellow {{ color: #d29922; }}
</style>
</head><body>
<h1>Briefing Dashboard</h1>
<button class="btn" onclick="fetch('/trigger',{{method:'POST'}}).then(()=>location.reload())">Refresh Data Now</button>
<div class="card"><h2>Latest Briefing</h2><pre>{}</pre></div>
<div class="card"><h2>Raw Data (JSON)</h2><pre>{}</pre></div>
<p style="color:#484f58;font-size:11px;">Generated: {}</p>
</body></html>"#,
        briefing.replace('<', "&lt;").replace('>', "&gt;"),
        serde_json::to_string_pretty(&*data).unwrap_or_default().replace('<', "&lt;").replace('>', "&gt;"),
        data.generated_at,
    );

    Html(html)
}

// ---------------------------------------------------------------------------
// Task handler (for Core API integration)
// ---------------------------------------------------------------------------

struct BriefingHandler;

#[async_trait]
impl TaskHandler for BriefingHandler {
    async fn handle(&self, _agent: &OpenClawAgent, task: &Task) -> Result<serde_json::Value> {
        match task.task_type.as_str() {
            "generate_briefing" => {
                let http = reqwest::Client::builder()
                    .timeout(std::time::Duration::from_secs(30))
                    .build()?;
                let data = fetch_all_data(&http).await;
                save_briefing_files(&data).await?;
                let text = format_briefing(&data);
                Ok(serde_json::json!({ "briefing": text, "data": data }))
            }
            other => anyhow::bail!("unknown task type: {}", other),
        }
    }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

#[tokio::main]
async fn main() -> Result<()> {
    let config = AgentConfig::from_env().context("failed to read agent config")?;
    let agent = OpenClawAgent::new(config);

    let http = reqwest::Client::builder()
        .timeout(std::time::Duration::from_secs(30))
        .build()
        .context("failed to build HTTP client")?;

    let state = BriefingState {
        agent: Arc::new(agent.clone()),
        data: Arc::new(RwLock::new(BriefingData::default())),
        http,
    };

    // Start background timer
    let timer_state = state.clone();
    tokio::spawn(async move {
        briefing_timer(timer_state).await;
    });

    let routes = Router::new()
        .route("/trigger", post(trigger_handler))
        .route("/data", get(data_handler))
        .route("/text", get(text_handler))
        .route("/dashboard", get(dashboard_handler))
        .with_state(state);

    agent.run(BriefingHandler, routes).await
}
