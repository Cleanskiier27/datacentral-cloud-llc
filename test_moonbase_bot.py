"""
Automated unit and integration tests for MOONBASE.BOT / BUSTER.BOT.
Tests RCON packet framing, VarInt encoding, Avatar lore bridge,
TokenManager space economy, and command dispatching.
"""

import io
import os
import struct
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from moonbase_bot.config import BotConfig
from moonbase_bot.mc_rcon import MinecraftRconClient, RconAuthError, RconError
from moonbase_bot.mc_status import (
    _decode_varint,
    _encode_varint,
    query_server_status,
    MinecraftServerStatus,
)
from moonbase_bot.avatar_bridge import MoonbaseAvatarBridge
from moonbase_bot.discord_bot import MoonbaseBotEngine
import buster_bot


class TestMinecraftProtocols(unittest.TestCase):
    """Test binary Minecraft networking protocols (RCON and VarInt)."""

    def test_varint_encoding_and_decoding(self):
        test_values = [0, 1, 2, 127, 128, 255, 25565, 2097151]
        for val in test_values:
            encoded = _encode_varint(val)
            self.assertIsInstance(encoded, bytes)
            # Decode via mock socket
            sock = MagicMock()
            sock.recv.side_effect = [bytes([b]) for b in encoded]
            decoded = _decode_varint(sock)
            self.assertEqual(val, decoded, f"VarInt mismatch for {val}")

    def test_rcon_packet_framing(self):
        client = MinecraftRconClient(host="127.0.0.1", port=25575, password="test")
        mock_sock = MagicMock()
        client._sock = mock_sock

        req_id = 42
        packet_type = MinecraftRconClient.SERVERDATA_EXECCOMMAND
        payload = "time set day"

        client._send_packet(req_id, packet_type, payload)

        self.assertTrue(mock_sock.sendall.called)
        sent_data = mock_sock.sendall.call_args[0][0]

        # Verify header structure: Length(4), ReqID(4), Type(4)
        length, sent_req_id, sent_type = struct.unpack("<iii", sent_data[:12])
        self.assertEqual(sent_req_id, req_id)
        self.assertEqual(sent_type, packet_type)
        self.assertEqual(length, len(sent_data) - 4)
        # Ends with two null bytes
        self.assertEqual(sent_data[-2:], b"\x00\x00")


class TestAvatarLoreBridge(unittest.TestCase):
    """Test Avatar and Moonbase Alpha lore bridge."""

    def setUp(self):
        self.bridge = MoonbaseAvatarBridge()

    def test_greetings_and_lore(self):
        greeting = self.bridge.get_greeting()
        self.assertTrue(any(kw in greeting for kw in ("ONLINE", "READY", "TRANSMISSION")))

        lore = self.bridge.get_lore_entry()
        self.assertTrue(len(lore) > 20)
        self.assertTrue(any(kw in lore for kw in ("Moonbase", "Network Buster", "Thomas", "Aris", "Fracture", "Log")))

        tip = self.bridge.get_survival_tip()
        self.assertTrue(len(tip) > 15)

    def test_embed_formatting(self):
        embed = self.bridge.format_discord_embed_dict("Test Title", "Test Desc", "ARIS")
        self.assertIn("title", embed)
        self.assertIn("description", embed)
        self.assertEqual(embed["color"], 0x3A6EA5)


class TestBotCommandEngine(unittest.TestCase):
    """Test MoonbaseBotEngine command dispatcher."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.token_file = os.path.join(self.temp_dir.name, "test_tokens.json")
        self.config = BotConfig(
            discord_token="",
            discord_guild_id=None,
            chat_channel_id=None,
            log_channel_id=None,
            admin_channel_id=None,
            command_prefix="!",
            mc_host="127.0.0.1",
            mc_query_port=25565,
            mc_rcon_port=25575,
            mc_rcon_password="secret_password",
            mc_world_name="MoonbaseAlpha_OpenWorld",
            server_motd="Moonbase Alpha Test",
            spawn_coords="X: 0, Y: 64, Z: 0",
            map_url="http://localhost:8100",
            token_storage_path=self.token_file,
            default_token_reward=50,
        )
        self.engine = MoonbaseBotEngine(self.config)
        self.engine.market_mgr.ledger = {"balances": {}, "purchases": []}

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_offline_status_command(self):
        # Server is not running on 25565, should gracefully return offline status
        res = self.engine.process_command("status")
        self.assertFalse(res["success"])
        self.assertIn("Offline", res["title"])

    def test_spawn_and_coords_command(self):
        res = self.engine.process_command("spawn")
        self.assertTrue(res["success"])
        self.assertIn("X: 0, Y: 64, Z: 0", res["text"])
        self.assertIn("MoonbaseAlpha_OpenWorld", res["text"])

    def test_moonbase_lore_command(self):
        res = self.engine.process_command("moonbase")
        self.assertTrue(res["success"])
        self.assertIn("Transmission from Moonbase Alpha", res["text"])

    def test_buster_avatar_command(self):
        res = self.engine.process_command("buster")
        self.assertTrue(res["success"])
        self.assertIn("BUSTER.BOT", res["text"])

    def test_token_space_economy_lifecycle(self):
        # Create token
        res_create = self.engine.process_command("token", ["create", "ExplorerOne", "space_economy_tax_metrics"])
        self.assertTrue(res_create["success"])
        self.assertIn("Token Created for ExplorerOne", res_create["text"])

        # List tokens
        res_list = self.engine.process_command("token", ["list"])
        self.assertTrue(res_list["success"])
        self.assertIn("minecraft_ExplorerOne", res_list["text"])

    def test_alias_buster_bot(self):
        # Verify buster_bot package exports the exact same classes
        self.assertEqual(buster_bot.MoonbaseBotEngine, MoonbaseBotEngine)
        self.assertEqual(buster_bot.MinecraftRconClient, MinecraftRconClient)

    def test_marketplace_browse_and_purchase(self):
        # Test browsing marketplace items
        res_market = self.engine.process_command("market")
        self.assertTrue(res_market["success"])
        self.assertIn("Moonbase Alpha Space Economy Marketplace", res_market["text"])
        self.assertIn("lunar_pickaxe", res_market["text"])

        # Test purchasing an affordable item (rations_crate = 40 tokens, player starting balance = 100)
        res_buy = self.engine.process_command("buy", ["rations_crate", "TestPioneer"])
        self.assertTrue(res_buy["success"])
        self.assertIn("Purchase Successful", res_buy["text"])
        self.assertIn("60", res_buy["text"])

        # Test inventory check
        res_inv = self.engine.process_command("inventory", ["TestPioneer"])
        self.assertTrue(res_inv["success"])
        self.assertIn("Hydroponic Rations Crate", res_inv["text"])

        # Test purchasing expensive item without enough tokens
        res_fail = self.engine.process_command("buy", ["lost_project_core", "TestPioneer"])
        self.assertFalse(res_fail["success"])
        self.assertIn("Insufficient tokens", res_fail["text"])


if __name__ == "__main__":
    unittest.main()
