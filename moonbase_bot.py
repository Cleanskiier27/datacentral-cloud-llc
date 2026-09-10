#!/usr/bin/env python3
"""
MOONBASE.BOT / BUSTER.BOT - Main Entry Point.
Launches the Discord bot gateway or CLI administrative console for the open-world Minecraft server.
"""

import argparse
import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from moonbase_bot.config import load_config
from moonbase_bot.discord_bot import MoonbaseBotEngine, create_discord_client, HAS_DISCORD


def print_banner():
    banner = r"""
  __  __  ____   ____  _   _ ____    _    ____  _____   ____   ___ _____ 
 |  \/  |/ __ \ / __ \| \ | | __ )  / \  / ___|| ____| | __ ) / _ \_   _|
 | |\/| | |  | | |  | |  \| |  _ \ / _ \ \___ \|  _|   |  _ \| | | || |  
 | |  | | |__| | |__| | |\  | |_) / ___ \ ___) | |___  | |_) | |_| || |  
 |_|  |_|\____/ \____/|_| \_|____/_/   \_\____/|_____| |____/ \___/ |_|  
                                                                          
       🚀 Open World Minecraft Server Sentinel & Discord Bridge 🤖
    """
    print(banner)


def run_cli_interactive(engine: MoonbaseBotEngine):
    """Run an interactive CLI session to issue commands to Minecraft and BUSTER.BOT."""
    print("=" * 65)
    print("Interactive CLI Console Mode active.")
    print("Type '!status', '!players', '!say <msg>', '!cmd <command>', '!token', or '!exit'.")
    print("=" * 65)

    while True:
        try:
            line = input("\n[MOONBASE.BOT] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting BUSTER.BOT console.")
            break

        if not line:
            continue
        if line.lower() in ("exit", "quit", "!exit", "!quit"):
            print("Shutting down console session.")
            break

        if line.startswith("!"):
            line = line[1:]

        parts = line.split()
        cmd = parts[0]
        args = parts[1:]

        result = engine.process_command(cmd, args)
        print(result["text"])


def main():
    parser = argparse.ArgumentParser(description="MOONBASE.BOT / BUSTER.BOT Open World Minecraft Discord Sentinel")
    parser.add_argument("--cli", action="store_true", help="Launch interactive CLI console mode")
    parser.add_argument("--status", action="store_true", help="Check Minecraft server status and exit")
    parser.add_argument("--command", type=str, help="Execute a single BUSTER.BOT command and exit")
    args = parser.parse_args()

    print_banner()
    config = load_config()
    engine = MoonbaseBotEngine(config)

    if args.status:
        res = engine.process_command("status")
        print(res["text"])
        sys.exit(0 if res.get("success") else 1)

    if args.command:
        parts = args.command.strip().split()
        cmd = parts[0].lstrip("!")
        cmd_args = parts[1:]
        res = engine.process_command(cmd, cmd_args)
        print(res["text"])
        sys.exit(0 if res.get("success") else 1)

    if args.cli or not config.discord_token:
        if not config.discord_token:
            print("ℹ️  DISCORD_BOT_TOKEN is not set.")
            print("   Set DISCORD_BOT_TOKEN in .env.minecraft or environment to connect to Discord.")
            print("   Starting in interactive CLI simulation mode...\n")
        run_cli_interactive(engine)
        return

    if not HAS_DISCORD:
        print("⚠️  discord.py is not installed in current Python environment.")
        print("   Install it with: pip install discord.py")
        print("   Falling back to interactive CLI console mode...\n")
        run_cli_interactive(engine)
        return

    print("🛰️  Starting Discord Gateway client...")
    client = create_discord_client(engine)
    try:
        client.run(config.discord_token)
    except Exception as e:
        print(f"❌ Discord Gateway error: {e}")
        print("   Falling back to CLI console mode...")
        run_cli_interactive(engine)


if __name__ == "__main__":
    main()
