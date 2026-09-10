"""
Discord Bot and CLI Engine for MOONBASE.BOT / BUSTER.BOT.
Provides Discord slash and prefix commands, chat bridge to Minecraft,
RCON server control, and space economy tokens.
"""

import asyncio
import os
import sys
from typing import Dict, List, Optional, Tuple

# Ensure parent directory is in sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from moonbase_bot.config import BotConfig, load_config
from moonbase_bot.mc_rcon import MinecraftRconClient, RconError
from moonbase_bot.mc_status import MinecraftServerStatus, query_server_status
from moonbase_bot.avatar_bridge import MoonbaseAvatarBridge
from moonbase_bot.marketplace import MarketplaceManager
from token_manager import TokenManager

try:
    import discord
    from discord.ext import commands, tasks
    HAS_DISCORD = True
except ImportError:
    HAS_DISCORD = False


class MoonbaseBotEngine:
    """
    Unified command execution engine for MOONBASE.BOT / BUSTER.BOT.
    Handles command logic independently so it works both via Discord Gateway
    and via standalone CLI / Test mode.
    """

    def __init__(self, config: Optional[BotConfig] = None):
        self.config = config or load_config()
        self.bridge = MoonbaseAvatarBridge()
        self.token_mgr = TokenManager(storage_path=self.config.token_storage_path)
        rcon = MinecraftRconClient(
            host=self.config.mc_host,
            port=self.config.mc_rcon_port,
            password=self.config.mc_rcon_password,
        )
        self.market_mgr = MarketplaceManager(rcon_client=rcon)

    def get_server_status(self) -> MinecraftServerStatus:
        """Query live Minecraft server status via Server List Ping."""
        return query_server_status(
            host=self.config.mc_host,
            port=self.config.mc_query_port,
        )

    def execute_rcon_command(self, command: str) -> str:
        """Execute command on Minecraft server via RCON."""
        client = MinecraftRconClient(
            host=self.config.mc_host,
            port=self.config.mc_rcon_port,
            password=self.config.mc_rcon_password,
        )
        with client:
            return client.execute(command)

    def broadcast_to_minecraft(self, sender: str, message: str) -> str:
        """Broadcast Discord message to Minecraft in-game chat."""
        safe_sender = sender.replace('"', '\\"')
        safe_msg = message.replace('"', '\\"')
        # Use Minecraft tellraw for rich JSON formatting
        tellraw_cmd = (
            f'tellraw @a ["", {{"text":"[Discord] ","color":"aqua","bold":true}}, '
            f'{{"text":"<{safe_sender}> ","color":"gold"}}, '
            f'{{"text":"{safe_msg}","color":"white"}}]'
        )
        try:
            return self.execute_rcon_command(tellraw_cmd)
        except Exception as e:
            # Fallback to standard /say if tellraw fails
            fallback_cmd = f"say [Discord] <{safe_sender}> {safe_msg}"
            return self.execute_rcon_command(fallback_cmd)

    def process_command(self, cmd_name: str, args: List[str] = None) -> Dict:
        """
        Core command dispatcher.
        Returns a dict with formatted response text, embed data, and status.
        """
        args = args or []
        cmd = cmd_name.lower().strip()

        if cmd in ("status", "mc-status", "ping"):
            status = self.get_server_status()
            if status.online:
                desc = (
                    f"**MOTD:** {status.motd or 'Open World Survival'}\n"
                    f"**Players:** `{status.players_online} / {status.players_max}`\n"
                    f"**Ping / Latency:** `{status.latency_ms} ms`\n"
                    f"**Version:** `{status.version_name}`\n\n"
                    f"*{self.bridge.get_survival_tip()}*"
                )
                return {
                    "success": True,
                    "title": "🟢 Minecraft Server Online",
                    "text": desc,
                    "embed": self.bridge.format_discord_embed_dict(
                        "Moonbase Alpha Server Status: ONLINE", desc, "BUSTER"
                    ),
                    "status_obj": status,
                }
            else:
                desc = (
                    f"**Server:** `{self.config.mc_host}:{self.config.mc_query_port}`\n"
                    f"**Status:** `OFFLINE` or unreachable\n"
                    f"**Detail:** {status.error or 'Connection timed out'}\n\n"
                    f"💡 *Tip: Start the server using docker-compose or local Java launcher.*"
                )
                return {
                    "success": False,
                    "title": "🔴 Minecraft Server Offline",
                    "text": desc,
                    "embed": self.bridge.format_discord_embed_dict(
                        "Moonbase Alpha Server Status: OFFLINE", desc, "THOMAS"
                    ),
                    "status_obj": status,
                }

        elif cmd in ("players", "mc-players", "list"):
            status = self.get_server_status()
            if not status.online:
                return {
                    "success": False,
                    "title": "Server Offline",
                    "text": "Cannot fetch player list: Minecraft server is offline.",
                }
            if not status.player_samples:
                msg = f"No pioneers currently online in the open world ({status.players_online}/{status.players_max})."
            else:
                names = ", ".join(f"`{p.name}`" for p in status.player_samples)
                msg = f"**Pioneers Online ({status.players_online}/{status.players_max}):**\n{names}"
            return {
                "success": True,
                "title": "Active Explorers",
                "text": msg,
                "embed": self.bridge.format_discord_embed_dict("Active Explorers", msg, "BUSTER"),
            }

        elif cmd in ("say", "broadcast", "shout"):
            if not args:
                return {"success": False, "text": "Usage: !say <message>"}
            message = " ".join(args)
            try:
                self.broadcast_to_minecraft("Discord Admin", message)
                return {"success": True, "text": f"📢 Broadcasted to Minecraft world: \"{message}\""}
            except Exception as e:
                return {"success": False, "text": f"Failed to broadcast via RCON: {e}"}

        elif cmd in ("cmd", "rcon", "mc-cmd"):
            if not args:
                return {"success": False, "text": "Usage: !cmd <minecraft command> (e.g., !cmd time set day)"}
            rcon_cmd = " ".join(args)
            try:
                response = self.execute_rcon_command(rcon_cmd)
                return {
                    "success": True,
                    "text": f"**Command Executed:** `{rcon_cmd}`\n```\n{response or 'Done.'}\n```",
                }
            except Exception as e:
                return {"success": False, "text": f"RCON execution error: {e}"}

        elif cmd in ("spawn", "coords", "loc"):
            msg = (
                f"**Moonbase Alpha Main Spawn:** `{self.config.spawn_coords}`\n"
                f"**World Matrix:** `{self.config.mc_world_name}`\n"
                f"**Map Radar:** [Live Web Map]({self.config.map_url})\n\n"
                f"🛡️ *Spawn chunk features protected airlocks, barter trading posts, and storage lockers.*"
            )
            return {
                "success": True,
                "title": "Spawn & World Coordinates",
                "text": msg,
                "embed": self.bridge.format_discord_embed_dict("World Telemetry & Coordinates", msg, "THOMAS"),
            }

        elif cmd in ("moonbase", "lore", "saga"):
            lore = self.bridge.get_lore_entry()
            tip = self.bridge.get_survival_tip()
            text = f"**Transmission from Moonbase Alpha Archive:**\n\n{lore}\n\n*Surveillance Note:* {tip}"
            return {
                "success": True,
                "title": "Moonbase Alpha - The Everlasting Saga",
                "text": text,
                "embed": self.bridge.format_discord_embed_dict("Moonbase Alpha Transmission", text, "ARIS"),
            }

        elif cmd in ("avatar", "buster"):
            status = self.get_server_status()
            text = self.bridge.format_status_dialogue(
                status.players_online if status.online else 0,
                status.latency_ms if status.online else 0.0,
            )
            return {
                "success": True,
                "title": "BUSTER.BOT Interactive Sentience",
                "text": text,
                "embed": self.bridge.format_discord_embed_dict("BUSTER.BOT Dialogue", text, "BUSTER"),
            }

        elif cmd in ("token", "tokens", "economy"):
            subcmd = args[0].lower() if args else "help"
            if subcmd == "create" and len(args) >= 2:
                player = args[1]
                scope = args[2] if len(args) > 2 else "space_economy_tax_metrics"
                token_val = self.token_mgr.generate_token(
                    name=f"minecraft_{player}",
                    scopes=[scope] if scope in self.token_mgr.STANDARD_SCOPES else list(self.token_mgr.STANDARD_SCOPES.keys()),
                    expiry_days=30,
                )
                return {
                    "success": True,
                    "text": f"🪙 **Token Created for {player}:**\n`{token_val}`\nKeep this secret! Used for automated bot APIs and rewards.",
                }
            elif subcmd == "list":
                tokens = self.token_mgr.list_tokens()
                if not tokens:
                    return {"success": True, "text": "No active player tokens found in space economy registry."}
                lines = [f"• `{t['name']}` (Scopes: `{', '.join(t.get('scopes', []))}`)" for t in tokens]
                return {"success": True, "text": "**Active Space Economy Tokens:**\n" + "\n".join(lines)}
            else:
                help_text = (
                    "**Space Economy Token Commands:**\n"
                    "• `!token create <player_name> [scope]` - Issue personal token for in-game rewards/API\n"
                    "• `!token list` - List active tokens\n"
                    "• Standard Scopes: `purchasing_economy`, `space_economy_tax_metrics`"
                )
                return {"success": True, "text": help_text}

        elif cmd in ("market", "shop", "store"):
            category = args[0] if args else None
            items = self.market_mgr.get_items(category)
            lines = [f"• **{it['item_id']}** - {it['icon']} {it['name']} (`{it['price_tokens']}` tokens)\n  *{it['description'][:60]}*" for it in items]
            msg = "**🛒 Moonbase Alpha Space Economy Marketplace:**\n\n" + "\n".join(lines) + "\n\n💡 *Use `!buy <item_id> [player]` to purchase with in-game delivery.*"
            return {
                "success": True,
                "title": "Space Economy Marketplace",
                "text": msg,
                "embed": self.bridge.format_discord_embed_dict("Marketplace Catalog", msg, "BUSTER"),
            }

        elif cmd in ("buy", "purchase"):
            if not args:
                return {"success": False, "text": "Usage: `!buy <item_id> [minecraft_player_name]`"}
            item_id = args[0]
            player = args[1] if len(args) > 1 else "Explorer"
            result = self.market_mgr.purchase_item(player_name=player, item_id=item_id, quantity=1)
            if result.get("success"):
                tx_msg = (
                    f"✅ **Purchase Successful!**\n"
                    f"• Item: **{result['item_name']}**\n"
                    f"• Pioneer: `{player}`\n"
                    f"• Tokens Deducted: 🪙 `{result['tokens_spent']}`\n"
                    f"• Balance Remaining: 🪙 `{result['remaining_balance']}`\n"
                    f"• Status: *{result['delivery_status']}*"
                )
                return {
                    "success": True,
                    "title": "Purchase Order Confirmed",
                    "text": tx_msg,
                    "embed": self.bridge.format_discord_embed_dict("Invoice Receipt", tx_msg, "THOMAS"),
                }
            else:
                return {"success": False, "text": f"❌ Purchase failed: {result.get('error')}"}

        elif cmd in ("inventory", "inv"):
            player = args[0] if args else "Explorer"
            inv = self.market_mgr.get_player_inventory(player)
            balance = self.market_mgr.get_player_balance(player)
            if not inv:
                msg = f"🎒 **Inventory for {player}:** Empty (Current Balance: 🪙 `{balance}` tokens)."
            else:
                lines = [f"• {p['item_name']} (Qty: {p['quantity']}, Spent: {p['tokens_spent']} tokens)" for p in inv]
                msg = f"🎒 **Inventory for {player}** (Balance: 🪙 `{balance}` tokens):\n" + "\n".join(lines)
            return {
                "success": True,
                "title": f"Inventory: {player}",
                "text": msg,
                "embed": self.bridge.format_discord_embed_dict(f"Inventory: {player}", msg, "BUSTER"),
            }

        elif cmd in ("map", "livemap", "radar"):
            return {
                "success": True,
                "text": f"🗺️ **Open World Live Map:** {self.config.map_url}",
            }

        elif cmd in ("help", "commands"):
            help_msg = (
                "**🚀 MOONBASE.BOT / BUSTER.BOT Commands:**\n"
                "• `!status` - Check Minecraft server online status, ping, and player count\n"
                "• `!players` - View current players active in the open world\n"
                "• `!market` - Browse space economy marketplace gear, artifacts, and perks\n"
                "• `!buy <item_id> [player]` - Purchase marketplace item with in-game RCON delivery\n"
                "• `!inventory [player]` - View player's purchased gear and token balance\n"
                "• `!say <message>` - Broadcast Discord message into Minecraft chat\n"
                "• `!cmd <command>` - Execute administrative RCON server command\n"
                "• `!spawn` - View world spawn and base coordinates\n"
                "• `!moonbase` - Transmit Moonbase Alpha lore & saga archives\n"
                "• `!buster` - Interactive dialogue with BUSTER.BOT AI sentinel\n"
                "• `!token` - Manage space-economy player tokens\n"
                "• `!map` - View world web map URL"
            )
            return {"success": True, "text": help_msg}

        else:
            return {
                "success": False,
                "text": f"Unknown command `{cmd}`. Type `!help` for available BUSTER.BOT commands.",
            }


