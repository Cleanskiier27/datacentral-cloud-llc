"""
NetworkBuster OS Utilities
Comprehensive cross-platform OS operations and system information
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class OSInfo:
    """Operating system information and utilities"""
    
    def __init__(self):
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.python_version = platform.python_version()
    
    @property
    def is_windows(self) -> bool:
        """Check if running on Windows"""
        return self.system == "Windows"
    
    @property
    def is_linux(self) -> bool:
        """Check if running on Linux"""
        return self.system == "Linux"
    
    @property
    def is_macos(self) -> bool:
        """Check if running on macOS"""
        return self.system == "Darwin"
    
    @property
    def is_posix(self) -> bool:
        """Check if running on POSIX-compliant system"""
        return os.name == "posix"
    
    def get_system_name(self) -> str:
        """Get human-readable system name"""
        if self.is_windows:
            return "Windows"
        elif self.is_linux:
            return "Linux"
        elif self.is_macos:
            return "macOS"
        return self.system
    
    def to_dict(self) -> Dict:
        """Convert OS info to dictionary"""
        return {
            "system": self.system,
            "system_name": self.get_system_name(),
            "release": self.release,
            "version": self.version,
            "machine": self.machine,
            "processor": self.processor,
            "python_version": self.python_version,
            "is_windows": self.is_windows,
            "is_linux": self.is_linux,
            "is_macos": self.is_macos,
            "is_posix": self.is_posix,
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.get_system_name()} {self.release} ({self.machine})"


class PathManager:
    """Cross-platform path management"""
    
    # Cache OSInfo instance at class level
    _os_info = None
    
    @classmethod
    def _get_os_info(cls) -> OSInfo:
        """Get cached OSInfo instance"""
        if cls._os_info is None:
            cls._os_info = OSInfo()
        return cls._os_info
    
    @staticmethod
    def get_home_dir() -> Path:
        """Get user home directory"""
        return Path.home()
    
    @staticmethod
    def get_temp_dir() -> Path:
        """Get system temp directory"""
        import tempfile
        return Path(tempfile.gettempdir())
    
    @classmethod
    def get_app_data_dir(cls, app_name: str = "NetworkBuster") -> Path:
        """Get application data directory"""
        os_info = cls._get_os_info()
        if os_info.is_windows:
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif os_info.is_macos:
            base = Path.home() / "Library" / "Application Support"
        else:  # Linux and others
            base = Path.home() / ".local" / "share"
        
        app_dir = base / app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir
    
    @classmethod
    def get_config_dir(cls, app_name: str = "NetworkBuster") -> Path:
        """Get application config directory"""
        os_info = cls._get_os_info()
        if os_info.is_windows:
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif os_info.is_macos:
            base = Path.home() / "Library" / "Preferences"
        else:  # Linux and others
            base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        
        config_dir = base / app_name
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    @classmethod
    def get_logs_dir(cls, app_name: str = "NetworkBuster") -> Path:
        """Get application logs directory"""
        os_info = cls._get_os_info()
        if os_info.is_windows:
            base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
            logs_dir = base / app_name / "logs"
        elif os_info.is_macos:
            logs_dir = Path.home() / "Library" / "Logs" / app_name
        else:  # Linux and others
            logs_dir = Path.home() / ".local" / "share" / app_name / "logs"
        
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir
    
    @classmethod
    def get_cache_dir(cls, app_name: str = "NetworkBuster") -> Path:
        """Get application cache directory"""
        os_info = cls._get_os_info()
        if os_info.is_windows:
            base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
            cache_dir = base / app_name / "cache"
        elif os_info.is_macos:
            cache_dir = Path.home() / "Library" / "Caches" / app_name
        else:  # Linux and others
            base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
            cache_dir = base / app_name
        
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir


class ProcessManager:
    """Process and command execution utilities"""
    
    @staticmethod
    def run_command(
        command: List[str],
        timeout: Optional[int] = None,
        capture_output: bool = True,
        check: bool = False,
    ) -> Tuple[int, str, str]:
        """
        Run a command and return exit code, stdout, stderr
        
        Args:
            command: Command and arguments as list
            timeout: Optional timeout in seconds
            capture_output: Whether to capture output
            check: Whether to raise exception on non-zero exit
        
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        try:
            result = subprocess.run(
                command,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
                check=check,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {timeout} seconds"
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
        except Exception as e:
            return -1, "", str(e)
    
    @staticmethod
    def is_command_available(command: str) -> bool:
        """Check if a command is available in PATH"""
        return shutil.which(command) is not None
    
    @staticmethod
    def get_process_id() -> int:
        """Get current process ID"""
        return os.getpid()
    
    @staticmethod
    def get_parent_process_id() -> int:
        """Get parent process ID"""
        return os.getppid()


class EnvironmentManager:
    """Environment variables and system settings"""
    
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable"""
        return os.environ.get(key, default)
    
    @staticmethod
    def set_env(key: str, value: str) -> None:
        """Set environment variable"""
        os.environ[key] = value
    
    @staticmethod
    def has_env(key: str) -> bool:
        """Check if environment variable exists"""
        return key in os.environ
    
    @staticmethod
    def get_all_env() -> Dict[str, str]:
        """Get all environment variables"""
        return dict(os.environ)
    
    @staticmethod
    def get_path() -> List[str]:
        """Get PATH directories as list"""
        path_var = os.environ.get("PATH", "")
        # Use module-level cached os_info instance
        separator = ";" if os_info.is_windows else ":"
        return [p for p in path_var.split(separator) if p]
    
    @staticmethod
    def get_python_executable() -> str:
        """Get Python executable path"""
        return sys.executable
    
    @staticmethod
    def get_python_version() -> Tuple[int, int, int]:
        """Get Python version as tuple (major, minor, micro)"""
        return sys.version_info[:3]


class FileSystemUtils:
    """File system operations utilities"""
    
    @staticmethod
    def ensure_dir(path: Path) -> Path:
        """Ensure directory exists, create if needed"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def is_writable(path: Path) -> bool:
        """Check if path is writable"""
        return os.access(str(path), os.W_OK)
    
    @staticmethod
    def is_readable(path: Path) -> bool:
        """Check if path is readable"""
        return os.access(str(path), os.R_OK)
    
    @staticmethod
    def is_executable(path: Path) -> bool:
        """Check if path is executable"""
        return os.access(str(path), os.X_OK)
    
    @staticmethod
    def get_file_size(path: Path) -> int:
        """Get file size in bytes"""
        return Path(path).stat().st_size
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format bytes to human-readable size"""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} PB"


# Convenience instances
os_info = OSInfo()
path_manager = PathManager()
process_manager = ProcessManager()
env_manager = EnvironmentManager()
fs_utils = FileSystemUtils()


def get_os_info() -> OSInfo:
    """Get OS information instance"""
    return os_info


def get_system_summary() -> Dict:
    """Get comprehensive system summary"""
    return {
        "os": os_info.to_dict(),
        "paths": {
            "home": str(path_manager.get_home_dir()),
            "temp": str(path_manager.get_temp_dir()),
            "app_data": str(path_manager.get_app_data_dir()),
            "config": str(path_manager.get_config_dir()),
            "logs": str(path_manager.get_logs_dir()),
            "cache": str(path_manager.get_cache_dir()),
        },
        "python": {
            "executable": env_manager.get_python_executable(),
            "version": ".".join(map(str, env_manager.get_python_version())),
        },
        "process": {
            "pid": process_manager.get_process_id(),
            "ppid": process_manager.get_parent_process_id(),
        },
    }
