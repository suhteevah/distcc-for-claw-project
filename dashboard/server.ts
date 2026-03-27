// =============================================================================
// Life Dashboard - Deno Server
// Serves on port 8888, designed to run behind Tailscale Funnel on cnc-server
// =============================================================================

const PORT = parseInt(Deno.env.get("DASHBOARD_PORT") || "8888");
const CONFIG_PATH = Deno.env.get("DASHBOARD_CONFIG") || "./dashboard.json";

// --- Config ---
interface Config {
  weather: { lat: string; lon: string; apiKey: string; units: string };
  finance: { stocks: string[]; crypto: string[] };
  fleet: { agents: { host: string; port: number; name: string }[]; tailscaleHosts: string[] };
  tasks: Task[];
  habits: Habit[];
}

interface Task {
  id: string;
  text: string;
  done: boolean;
  created: string;
}

interface Habit {
  id: string;
  name: string;
  log: string[]; // dates completed
}

let config: Config;

async function loadConfig(): Promise<Config> {
  try {
    const raw = await Deno.readTextFile(CONFIG_PATH);
    return JSON.parse(raw);
  } catch {
    const defaults: Config = {
      weather: { lat: "40.7128", lon: "-74.0060", apiKey: "", units: "metric" },
      finance: { stocks: ["AAPL", "GOOGL", "MSFT"], crypto: ["bitcoin", "ethereum"] },
      fleet: {
        agents: [
          { host: "localhost", port: 3284, name: "cnc-local" },
          { host: "macbook1", port: 3284, name: "macbook1" },
          { host: "imac", port: 3284, name: "imac" },
          { host: "rpi1", port: 3284, name: "rpi1" },
          { host: "rpi2", port: 3284, name: "rpi2" },
          { host: "rpi3", port: 3284, name: "rpi3" },
          { host: "fcp-appletv", port: 3284, name: "appletv-4k" },
        ],
        tailscaleHosts: ["cnc-server", "macbook1", "macbook2", "imac", "rpi1", "rpi2", "rpi3", "fcp-appletv"],
      },
      tasks: [],
      habits: [],
    };
    await saveConfig(defaults);
    return defaults;
  }
}

async function saveConfig(cfg: Config) {
  await Deno.writeTextFile(CONFIG_PATH, JSON.stringify(cfg, null, 2));
}

// --- Data Fetchers ---

async function fetchWeather(): Promise<Record<string, unknown>> {
  const { lat, lon, apiKey, units } = config.weather;
  if (!apiKey) return { error: "No weather API key configured. Set weather.apiKey in dashboard.json (OpenWeatherMap)" };
  try {
    const resp = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=${units}`
    );
    return await resp.json();
  } catch (e) {
    return { error: String(e) };
  }
}

async function fetchForecast(): Promise<Record<string, unknown>> {
  const { lat, lon, apiKey, units } = config.weather;
  if (!apiKey) return { error: "No API key" };
  try {
    const resp = await fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${apiKey}&units=${units}&cnt=8`
    );
    return await resp.json();
  } catch (e) {
    return { error: String(e) };
  }
}

async function fetchCrypto(): Promise<Record<string, unknown>[]> {
  const ids = config.finance.crypto.join(",");
  try {
    const resp = await fetch(
      `https://api.coingecko.com/api/v3/simple/price?ids=${ids}&vs_currencies=usd&include_24hr_change=true`
    );
    return [await resp.json()];
  } catch (e) {
    return [{ error: String(e) }];
  }
}

async function fetchStocks(): Promise<Record<string, unknown>[]> {
  // Yahoo Finance v8 quote endpoint (no API key needed)
  const symbols = config.finance.stocks.join(",");
  try {
    const resp = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${symbols}?interval=1d&range=1d`
    );
    return [await resp.json()];
  } catch (e) {
    return [{ error: String(e) }];
  }
}

async function checkAgent(host: string, port: number): Promise<{ status: string; data?: string }> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 3000);
    const resp = await fetch(`http://${host}:${port}/status`, { signal: controller.signal });
    clearTimeout(timeout);
    const text = await resp.text();
    return { status: "up", data: text };
  } catch {
    return { status: "down" };
  }
}

async function fetchFleetHealth(): Promise<Record<string, unknown>> {
  const results = await Promise.all(
    config.fleet.agents.map(async (a) => ({
      name: a.name,
      host: a.host,
      ...(await checkAgent(a.host, a.port)),
    }))
  );
  return { agents: results, timestamp: new Date().toISOString() };
}

