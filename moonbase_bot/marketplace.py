"""
Marketplace Subsystem for NetworkBuster & MOONBASE.BOT.
Manages the Open World Space Economy catalog, token pricing, player purchasing,
in-game Minecraft RCON item delivery, and transaction ledgers.
"""

import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from token_manager import TokenManager
from moonbase_bot.mc_rcon import MinecraftRconClient, RconError


@dataclass
class MarketplaceItem:
    item_id: str
    name: str
    category: str  # "gear", "perks", "artifacts", "supplies"
    price_tokens: int
    description: str
    minecraft_command: str
    icon: str = "📦"
    stock: int = -1  # -1 = unlimited


# Default catalog for the Moonbase Alpha open-world server
DEFAULT_CATALOG: List[MarketplaceItem] = [
    MarketplaceItem(
        item_id="lunar_pickaxe",
        name="Quantum Plasma Pickaxe",
        category="gear",
        price_tokens=150,
        description="Netherite Pickaxe infused with Efficiency V, Fortune III, and Unbreaking III.",
        minecraft_command='give {player} netherite_pickaxe[custom_name=\'{"text":"Quantum Plasma Pickaxe","color":"aqua","bold":true}\',enchantments={levels:{"minecraft:efficiency":5,"minecraft:fortune":3,"minecraft:unbreaking":3}}] 1',
        icon="⛏️",
    ),
    MarketplaceItem(
        item_id="oxygen_tank",
        name="Pressurized Oxygen Rig",
        category="gear",
        price_tokens=100,
        description="Netherite Helmet with Respiration III, Aqua Affinity, and Night Vision aura.",
        minecraft_command='give {player} netherite_helmet[custom_name=\'{"text":"Pressurized Oxygen Rig","color":"blue","bold":true}\',enchantments={levels:{"minecraft:respiration":3,"minecraft:aqua_affinity":1,"minecraft:unbreaking":3}}] 1',
        icon="🤿",
    ),
    MarketplaceItem(
        item_id="starlight_elytra",
        name="Starlight Warp Wings",
        category="gear",
        price_tokens=300,
        description="Aerodynamic Elytra with Unbreaking III and Mending for open-world gliding.",
        minecraft_command='give {player} elytra[custom_name=\'{"text":"Starlight Warp Wings","color":"light_purple","bold":true}\',enchantments={levels:{"minecraft:unbreaking":3,"minecraft:mending":1}}] 1',
        icon="🪽",
    ),
    MarketplaceItem(
        item_id="antigravity_boots",
        name="Anti-Gravity Thruster Boots",
        category="gear",
        price_tokens=120,
        description="Netherite Boots with Feather Falling IV and Depth Strider III.",
        minecraft_command='give {player} netherite_boots[custom_name=\'{"text":"Anti-Gravity Thruster Boots","color":"gold","bold":true}\',enchantments={levels:{"minecraft:feather_falling":4,"minecraft:depth_strider":3}}] 1',
        icon="🥾",
    ),
    MarketplaceItem(
        item_id="lost_project_core",
        name="Lost Project Resonance Core",
        category="artifacts",
        price_tokens=500,
        description="Ancient Moonbase artifact: Nether Star pulsing with quantum resonance energy.",
        minecraft_command='give {player} nether_star[custom_name=\'{"text":"Lost Project Resonance Core","color":"dark_purple","bold":true}\'] 1',
        icon="🔮",
    ),
    MarketplaceItem(
        item_id="beacon_pack",
        name="Moonbase Station Beacon Kit",
        category="artifacts",
        price_tokens=350,
        description="1 Beacon + 16 Iron Blocks to establish your lunar perimeter base.",
        minecraft_command='give {player} beacon 1; give {player} iron_block 16',
        icon="📡",
    ),
    MarketplaceItem(
        item_id="rations_crate",
        name="Hydroponic Rations Crate",
        category="supplies",
        price_tokens=40,
        description="32 Golden Carrots and 4 Enchanted Golden Apples for expedition endurance.",
        minecraft_command='give {player} golden_carrot 32; give {player} enchanted_golden_apple 4',
        icon="🥕",
    ),
    MarketplaceItem(
        item_id="pioneer_vip",
        name="Moonbase Pioneer VIP Status",
        category="perks",
        price_tokens=250,
        description="Grants [Pioneer] in-game title, colored chat prefix, and priority login queue.",
        minecraft_command='tellraw @a ["", {"text":"[Moonbase Announce] ","color":"gold","bold":true}, {"text":"{player} has been promoted to Moonbase Pioneer VIP!","color":"green"}]',
        icon="⭐",
    ),
    MarketplaceItem(
        item_id="nasa_telemetry_array",
        name="NASA Deep Research Telemetry Array",
        category="artifacts",
        price_tokens=780,
        description="Classified multi-spectrum lunar scanner enabling Deep Research Mode, artifact detection, and scientific yield boosts.",
        minecraft_command='give {player} recovery_compass[custom_name=\'{"text":"NASA Deep Research Telemetry Array","color":"gold","bold":true}\',lore=[\'{"text":"Classified multi-spectrum lunar scanner","color":"yellow"}\',\'{"text":"Enables Deep Research Mode & artifact detection","color":"aqua"}\'],enchantments={levels:{"minecraft:unbreaking":10}}] 1; tellraw @a ["", {"text":"[Moonbase Science Alert] ","color":"gold","bold":true}, {"text":"{player} has deployed the NASA Deep Research Telemetry Array!","color":"aqua"}]',
        icon="📡",
    ),
]


