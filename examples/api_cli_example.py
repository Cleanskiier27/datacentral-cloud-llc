#!/usr/bin/env python3
"""
NetworkBuster & MOONBASE.BOT - API Command Line Interface (CLI) Example.
Demonstrates how to interact with the NetworkBuster WebApp REST API via CLI.
Supports both non-interactive commands and an interactive REPL console.
Uses standard library urllib for zero external dependencies.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

# Ensure UTF-8 console encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class NetworkBusterApiClient:
    """Client for interacting with the NetworkBuster REST API."""

    def __init__(self, base_url: str = "http://localhost:5000", timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def check_health(self) -> bool:
        """Check if the API server is reachable."""
        try:
            req = urllib.request.Request(f"{self.base_url}/", headers={"User-Agent": "NetworkBuster-CLI/1.0"})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

    def get_distro_info(self) -> Dict[str, Any]:
        """Fetch list of built distributions from GET /distro-info."""
        url = f"{self.base_url}/distro-info"
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkBuster-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def execute_command(self, cmd_id: str) -> Dict[str, Any]:
        """Execute a flash command via POST /execute/<cmd_id>."""
        url = f"{self.base_url}/execute/{cmd_id}"
        req = urllib.request.Request(
            url,
            data=b"{}",
            headers={"Content-Type": "application/json", "User-Agent": "NetworkBuster-CLI/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def download_latest_distro(self, output_dir: str = "./downloads") -> str:
        """Download latest distribution archive from GET /download."""
        url = f"{self.base_url}/download"
        os.makedirs(output_dir, exist_ok=True)

        req = urllib.request.Request(url, headers={"User-Agent": "NetworkBuster-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            content_disp = resp.headers.get("Content-Disposition", "")
            filename = "networkbuster-distro.zip"
            if "download_name=" in content_disp:
                filename = content_disp.split("download_name=")[-1].strip("\"' ")
            elif "filename=" in content_disp:
                filename = content_disp.split("filename=")[-1].strip("\"' ")

            target_path = os.path.join(output_dir, filename)
            with open(target_path, "wb") as f:
                f.write(resp.read())
            return target_path

    # --- Marketplace REST API Methods ---

    def get_marketplace_items(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Fetch open-world marketplace items from GET /api/marketplace/items."""
        url = f"{self.base_url}/api/marketplace/items"
        if category:
            url += f"?category={urllib.parse.quote(category)}"
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkBuster-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_player_balance(self, player_name: str) -> Dict[str, Any]:
        """Get player token balance from GET /api/marketplace/balance/<player>."""
        url = f"{self.base_url}/api/marketplace/balance/{urllib.parse.quote(player_name)}"
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkBuster-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_player_inventory(self, player_name: str) -> Dict[str, Any]:
        """Get player purchase history from GET /api/marketplace/inventory/<player>."""
        url = f"{self.base_url}/api/marketplace/inventory/{urllib.parse.quote(player_name)}"
        req = urllib.request.Request(url, headers={"User-Agent": "NetworkBuster-CLI/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def buy_marketplace_item(
        self,
        player_name: str,
        item_id: str,
        token_str: Optional[str] = None,
        quantity: int = 1,
    ) -> Dict[str, Any]:
        """Purchase an item and trigger in-game RCON delivery via POST /api/marketplace/buy."""
        url = f"{self.base_url}/api/marketplace/buy"
        payload = json.dumps({
            "player": player_name,
            "item_id": item_id,
            "token": token_str,
            "quantity": quantity,
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "NetworkBuster-CLI/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))


def print_banner(base_url: str):
    banner = rf"""
  _   _ _____ _______        _____  ____  _  __ ____  _   _ ____ _____ _____ ____  
 | \ | | ____|_   _\ \      / / _ \|  _ \| |/ /| __ )| | | / ___|_   _| ____|  _ \ 
 |  \| |  _|   | |  \ \ /\ / / | | | |_) | ' / |  _ \| | | \___ \ | | |  _| | |_) |
 | |\  | |___  | |   \ V  V /| |_| |  _ <| . \ | |_) | |_| |___) || | | |___|  _ < 
 |_| \_|_____| |_|    \_/\_/  \___/|_| \_\_|\_\|____/ \___/|____/ |_| |_____|_| \_\
                                                                                    
            🚀 REST API Command-Line Interface (Connected to: {base_url})
    """
    print(banner)


def cmd_status(client: NetworkBusterApiClient):
    """Check API server health and run buster_status command."""
    print("🛰️  Checking API Server Connection...")
    if not client.check_health():
        print(f"❌ Could not connect to API server at {client.base_url}")
        print("   Make sure the server is running (python webapp/app.py).")
        return

    print(f"✅ Connected to API server: {client.base_url}")
    print("\n📡 Querying BUSTER.BOT & Minecraft Server Telemetry via API...")
    try:
        res = client.execute_command("buster_status")
        print("\n--- Telemetry Output ---")
        print(res.get("stdout", "").strip() or "No output returned.")
        if res.get("stderr"):
            print("Stderr:", res["stderr"])
    except Exception as e:
        print(f"❌ Error querying status: {e}")


def cmd_distros(client: NetworkBusterApiClient):
    """List available distributions from API."""
    print("📦 Querying Available Distributions from API...")
    try:
        data = client.get_distro_info()
        if data.get("status") == "no_distro" or not data.get("distros"):
            print("ℹ️  No distributions built yet. Run 'exec moonbase_build' to package one.")
            return

        print(f"Found {len(data['distros'])} distribution archive(s):\n")
        print(f"{'Archive Name':<38} {'Size (MB)':<12} {'Created (Timestamp)'}")
        print("-" * 70)
        for d in data["distros"]:
            created_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d["created"]))
            print(f"{d['name']:<38} {d['size_mb']:<12} {created_str}")
    except Exception as e:
        print(f"❌ Error fetching distro info: {e}")


def cmd_exec(client: NetworkBusterApiClient, cmd_id: str):
    """Execute a flash command via API."""
    print(f"⚡ Executing command '{cmd_id}' via POST /execute/{cmd_id}...")
    start_time = time.time()
    try:
        res = client.execute_command(cmd_id)
        elapsed = round(time.time() - start_time, 2)
        status_label = "✅ SUCCESS" if res.get("status") == "success" else "⚠️ FAILED / NOTICE"
        print(f"\n{status_label} (Elapsed: {elapsed}s, Code: {res.get('returncode', 0)})")
        if res.get("stdout"):
            print("\n[STDOUT]:")
            print(res["stdout"].strip())
        if res.get("stderr"):
            print("\n[STDERR]:")
            print(res["stderr"].strip())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        try:
            err_body = json.loads(e.read().decode())
            print("   Message:", err_body.get("message", "Unknown error"))
        except Exception:
            pass
    except Exception as e:
        print(f"❌ Execution error: {e}")


def cmd_download(client: NetworkBusterApiClient, output_dir: str = "./downloads"):
    """Download the latest distribution package via API."""
    print(f"📥 Downloading latest distribution package from {client.base_url}/download...")
    try:
        saved_file = client.download_latest_distro(output_dir)
        size_kb = round(os.path.getsize(saved_file) / 1024, 2)
        print(f"✅ Download complete!")
        print(f"   Saved to: {os.path.abspath(saved_file)}")
        print(f"   Size:     {size_kb} KB")
    except urllib.error.HTTPError as e:
        print(f"❌ Download failed (HTTP {e.code}): {e.reason}")
    except Exception as e:
        print(f"❌ Error downloading distribution: {e}")


# --- Marketplace CLI Commands ---

def cmd_market(client: NetworkBusterApiClient, category: Optional[str] = None):
    """Browse open-world marketplace items from API."""
    print("🛒 Querying Open-World Space Economy Marketplace...")
    try:
        data = client.get_marketplace_items(category)
        items = data.get("items", [])
        if not items:
            print("ℹ️  No items found in marketplace.")
            return

        print(f"\nFound {len(items)} item(s) in catalog:\n")
        print(f"{'ID':<20} {'Name':<28} {'Category':<12} {'Tokens':<8} {'Description'}")
        print("-" * 95)
        for it in items:
            desc_short = it['description'][:45] + ("..." if len(it['description']) > 45 else "")
            icon_name = f"{it.get('icon', '📦')} {it['name']}"
            print(f"{it['item_id']:<20} {icon_name:<28} {it['category']:<12} {it['price_tokens']:<8} {desc_short}")
        print("\n💡 Purchase an item using: buy <item_id> --player <your_minecraft_name>")
    except Exception as e:
        print(f"❌ Error fetching marketplace items: {e}")


def cmd_buy(
    client: NetworkBusterApiClient,
    item_id: str,
    player_name: str,
    token_str: Optional[str] = None,
    quantity: int = 1,
):
    """Purchase a marketplace item and trigger in-game delivery."""
    print(f"🛍️  Submitting purchase order for '{item_id}' (Qty: {quantity}) for player '{player_name}'...")
    try:
        res = client.buy_marketplace_item(
            player_name=player_name,
            item_id=item_id,
            token_str=token_str,
            quantity=quantity,
        )
        if res.get("status") == "success":
            tx = res["transaction"]
            print("\n" + "=" * 55)
            print("✅ PURCHASE SUCCESSFUL! INVOICE RECEIPT")
            print("=" * 55)
            print(f"• Transaction ID:     {tx.get('tx_id')}")
            print(f"• Item Purchased:     {tx.get('item_name')}")
            print(f"• Quantity:           {tx.get('quantity')}")
            print(f"• Tokens Spent:       🪙 {tx.get('tokens_spent')}")
            print(f"• Remaining Balance:  🪙 {tx.get('remaining_balance')}")
            print(f"• In-Game Delivery:   {tx.get('delivery_status')}")
            print("=" * 55)
        else:
            print(f"❌ Purchase rejected: {res.get('message', 'Unknown error')}")
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode())
            print(f"❌ Purchase failed (HTTP {e.code}): {err.get('message', e.reason)}")
        except Exception:
            print(f"❌ Purchase failed: HTTP {e.code} {e.reason}")
    except Exception as e:
        print(f"❌ Error executing purchase: {e}")


