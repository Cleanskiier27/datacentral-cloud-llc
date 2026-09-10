# MOONBASE.BOT / BUSTER.BOT Guide

## Overview

**MOONBASE.BOT** (also known as **BUSTER.BOT**) is an autonomous sentinel and bridge system connecting an open-world Minecraft server to Discord. Built directly into the NetworkBuster architecture, it integrates:
- **Discord Community Sentinel**: Real-time server telemetry, player queries, and administrative RCON commands.
- **Bidirectional Chat Bridge**: Relays messages between Discord channels and Minecraft in-game chat.
- **Moonbase Alpha Saga Integration**: Imbued with the lore of Moonbase Alpha, Network Buster spacecraft, Dr. Aris Thorne, and Thomas the Chief Systems Engineer.
- **Space Economy Tokens**: Powered by NetworkBuster's personal access token manager (`token_manager.py`).

---

## Architecture & Directory Structure

```
f:\datacentral-cloud-llc/
├── moonbase_bot/              # Core bot package
│   ├── __init__.py           # Package exports
│   ├── config.py             # Environment & configuration loader
│   ├── mc_rcon.py            # RFC-compliant binary Minecraft RCON client
│   ├── mc_status.py          # Pure Python Server List Ping (SLP) client
│   ├── avatar_bridge.py      # NetworkBuster Avatar & Moonbase Alpha lore bridge
│   └── discord_bot.py        # Discord bot client & command dispatcher
├── buster_bot/               # Compatibility alias forwarding to moonbase_bot
│   └── __init__.py
├── moonbase_bot.py           # Primary executable runner (Discord & CLI simulation)
├── BUSTER_BOT.py             # Interoperable alias runner
├── test_moonbase_bot.py      # Automated test suite
├── docker-compose.minecraft.yml # Complete open-world server + bot Docker stack
├── Dockerfile.moonbase       # Container definition for MOONBASE.BOT
├── .env.minecraft.example    # Configuration template
├── scripts/
│   ├── build_moonbase_bot.py # Cross-platform build script
│   └── build_distro.py       # Distribution builder (--type moonbase)
└── dist/                     # Generated release zip archives
```

---

## Quick Start

### 1. Configuration

Copy the example environment file:
```powershell
Copy-Item .env.minecraft.example .env.minecraft
```

Configure your Discord bot token and channels inside `.env.minecraft`:
```ini
DISCORD_BOT_TOKEN=your_token_from_discord_portal
DISCORD_CHAT_CHANNEL_ID=123456789012345678
MINECRAFT_HOST=127.0.0.1
MINECRAFT_QUERY_PORT=25565
MINECRAFT_RCON_PORT=25575
MINECRAFT_RCON_PASSWORD=BusterOpenWorld2026!
```

### 2. Run in Standalone CLI Mode

If you don't have a Discord bot token configured yet, you can run the bot in interactive CLI simulation mode:
```powershell
python moonbase_bot.py --cli
# or
python BUSTER_BOT.py --cli
```

### 3. Check Server Status

Check real-time telemetry non-interactively:
```powershell
python moonbase_bot.py --status
```

---

## Building MOONBASE.BOT

You can build and package release distributions using any of the following methods:

### Method 1: Dedicated Build Pipeline (Recommended)
```powershell
python scripts/build_moonbase_bot.py
```
This runs the test suite, validates components, and creates a timestamped zip archive in `dist/` (e.g. `dist/moonbase-bot-YYYYMMDD-HHMMSS.zip`).

### Method 2: NetworkBuster Distribution Builder
```powershell
python scripts/build_distro.py --type moonbase
```

### Method 3: Make (Linux / macOS / WSL)
```bash
make build
# or
make moonbase.bot
```

### Method 4: Local WebApp Control Center
1. Open **http://localhost:5000** in your browser.
2. Under FlashCommands, click **Execute** on **Build MOONBASE.BOT** or **BUSTER.BOT Status**.

---

## Open-World Minecraft Server Deployment (Docker)

To launch the open-world Minecraft server alongside MOONBASE.BOT in Docker:

```powershell
docker compose -f docker-compose.minecraft.yml up -d
```

This starts:
1. `moonbase-minecraft-server`: Paper 1.20+ Minecraft server with survival mode, 4GB RAM, RCON enabled, and world storage persisted in `./minecraft-data`.
2. `moonbase-discord-bot`: MOONBASE.BOT connected to the server network.

To view logs:
```powershell
docker compose -f docker-compose.minecraft.yml logs -f
```

To stop:
```powershell
docker compose -f docker-compose.minecraft.yml down
```

---

## Discord & In-Game Command Reference

| Command | Description | Example |
| :--- | :--- | :--- |
| `!status` | Real-time Minecraft server status, ping, and player count | `!status` |
| `!players` | Current players active in the open world | `!players` |
| `!say <msg>` | Broadcast an announcement from Discord to in-game chat | `!say Welcome pioneers!` |
| `!cmd <rcon>` | Admin RCON console command (Requires admin privileges) | `!cmd time set day` |
| `!spawn` | Show Moonbase Alpha core spawn coordinates & compass radar | `!spawn` |
| `!moonbase` | Transmit Moonbase Alpha lore & Lost Project archives | `!moonbase` |
| `!buster` | Interactive dialogue with BUSTER.BOT AI sentinel | `!buster` |
| `!token` | Space economy tokens (`create`, `list`) | `!token create Player1` |
| `!map` | URL link to live web map | `!map` |

---

## Space Economy Token System

Players can be granted Personal Access Tokens for API automation, web store rewards, and in-game achievements using:
```text
!token create <player_name> [scope]
```
Standard scopes supported:
- `space_economy_tax_metrics`: Access to space-based economic metrics and resource trade.
- `purchasing_economy`: Access to procurement and base barter markets.

---

## Testing

Run the automated test suite at any time:
```powershell
python -m unittest test_moonbase_bot.py
```
