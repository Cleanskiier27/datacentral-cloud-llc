"""
Avatar Bridge for MOONBASE.BOT / BUSTER.BOT.
Bridges NetworkBuster's core Avatar companion system with Moonbase Alpha saga lore
and open-world Minecraft survival interactions.
"""

import os
import random
import sys
from typing import Dict, List, Optional

# Ensure core is importable
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

try:
    from core.avatar import Avatar, AvatarMood, AvatarState
except ImportError:
    # Graceful fallback if standalone
    class AvatarMood:
        NEUTRAL = "neutral"
        HAPPY = "happy"
        THINKING = "thinking"
        ALERT = "alert"
        WORKING = "working"
        SUCCESS = "success"
        ERROR = "error"

    class AvatarState:
        IDLE = "idle"
        MONITORING = "monitoring"
        PROCESSING = "processing"
        ANALYZING = "analyzing"
        ALERTING = "alerting"

    class Avatar:
        def __init__(self, name="BUSTER"):
            self.name = name
            self.state = AvatarState.IDLE
            self.mood = AvatarMood.NEUTRAL


class MoonbaseAvatarBridge:
    """
    Manages AI persona dialogues, lore broadcasts, and player survival tips
    for the open-world Minecraft server and Discord community.
    """

    CHARACTERS = {
        "BUSTER": {
            "title": "BUSTER.BOT // Moonbase Sentinel",
            "color": 0x00FF88,  # Neon Green
            "icon": "🤖",
        },
        "ARIS": {
            "title": "Dr. Aris Thorne // Lead Resonance Physicist",
            "color": 0x3A6EA5,  # Deep Tech Blue
            "icon": "🔬",
        },
        "THOMAS": {
            "title": "Thomas // Chief Systems Engineer",
            "color": 0xD4AF37,  # Lunar Gold
            "icon": "🛠️",
        },
    }

    SURVIVAL_TIPS = [
        "Oxygen levels optimal. Remember to build your lunar airlock before venturing into unshielded craters.",
        "Deepslate mining resonance detected at Y: -54. Keep torches lit to avoid subterranean hostile spawns.",
        "The Network Buster spacecraft thrives on fuel refinement. Smelt ancient debris to bolster alloy shielding.",
        "Lunar eclipse phase active: Nether portals stabilize faster under moonlight. Secure your base perimeter.",
        "Moonbase Alpha perimeter beacon online at spawn (0, 64, 0). Restock supplies at the central hub.",
        "Thomas recommends crafting Diamond or Netherite pickaxes before attempting to breach meteor crusts.",
        "Dr. Thorne notes: 'The Lost Project isn't just an artifact—it adapts to the builder's imagination.'",
    ]

    LORE_ENTRIES = [
        "**Log 01 - The Fracture:** After Earth's ecological collapse, Network Buster breached the toxic stratosphere, rewrote local aerodynamics, and charted the course to Moonbase Alpha.",
        "**Log 14 - The Resonance:** Dr. Aris Thorne discovered that the Lost Project shifts between cube, sphere, and pyramid, vibrating at the harmonic frequency of quantum belief.",
        "**Log 27 - The Engineers:** Thomas confirmed that the spacecraft's alloys reconfigure according to the pilot's heart rate. Science and craft are two sides of the same coin.",
        "**Log 42 - The Outpost:** Moonbase Alpha stands eternal. From here, new worlds are forged block by block.",
    ]

    def __init__(self):
        self.avatar = Avatar(name="BUSTER.BOT")

    def get_greeting(self) -> str:
        greetings = [
            "🚀 **[MOONBASE.BOT ONLINE]** All systems nominal. Welcome to the Moonbase Alpha open world!",
            "🤖 **[BUSTER.BOT READY]** Monitoring Minecraft telemetry and Discord comms. Awaiting orders.",
            "🌌 **[TRANSMISSION RECEIVED]** Relaying from Moonbase Alpha Station. Comms channel active.",
        ]
        return random.choice(greetings)

    def get_survival_tip(self) -> str:
        return random.choice(self.SURVIVAL_TIPS)

    def get_lore_entry(self) -> str:
        return random.choice(self.LORE_ENTRIES)

    def format_status_dialogue(self, online_players: int, latency_ms: float) -> str:
        if online_players == 0:
            return (
                f"📡 **BUSTER.BOT Status Report:**\n"
                f"• Server Status: **ONLINE** (Ping: `{latency_ms}ms`)\n"
                f"• Open World Sector: *Quiet. No pioneers currently deployed.*\n"
                f"• System Advisory: *{self.get_survival_tip()}*"
            )
        else:
            return (
                f"🚀 **BUSTER.BOT Active Sector Alert:**\n"
                f"• Server Status: **ONLINE** (Ping: `{latency_ms}ms`)\n"
                f"• Active Pioneers: **{online_players}** explorer(s) currently in the open world.\n"
                f"• Life Support: All lunar base hubs operating at 100% efficiency."
            )

    def format_discord_embed_dict(self, title: str, description: str, character: str = "BUSTER") -> Dict:
        char_info = self.CHARACTERS.get(character, self.CHARACTERS["BUSTER"])
        return {
            "title": f"{char_info['icon']} {title}",
            "description": description,
            "color": char_info["color"],
            "footer": {"text": char_info["title"]},
        }
