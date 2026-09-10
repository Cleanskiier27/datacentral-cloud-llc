"""
Configuration loader for MOONBASE.BOT / BUSTER.BOT.
Loads environment variables for Discord, Minecraft Server, and Space Economy settings.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BotConfig:
    """Bot and server configuration."""
    # Discord Bot Settings
    discord_token: str
    discord_guild_id: Optional[int]
    chat_channel_id: Optional[int]
    log_channel_id: Optional[int]
    admin_channel_id: Optional[int]
    command_prefix: str

    # Minecraft Server Settings
    mc_host: str
    mc_query_port: int
    mc_rcon_port: int
    mc_rcon_password: str
    mc_world_name: str
    server_motd: str

    # Open World & Lore
    spawn_coords: str
    map_url: str

    # Space Economy Tokens
    token_storage_path: str
    default_token_reward: int


def load_config() -> BotConfig:
    """Load configuration from environment variables with safe defaults."""
    # Try loading a local .env file if available
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.minecraft")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("\"'")
                        if k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

    return BotConfig(
        discord_token=os.environ.get("DISCORD_BOT_TOKEN", "").strip(),
        discord_guild_id=int(os.environ.get("DISCORD_GUILD_ID")) if os.environ.get("DISCORD_GUILD_ID") else None,
        chat_channel_id=int(os.environ.get("DISCORD_CHAT_CHANNEL_ID")) if os.environ.get("DISCORD_CHAT_CHANNEL_ID") else None,
        log_channel_id=int(os.environ.get("DISCORD_LOG_CHANNEL_ID")) if os.environ.get("DISCORD_LOG_CHANNEL_ID") else None,
        admin_channel_id=int(os.environ.get("DISCORD_ADMIN_CHANNEL_ID")) if os.environ.get("DISCORD_ADMIN_CHANNEL_ID") else None,
        command_prefix=os.environ.get("BUSTER_BOT_PREFIX", "!").strip(),

        mc_host=os.environ.get("MINECRAFT_HOST", "127.0.0.1").strip(),
        mc_query_port=int(os.environ.get("MINECRAFT_QUERY_PORT", "25565")),
        mc_rcon_port=int(os.environ.get("MINECRAFT_RCON_PORT", "25575")),
        mc_rcon_password=os.environ.get("MINECRAFT_RCON_PASSWORD", "BusterOpenWorld2026!").strip(),
        mc_world_name=os.environ.get("MINECRAFT_WORLD_NAME", "MoonbaseAlpha_OpenWorld").strip(),
        server_motd=os.environ.get(
            "MINECRAFT_SERVER_MOTD",
            "§b§lMOONBASE.BOT §8| §aOpen World Minecraft §8| §eDiscord Integrated"
        ).strip(),

        spawn_coords=os.environ.get("MINECRAFT_SPAWN_COORDS", "X: 0, Y: 64, Z: 0 [Moonbase Core]").strip(),
        map_url=os.environ.get("MINECRAFT_MAP_URL", "http://localhost:8100").strip(),

        token_storage_path=os.environ.get("TOKEN_STORAGE_PATH", "tokens.json").strip(),
        default_token_reward=int(os.environ.get("DEFAULT_TOKEN_REWARD", "50")),
    )
