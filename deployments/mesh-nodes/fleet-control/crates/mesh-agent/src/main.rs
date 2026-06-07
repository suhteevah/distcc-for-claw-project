mod audit;
mod command;
mod config;
mod exec;
mod heartbeat;
mod probe;
mod run;
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .init();
    let cfg = config::AgentConfig::from_env()?;
    tracing::info!(node = %cfg.node, "mesh-agent starting v{}", env!("CARGO_PKG_VERSION"));
    run::serve(cfg).await
}
