# OpenClaw Podman Deployment Reference

*Scraped from https://docs.openclaw.ai/install/podman — March 2026*

## Setup
```bash
./setup-podman.sh           # One-time init
./setup-podman.sh --quadlet # With systemd auto-restart
```

## The openclaw User
- System user with `nologin` shell
- Home: `/home/openclaw`
- Config at `~/.openclaw`
- Requires subuid/subgid: `openclaw:100000:65536` in `/etc/subuid` and `/etc/subgid`

## Systemd Quadlet
Config: `~openclaw/.config/containers/systemd/openclaw.container`

```bash
sudo systemctl --machine openclaw@ --user start openclaw.service
sudo systemctl --machine openclaw@ --user stop openclaw.service
sudo systemctl --machine openclaw@ --user status openclaw.service
journalctl -u openclaw.service -f
```

## Launch
```bash
./scripts/run-openclaw-podman.sh launch        # Manual
./scripts/run-openclaw-podman.sh launch setup   # With wizard
```

## Port Overrides
- `OPENCLAW_PODMAN_GATEWAY_HOST_PORT` (default: 18789)
- `OPENCLAW_PODMAN_BRIDGE_HOST_PORT` (default: 18790)

## Gateway Binding
Default: `--bind loopback`. For LAN: `OPENCLAW_GATEWAY_BIND=lan`

## Path Overrides
- `OPENCLAW_CONFIG_DIR`
- `OPENCLAW_WORKSPACE_DIR`

## Storage
- Persistent: config and workspace bind-mounted
- Ephemeral: tmpfs for sandbox containers

## Troubleshooting
1. Permission errors → verify ownership matches executing user
2. Gateway won't start → confirm `gateway.mode="local"`
3. Rootless fails → check `/etc/subuid` and `/etc/subgid`
4. Cgroups → must be v2: `podman info --format '{{.Host.CgroupsVersion}}'`