def create_discord_client(engine: MoonbaseBotEngine):
    """Factory to construct discord.py Bot client if discord package is available."""
    if not HAS_DISCORD:
        return None

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=engine.config.command_prefix, intents=intents)

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} has connected to Discord Gateway!")
        print(f"   Command Prefix: {engine.config.command_prefix}")
        try:
            synced = await bot.tree.sync()
            print(f"   Synced {len(synced)} slash commands.")
        except Exception as e:
            print(f"   Slash command sync note: {e}")

    @bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return

        # Bridge Discord chat in configured channel to Minecraft
        if engine.config.chat_channel_id and message.channel.id == engine.config.chat_channel_id:
            if not message.content.startswith(engine.config.command_prefix):
                try:
                    engine.broadcast_to_minecraft(message.author.display_name, message.content)
                except Exception:
                    pass

        await bot.process_commands(message)

    @bot.command(name="status")
    async def cmd_status(ctx):
        res = engine.process_command("status")
        if "embed" in res:
            e = discord.Embed(
                title=res["embed"]["title"],
                description=res["embed"]["description"],
                color=res["embed"]["color"],
            )
            await ctx.send(embed=e)
        else:
            await ctx.send(res["text"])

    @bot.command(name="players")
    async def cmd_players(ctx):
        res = engine.process_command("players")
        await ctx.send(res["text"])

    @bot.command(name="say")
    async def cmd_say(ctx, *, message: str):
        res = engine.process_command("say", [message])
        await ctx.send(res["text"])

    @bot.command(name="cmd")
    @commands.has_permissions(administrator=True)
    async def cmd_cmd(ctx, *, command_str: str):
        res = engine.process_command("cmd", command_str.split())
        await ctx.send(res["text"])

    @bot.command(name="spawn")
    async def cmd_spawn(ctx):
        res = engine.process_command("spawn")
        await ctx.send(res["text"])

    @bot.command(name="moonbase")
    async def cmd_moonbase(ctx):
        res = engine.process_command("moonbase")
        await ctx.send(res["text"])

    @bot.command(name="buster")
    async def cmd_buster(ctx):
        res = engine.process_command("buster")
        await ctx.send(res["text"])

    @bot.command(name="token")
    async def cmd_token(ctx, *args):
        res = engine.process_command("token", list(args))
        await ctx.send(res["text"])

    @bot.command(name="map")
    async def cmd_map(ctx):
        res = engine.process_command("map")
        await ctx.send(res["text"])

    @bot.command(name="market")
    async def cmd_market(ctx, category: Optional[str] = None):
        res = engine.process_command("market", [category] if category else [])
        await ctx.send(res["text"])

    @bot.command(name="buy")
    async def cmd_buy(ctx, item_id: str, player: Optional[str] = None):
        target_player = player or ctx.author.display_name
        res = engine.process_command("buy", [item_id, target_player])
        await ctx.send(res["text"])

    @bot.command(name="inventory")
    async def cmd_inventory(ctx, player: Optional[str] = None):
        target_player = player or ctx.author.display_name
        res = engine.process_command("inventory", [target_player])
        await ctx.send(res["text"])

    return bot
