mod api;
mod audit;
mod config;
mod dispatch;
mod metrics;
mod nats;
mod notify;
mod presence;
use anyhow::Result;

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .init();
    let cfg = config::ControllerConfig::from_env()?;
    tracing::info!("fleet-controller v{} starting", env!("CARGO_PKG_VERSION"));
    api::run(cfg).await
}
