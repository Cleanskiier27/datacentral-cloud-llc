"""
Pure-Python Minecraft RCON (Remote Console) Client.
Compliant with Source RCON protocol specification. No external dependencies required.
"""

import socket
import struct
from typing import Optional, Tuple


class RconError(Exception):
    """Base exception for RCON communication errors."""
    pass


class RconAuthError(RconError):
    """Authentication failed exception."""
    pass


class MinecraftRconClient:
    """
    RCON client for Minecraft servers.
    Provides thread-safe or direct socket communication to issue console commands.
    """

    # Packet types
    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0

    def __init__(self, host: str = "127.0.0.1", port: int = 25575, password: str = "", timeout: float = 5.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id = (self._req_id + 1) & 0x7FFFFFFF
        return self._req_id

    def connect(self) -> bool:
        """Establish TCP connection and authenticate with the Minecraft server."""
        self.disconnect()
        try:
            self._sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self._sock.settimeout(self.timeout)
            # Authenticate
            req_id = self._next_id()
            self._send_packet(req_id, self.SERVERDATA_AUTH, self.password)
            
            # Auth response
            resp_id, resp_type, _ = self._read_packet()
            if resp_id == -1 or resp_type != self.SERVERDATA_AUTH_RESPONSE:
                self.disconnect()
                raise RconAuthError("RCON authentication rejected by Minecraft server.")
            return True
        except (socket.error, OSError) as e:
            self.disconnect()
            raise RconError(f"Failed to connect to RCON server {self.host}:{self.port}: {e}")

    def disconnect(self) -> None:
        """Close socket connection if open."""
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def execute(self, command: str) -> str:
        """
        Execute an administrative command on the Minecraft server and return the response text.
        Automatically connects if not already connected.
        """
        if not self._sock:
            self.connect()

        req_id = self._next_id()
        self._send_packet(req_id, self.SERVERDATA_EXECCOMMAND, command)

        resp_id, resp_type, payload = self._read_packet()
        if resp_id != req_id and resp_id != 0:
            pass  # Some server implementations return 0 or mirror req_id
        return payload

    def _send_packet(self, req_id: int, packet_type: int, payload: str) -> None:
        """Encode and send binary RCON packet."""
        payload_bytes = payload.encode("utf-8")
        packet_len = 4 + 4 + len(payload_bytes) + 2  # req_id(4) + type(4) + payload + 2 null bytes
        header = struct.pack("<iii", packet_len, req_id, packet_type)
        packet = header + payload_bytes + b"\x00\x00"
        self._sock.sendall(packet)

    def _read_packet(self) -> Tuple[int, int, str]:
        """Read and decode binary RCON packet from server."""
        raw_len = self._recv_exact(4)
        packet_len = struct.unpack("<i", raw_len)[0]
        if packet_len < 10 or packet_len > 40960:
            raise RconError(f"Invalid RCON packet length: {packet_len}")

        body = self._recv_exact(packet_len)
        req_id, packet_type = struct.unpack("<ii", body[:8])
        # Payload is up to the first null byte after 8-byte header
        payload_bytes = body[8:-2]  # strip the 2 trailing nulls
        try:
            payload = payload_bytes.decode("utf-8", errors="replace").strip()
        except Exception:
            payload = payload_bytes.decode("latin1", errors="replace").strip()
        return req_id, packet_type, payload

    def _recv_exact(self, num_bytes: int) -> bytes:
        """Receive exact number of bytes from socket."""
        chunks = []
        bytes_left = num_bytes
        while bytes_left > 0:
            chunk = self._sock.recv(min(bytes_left, 4096))
            if not chunk:
                raise RconError("Connection closed prematurely by Minecraft RCON server.")
            chunks.append(chunk)
            bytes_left -= len(chunk)
        return b"".join(chunks)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
