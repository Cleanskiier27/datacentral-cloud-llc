"""
BUSTER.BOT alias package forwarding to moonbase_bot.
Ensures full compatibility with both naming conventions.
"""

from moonbase_bot import *
from moonbase_bot.config import BotConfig, load_config
from moonbase_bot.mc_rcon import MinecraftRconClient, RconError
from moonbase_bot.mc_status import MinecraftServerStatus, query_server_status
from moonbase_bot.avatar_bridge import MoonbaseAvatarBridge
from moonbase_bot.discord_bot import MoonbaseBotEngine, create_discord_client