def cmd_inventory(client: NetworkBusterApiClient, player_name: str):
    """View player purchase history and inventory."""
    print(f"🎒 Fetching inventory & purchase history for '{player_name}'...")
    try:
        data = client.get_player_inventory(player_name)
        purchases = data.get("inventory", [])
        bal_data = client.get_player_balance(player_name)
        balance = bal_data.get("balance", 0)

        print(f"\nExplorer: {player_name} | Current Balance: 🪙 {balance} tokens")
        if not purchases:
            print("ℹ️  No marketplace purchases recorded yet.")
            return

        print(f"\n{'Date/Time':<20} {'Item':<30} {'Qty':<5} {'Cost':<8} {'Status'}")
        print("-" * 80)
        for p in purchases:
            ts_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(p["timestamp"]))
            print(f"{ts_str:<20} {p['item_name']:<30} {p['quantity']:<5} {p['tokens_spent']:<8} {p.get('delivery_status', 'Delivered')[:18]}")
    except Exception as e:
        print(f"❌ Error fetching inventory: {e}")


def cmd_balance(client: NetworkBusterApiClient, player_name: str):
    """Check player token balance."""
    try:
        data = client.get_player_balance(player_name)
        print(f"🪙 Player '{player_name}' Token Balance: {data.get('balance', 0)} tokens")
    except Exception as e:
        print(f"❌ Error querying balance: {e}")


