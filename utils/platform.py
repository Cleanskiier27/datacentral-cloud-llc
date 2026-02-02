"""
NetworkBuster Software - Platform Utilities
Cross-platform compatibility layer for Windows and Linux
"""

import os
import platform
import subprocess
from pathlib import Path


def get_platform() -> str:
    """Get the current platform name."""
    return platform.system().lower()


def is_windows() -> bool:
    """Check if running on Windows."""
    return platform.system() == "Windows"


def is_linux() -> bool:
    """Check if running on Linux."""
    return platform.system() == "Linux"


def get_home_directory() -> Path:
    """Get the user's home directory."""
    return Path.home()


def get_logs_directory() -> Path:
    """Get the system logs directory based on platform."""
    if is_windows():
        return Path(r"C:\Windows\Logs")
    else:
        return Path("/var/log")


def get_default_monitor_paths() -> list:
    """Get default paths to monitor for log activity."""
    if is_windows():
        return [
            Path(r"C:\Windows\Logs"),
            Path(os.environ.get("TEMP", r"C:\Temp")),
        ]
    else:
        return [
            Path("/var/log"),
            Path("/tmp"),
        ]


def open_file_explorer(path: Path) -> None:
    """Open the system file explorer at the given path."""
    if is_windows():
        subprocess.Popen(f'explorer "{path}"')
    else:
        subprocess.Popen(["xdg-open", str(path)])


def get_system_info() -> dict:
    """Get system information."""
    import psutil
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_usage": psutil.disk_usage("/").percent if not is_windows() else psutil.disk_usage("C:").percent,
    }


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"