class MarketplaceManager:
    """Manages the catalog, transactions, and Minecraft RCON deliveries."""

    def __init__(self, ledger_path: str = "marketplace_ledger.json", rcon_client: Optional[MinecraftRconClient] = None):
        self.ledger_path = ledger_path
        self.rcon_client = rcon_client
        self.items: Dict[str, MarketplaceItem] = {item.item_id: item for item in DEFAULT_CATALOG}
        self.token_mgr = TokenManager()
        self.ledger = self._load_ledger()

    def _load_ledger(self) -> Dict[str, Any]:
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"balances": {}, "purchases": []}

    def _save_ledger(self) -> None:
        try:
            with open(self.ledger_path, "w", encoding="utf-8") as f:
                json.dump(self.ledger, f, indent=2)
        except Exception:
            pass

    def get_items(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return all catalog items, optionally filtered by category."""
        results = []
        for item in self.items.values():
            if not category or item.category.lower() == category.lower():
                results.append(asdict(item))
        return results

    def get_item(self, item_id: str) -> Optional[MarketplaceItem]:
        return self.items.get(item_id)

    def get_player_balance(self, player_name: str) -> int:
        """Get player token balance from the ledger, defaulting to 100 starter tokens."""
        return self.ledger["balances"].get(player_name, 100)

    def add_player_balance(self, player_name: str, amount: int) -> int:
        current = self.get_player_balance(player_name)
        new_balance = max(0, current + amount)
        self.ledger["balances"][player_name] = new_balance
        self._save_ledger()
        return new_balance

    def purchase_item(
        self,
        player_name: str,
        item_id: str,
        token_str: Optional[str] = None,
        quantity: int = 1,
    ) -> Dict[str, Any]:
        """
        Execute a purchase:
        1. Validates the item exists and is in stock.
        2. Validates personal access token if provided, or uses player ledger balance.
        3. Deducts tokens.
        4. Triggers Minecraft RCON command to deliver items in-game.
        5. Logs transaction to ledger.
        """
        item = self.get_item(item_id)
        if not item:
            return {"success": False, "error": f"Item '{item_id}' does not exist in marketplace."}

        if item.stock != -1 and item.stock < quantity:
            return {"success": False, "error": f"Item '{item.name}' is out of stock."}

        total_price = item.price_tokens * quantity

        # Authentication: if token provided, validate scope
        if token_str:
            is_valid = self.token_mgr.validate_token(token_str)
            if not is_valid:
                return {"success": False, "error": "Invalid or expired personal access token."}
            scopes = self.token_mgr.get_token_scopes(token_str) or []
            if "purchasing_economy" not in scopes and "space_economy_tax_metrics" not in scopes:
                return {"success": False, "error": "Token missing required scope: 'purchasing_economy'."}

        # Check and deduct balance
        current_balance = self.get_player_balance(player_name)
        if current_balance < total_price:
            return {
                "success": False,
                "error": f"Insufficient tokens. Required: {total_price}, Current Balance: {current_balance}.",
                "required": total_price,
                "balance": current_balance,
            }

        new_balance = self.add_player_balance(player_name, -total_price)

        if item.stock != -1:
            item.stock -= quantity

        # In-Game Delivery via Minecraft RCON
        delivery_status = "Not delivered (RCON unavailable)"
        if self.rcon_client:
            try:
                # Commands may contain multiple instructions separated by semicolons
                raw_cmds = item.minecraft_command.split(";")
                results = []
                for raw_cmd in raw_cmds:
                    formatted_cmd = raw_cmd.strip().format(player=player_name)
                    res = self.rcon_client.execute(formatted_cmd)
                    results.append(res)
                delivery_status = "Delivered in-game via RCON: " + "; ".join(results)
            except Exception as e:
                delivery_status = f"Delivery queued (RCON error: {e})"

        # Record purchase
        tx_id = f"tx_{int(time.time())}_{player_name[:4]}"
        tx_record = {
            "tx_id": tx_id,
            "player": player_name,
            "item_id": item.item_id,
            "item_name": item.name,
            "quantity": quantity,
            "tokens_spent": total_price,
            "remaining_balance": new_balance,
            "delivery_status": delivery_status,
            "timestamp": time.time(),
        }
        self.ledger["purchases"].append(tx_record)
        self._save_ledger()

        return {
            "success": True,
            "tx_id": tx_id,
            "item_name": item.name,
            "quantity": quantity,
            "tokens_spent": total_price,
            "remaining_balance": new_balance,
            "delivery_status": delivery_status,
        }

    def get_player_inventory(self, player_name: str) -> List[Dict[str, Any]]:
        """Return all purchases made by a player."""
        return [
            p for p in self.ledger.get("purchases", [])
            if p.get("player", "").lower() == player_name.lower()
        ]