def run_interactive(client: NetworkBusterApiClient):
    """Run interactive REPL console for API commands."""
    print("=" * 70)
    print("Interactive API REPL Mode. Available commands:")
    print("  • status                 - Check API health and Minecraft/BUSTER telemetry")
    print("  • distros                - List built distribution zip packages")
    print("  • exec <cmd_id>          - Execute server command (e.g. exec moonbase_build)")
    print("  • download               - Download latest distribution archive to ./downloads")
    print("  • market [category]      - Browse space economy items (gear, perks, artifacts)")
    print("  • buy <id> <player>      - Purchase marketplace item with in-game RCON delivery")
    print("  • inventory <player>     - View player's purchased gear and transaction history")
    print("  • balance <player>       - View player's token balance")
    print("  • help                   - Show command list")
    print("  • exit / quit            - Exit the CLI")
    print("=" * 70)

    while True:
        try:
            line = input(f"\n[{client.base_url}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting CLI.")
            break

        if not line:
            continue

        parts = line.split()
        subcmd = parts[0].lower()

        if subcmd in ("exit", "quit", "q"):
            print("Exiting API CLI.")
            break
        elif subcmd in ("status", "health", "ping"):
            cmd_status(client)
        elif subcmd in ("distros", "list", "ls"):
            cmd_distros(client)
        elif subcmd == "exec":
            if len(parts) < 2:
                print("Usage: exec <cmd_id> (Available: moonbase_build, buster_status, build, status, web3)")
            else:
                cmd_exec(client, parts[1])
        elif subcmd in ("download", "get"):
            cmd_download(client)
        elif subcmd in ("market", "marketplace", "items", "shop"):
            cat = parts[1] if len(parts) > 1 else None
            cmd_market(client, cat)
        elif subcmd == "buy":
            if len(parts) < 3:
                print("Usage: buy <item_id> <player_name> [quantity]")
            else:
                qty = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 1
                cmd_buy(client, item_id=parts[1], player_name=parts[2], quantity=qty)
        elif subcmd in ("inventory", "inv"):
            if len(parts) < 2:
                print("Usage: inventory <player_name>")
            else:
                cmd_inventory(client, parts[1])
        elif subcmd in ("balance", "bal"):
            if len(parts) < 2:
                print("Usage: balance <player_name>")
            else:
                cmd_balance(client, parts[1])
        elif subcmd in ("help", "?"):
            print("Available commands: status, distros, exec <cmd_id>, download, market, buy, inventory, balance, exit")
        else:
            print(f"Unknown command '{subcmd}'. Type 'help' for available commands.")


