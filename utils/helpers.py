"""
NetworkBuster Software - Helper Utilities
Common helper functions used throughout the application
"""

import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def timestamp_now() -> str:
    """Get current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def parse_log_line(line: str) -> dict:
    """Parse a log line and extract common components."""
    result = {
        "raw": line.strip(),
        "timestamp": None,
        "level": None,
        "message": line.strip(),
    }
    
    # Try to extract timestamp (common formats)
    timestamp_patterns = [
        r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})",  # 2024-01-28 20:48:51
        r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2})",  # 01/28/2024 20:48:51
        r"\[(\d{2}:\d{2}:\d{2})\]",                   # [20:48:51]
    ]
    
    for pattern in timestamp_patterns:
        match = re.search(pattern, line)
        if match:
            result["timestamp"] = match.group(1)
            break
    
    # Try to extract log level
    level_patterns = [
        (r"\b(ERROR|CRITICAL|FATAL)\b", "error"),
        (r"\b(WARNING|WARN)\b", "warning"),
        (r"\b(INFO)\b", "info"),
        (r"\b(DEBUG)\b", "debug"),
    ]
    
    for pattern, level in level_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            result["level"] = level
            break
    
    return result


def hash_string(text: str) -> str:
    """Generate MD5 hash of a string."""
    return hashlib.md5(text.encode()).hexdigest()


def safe_json_loads(text: str, default: Any = None) -> Any:
    """Safely parse JSON string."""
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, pretty: bool = False) -> str:
    """Safely convert object to JSON string."""
    try:
        if pretty:
            return json.dumps(obj, indent=2, default=str)
        return json.dumps(obj, default=str)
    except (TypeError, ValueError):
        return "{}"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate a string to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_file_size(path: Path) -> int:
    """Get file size in bytes, returns 0 if file doesn't exist."""
    try:
        return path.stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, create if it doesn't."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_file_lines(path: Path, max_lines: int = 100, from_end: bool = True) -> list:
    """Read lines from a file, optionally from the end."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            if from_end:
                return lines[-max_lines:]
            return lines[:max_lines]
    except (OSError, FileNotFoundError):
        return []