async function fetchSystemMetrics(): Promise<Record<string, unknown>> {
  // Local system metrics from /proc
  try {
    const [memRaw, loadRaw, uptimeRaw, dfOut] = await Promise.all([
      Deno.readTextFile("/proc/meminfo").catch(() => ""),
      Deno.readTextFile("/proc/loadavg").catch(() => ""),
      Deno.readTextFile("/proc/uptime").catch(() => ""),
      new Deno.Command("df", { args: ["-h", "/"], stdout: "piped" }).output().then(
        (o) => new TextDecoder().decode(o.stdout)
      ).catch(() => ""),
    ]);

    const memTotal = parseInt(memRaw.match(/MemTotal:\s+(\d+)/)?.[1] || "0") / 1024;
    const memAvail = parseInt(memRaw.match(/MemAvailable:\s+(\d+)/)?.[1] || "0") / 1024;
    const load = loadRaw.split(" ").slice(0, 3).map(Number);
    const uptimeSecs = parseFloat(uptimeRaw.split(" ")[0] || "0");
    const days = Math.floor(uptimeSecs / 86400);
    const hours = Math.floor((uptimeSecs % 86400) / 3600);

    // Parse df output
    const dfLines = dfOut.trim().split("\n");
    const dfData = dfLines[1]?.split(/\s+/) || [];

    return {
      hostname: Deno.hostname?.() || "cnc-server",
      memory: {
        totalMB: Math.round(memTotal),
        availableMB: Math.round(memAvail),
        usedPercent: Math.round(((memTotal - memAvail) / memTotal) * 100),
      },
      load: { "1m": load[0], "5m": load[1], "15m": load[2] },
      uptime: `${days}d ${hours}h`,
      disk: { size: dfData[1], used: dfData[2], avail: dfData[3], usePercent: dfData[4] },
    };
  } catch (e) {
    return { error: String(e) };
  }
}

// --- HTTP Router ---

async function handler(req: Request): Promise<Response> {
  const url = new URL(req.url);
  const path = url.pathname;
  const method = req.method;

  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (method === "OPTIONS") return new Response(null, { headers: cors });

  const json = (data: unknown, status = 200) =>
    new Response(JSON.stringify(data), {
      status,
      headers: { "Content-Type": "application/json", ...cors },
    });

  try {
    // API routes
    if (path === "/api/weather") return json(await fetchWeather());
    if (path === "/api/forecast") return json(await fetchForecast());
    if (path === "/api/crypto") return json(await fetchCrypto());
    if (path === "/api/stocks") return json(await fetchStocks());
    if (path === "/api/fleet") return json(await fetchFleetHealth());
    if (path === "/api/metrics") return json(await fetchSystemMetrics());

    // Tasks CRUD
    if (path === "/api/tasks" && method === "GET") return json(config.tasks);
    if (path === "/api/tasks" && method === "POST") {
      const body = await req.json();
      const task: Task = {
        id: crypto.randomUUID(),
        text: body.text,
        done: false,
        created: new Date().toISOString(),
      };
      config.tasks.push(task);
      await saveConfig(config);
      return json(task, 201);
    }
    if (path.startsWith("/api/tasks/") && method === "PUT") {
      const id = path.split("/")[3];
      const body = await req.json();
      const task = config.tasks.find((t) => t.id === id);
      if (!task) return json({ error: "not found" }, 404);
      if (body.text !== undefined) task.text = body.text;
      if (body.done !== undefined) task.done = body.done;
      await saveConfig(config);
      return json(task);
    }
    if (path.startsWith("/api/tasks/") && method === "DELETE") {
      const id = path.split("/")[3];
      config.tasks = config.tasks.filter((t) => t.id !== id);
      await saveConfig(config);
      return json({ ok: true });
    }

    // Habits CRUD
    if (path === "/api/habits" && method === "GET") return json(config.habits);
    if (path === "/api/habits" && method === "POST") {
      const body = await req.json();
      const habit: Habit = { id: crypto.randomUUID(), name: body.name, log: [] };
      config.habits.push(habit);
      await saveConfig(config);
      return json(habit, 201);
    }
    if (path.startsWith("/api/habits/") && path.endsWith("/log") && method === "POST") {
      const id = path.split("/")[3];
      const habit = config.habits.find((h) => h.id === id);
      if (!habit) return json({ error: "not found" }, 404);
      const today = new Date().toISOString().split("T")[0];
      if (!habit.log.includes(today)) habit.log.push(today);
      await saveConfig(config);
      return json(habit);
    }
    if (path.startsWith("/api/habits/") && !path.endsWith("/log") && method === "DELETE") {
      const id = path.split("/")[3];
      config.habits = config.habits.filter((h) => h.id !== id);
      await saveConfig(config);
      return json({ ok: true });
    }

    // Config endpoint
    if (path === "/api/config" && method === "GET") {
      // Return config without sensitive keys
      const safe = { ...config, weather: { ...config.weather, apiKey: config.weather.apiKey ? "***" : "" } };
      return json(safe);
    }
    if (path === "/api/config" && method === "PUT") {
      const body = await req.json();
      if (body.weather) {
        if (body.weather.lat) config.weather.lat = body.weather.lat;
        if (body.weather.lon) config.weather.lon = body.weather.lon;
        if (body.weather.apiKey) config.weather.apiKey = body.weather.apiKey;
        if (body.weather.units) config.weather.units = body.weather.units;
      }
      if (body.finance) {
        if (body.finance.stocks) config.finance.stocks = body.finance.stocks;
        if (body.finance.crypto) config.finance.crypto = body.finance.crypto;
      }
      await saveConfig(config);
      return json({ ok: true });
    }

    // Serve static frontend
    if (path === "/" || path === "/index.html") {
      const html = await Deno.readTextFile(new URL("./index.html", import.meta.url).pathname);
      return new Response(html, { headers: { "Content-Type": "text/html" } });
    }

    return new Response("Not Found", { status: 404 });
  } catch (e) {
    console.error(e);
    return json({ error: String(e) }, 500);
  }
}

// --- Start ---
config = await loadConfig();
console.log(`Dashboard server running on http://0.0.0.0:${PORT}`);
Deno.serve({ port: PORT, hostname: "0.0.0.0" }, handler);