def main():
    parser = argparse.ArgumentParser(
        description="NetworkBuster & MOONBASE.BOT REST API Command-Line Interface (CLI)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python examples/api_cli_example.py status
  python examples/api_cli_example.py distros
  python examples/api_cli_example.py market
  python examples/api_cli_example.py market --category gear
  python examples/api_cli_example.py buy lunar_pickaxe --player Pioneer_1
  python examples/api_cli_example.py inventory Pioneer_1
  python examples/api_cli_example.py balance Pioneer_1
  python examples/api_cli_example.py exec moonbase_build
  python examples/api_cli_example.py download
  python examples/api_cli_example.py --interactive
        """
    )
    parser.add_argument(
        "--api-url",
        default=os.environ.get("NETWORKBUSTER_API_URL", "http://localhost:5000"),
        help="Base URL of the NetworkBuster API server (default: http://localhost:5000)",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive REPL console mode",
    )

    subparsers = parser.add_subparsers(dest="command", help="API Command to run")

    # status
    subparsers.add_parser("status", help="Check API health and Minecraft/BUSTER.BOT telemetry")

    # distros
    subparsers.add_parser("distros", help="List available distribution archives from GET /distro-info")

    # exec
    exec_parser = subparsers.add_parser("exec", help="Execute a flash command via POST /execute/<cmd_id>")
    exec_parser.add_argument(
        "cmd_id",
        choices=["moonbase_build", "buster_status", "build", "status", "web3", "train"],
        help="Command identifier to execute on the server",
    )

    # download
    dl_parser = subparsers.add_parser("download", help="Download latest distribution archive from GET /download")
    dl_parser.add_argument(
        "--out",
        default="./downloads",
        help="Directory to save downloaded archive (default: ./downloads)",
    )

    # market
    market_parser = subparsers.add_parser("market", help="Browse space economy marketplace items")
    market_parser.add_argument(
        "--category", "-c",
        choices=["gear", "artifacts", "supplies", "perks"],
        help="Filter items by category",
    )

    # buy
    buy_parser = subparsers.add_parser("buy", help="Purchase an item with in-game RCON delivery")
    buy_parser.add_argument("item_id", help="Marketplace item ID (e.g., lunar_pickaxe, oxygen_tank)")
    buy_parser.add_argument("--player", "-p", default="Pioneer_1", help="Minecraft player name (default: Pioneer_1)")
    buy_parser.add_argument("--token", "-t", help="Optional Personal Access Token with purchasing_economy scope")
    buy_parser.add_argument("--qty", "-q", type=int, default=1, help="Quantity to purchase (default: 1)")

    # inventory
    inv_parser = subparsers.add_parser("inventory", help="View player inventory & purchase history")
    inv_parser.add_argument("player", default="Pioneer_1", nargs="?", help="Minecraft player name")

    # balance
    bal_parser = subparsers.add_parser("balance", help="View player space economy token balance")
    bal_parser.add_argument("player", default="Pioneer_1", nargs="?", help="Minecraft player name")

    args = parser.parse_args()

    print_banner(args.api_url)
    client = NetworkBusterApiClient(base_url=args.api_url)

    if args.interactive or not args.command:
        run_interactive(client)
    elif args.command == "status":
        cmd_status(client)
    elif args.command == "distros":
        cmd_distros(client)
    elif args.command == "exec":
        cmd_exec(client, args.cmd_id)
    elif args.command == "download":
        cmd_download(client, output_dir=args.out)
    elif args.command == "market":
        cmd_market(client, category=args.category)
    elif args.command == "buy":
        cmd_buy(client, item_id=args.item_id, player_name=args.player, token_str=args.token, quantity=args.qty)
    elif args.command == "inventory":
        cmd_inventory(client, player_name=args.player)
    elif args.command == "balance":
        cmd_balance(client, player_name=args.player)


if __name__ == "__main__":
    main()

