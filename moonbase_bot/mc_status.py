"""
Pure-Python Minecraft Server Status & Query Client (Server List Ping / SLP).
Queries server status, online players, MOTD, version, and latency without dependencies.
"""

import json
import socket
import struct
import time
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PlayerSample:
    name: str
    id: str


@dataclass
class MinecraftServerStatus:
    online: bool
    latency_ms: float = 0.0
    version_name: str = "Unknown"
    protocol_version: int = 0
    players_online: int = 0
    players_max: int = 0
    player_samples: List[PlayerSample] = field(default_factory=list)
    motd: str = ""
    error: Optional[str] = None


def _encode_varint(val: int) -> bytes:
    """Encode an integer as a Minecraft VarInt."""
    total = b""
    while True:
        byte = val & 0x7F
        val >>= 7
        if val:
            total += struct.pack("!B", byte | 0x80)
        else:
            total += struct.pack("!B", byte)
            break
    return total


def _decode_varint(sock: socket.socket) -> int:
    """Decode a Minecraft VarInt from a socket."""
    val = 0
    for i in range(5):
        raw = sock.recv(1)
        if not raw:
            raise ConnectionError("Socket closed while reading VarInt")
        byte = ord(raw)
        val |= (byte & 0x7F) << (7 * i)
        if not (byte & 0x80):
            break
    return val


def _read_exact(sock: socket.socket, num_bytes: int) -> bytes:
    """Read an exact number of bytes."""
    data = b""
    while len(data) < num_bytes:
        chunk = sock.recv(num_bytes - len(data))
        if not chunk:
            raise ConnectionError("Premature end of stream")
        data += chunk
    return data


def query_server_status(host: str = "127.0.0.1", port: int = 25565, timeout: float = 3.0) -> MinecraftServerStatus:
    """
    Ping and query a Minecraft server using standard Server List Ping.
    Returns structured status with latency and player list.
    """
    start_time = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)

            # Build Handshake Packet (ID = 0x00)
            host_bytes = host.encode("utf-8")
            handshake_payload = (
                b"\x00"  # Packet ID 0
                + _encode_varint(47)  # Protocol version (47 works for 1.8 - 1.20+ for status)
                + _encode_varint(len(host_bytes))
                + host_bytes
                + struct.pack("!H", port)
                + _encode_varint(1)  # Next state: 1 (status)
            )
            handshake_packet = _encode_varint(len(handshake_payload)) + handshake_payload
            sock.sendall(handshake_packet)

            # Build Status Request Packet (ID = 0x00, empty payload)
            request_packet = _encode_varint(1) + b"\x00"
            sock.sendall(request_packet)

            # Read Response
            _ = _decode_varint(sock)  # Packet length
            packet_id = _decode_varint(sock)
            if packet_id != 0:
                raise ValueError(f"Unexpected packet ID {packet_id} in status response")

            json_len = _decode_varint(sock)
            raw_json = _read_exact(sock, json_len).decode("utf-8", errors="replace")
            latency_ms = round((time.time() - start_time) * 1000, 2)

            data = json.loads(raw_json)

            # Parse MOTD (can be string or dict component)
            motd_raw = data.get("description", "")
            if isinstance(motd_raw, dict):
                motd = motd_raw.get("text", "")
                if "extra" in motd_raw and isinstance(motd_raw["extra"], list):
                    for part in motd_raw["extra"]:
                        if isinstance(part, dict):
                            motd += part.get("text", "")
                        elif isinstance(part, str):
                            motd += part
            else:
                motd = str(motd_raw)

            players_info = data.get("players", {})
            version_info = data.get("version", {})

            player_samples = []
            for sample in players_info.get("sample", []):
                player_samples.append(
                    PlayerSample(name=sample.get("name", "Unknown"), id=sample.get("id", ""))
                )

            return MinecraftServerStatus(
                online=True,
                latency_ms=latency_ms,
                version_name=version_info.get("name", "Unknown"),
                protocol_version=version_info.get("protocol", 0),
                players_online=players_info.get("online", 0),
                players_max=players_info.get("max", 0),
                player_samples=player_samples,
                motd=motd.strip(),
            )
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return MinecraftServerStatus(
            online=False,
            latency_ms=latency_ms,
            error=str(e),
        )
