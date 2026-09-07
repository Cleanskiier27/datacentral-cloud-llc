# OS Utilities Documentation

## Overview

The `os_utils` module provides comprehensive cross-platform operating system utilities for the NetworkBuster application. It offers a clean, consistent API for OS detection, path management, process control, environment management, and filesystem operations.

## Features

- 🖥️ **OS Detection**: Identify Windows, Linux, macOS, and POSIX systems
- 📁 **Path Management**: Cross-platform directory paths (config, data, logs, cache)
- ⚙️ **Process Management**: Execute commands, check availability, get PIDs
- 🌍 **Environment Management**: Access and modify environment variables
- 📂 **Filesystem Utilities**: File operations and size formatting

## Quick Start

```python
from utils.os_utils import get_os_info, get_system_summary

# Get OS information
os_info = get_os_info()
print(f"Running on: {os_info.get_system_name()}")
print(f"Is Linux: {os_info.is_linux}")

# Get comprehensive system summary
summary = get_system_summary()
print(summary)
```

## API Reference

### OSInfo Class

Provides operating system information and detection.

```python
from utils.os_utils import OSInfo

os_info = OSInfo()

# Properties
os_info.system          # Platform name (e.g., "Windows", "Linux", "Darwin")
os_info.release         # OS release version
os_info.version         # OS version string
os_info.machine         # Machine architecture (e.g., "x86_64", "arm64")
os_info.processor       # Processor type
os_info.python_version  # Python version string

# Platform detection (properties)
os_info.is_windows      # True if running on Windows
os_info.is_linux        # True if running on Linux
os_info.is_macos        # True if running on macOS
os_info.is_posix        # True if running on POSIX system

# Methods
os_info.get_system_name()  # Human-readable system name
os_info.to_dict()          # Convert to dictionary
str(os_info)               # String representation
```

### PathManager Class

Cross-platform path management for application directories.

```python
from utils.os_utils import PathManager

# Standard directories
PathManager.get_home_dir()                      # User home directory
PathManager.get_temp_dir()                      # System temp directory

# Application-specific directories (creates if needed)
PathManager.get_app_data_dir("AppName")         # Application data directory
PathManager.get_config_dir("AppName")           # Configuration directory
PathManager.get_logs_dir("AppName")             # Logs directory
PathManager.get_cache_dir("AppName")            # Cache directory
```

#### Platform-Specific Paths

**Windows:**
- App Data: `%APPDATA%\AppName`
- Config: `%APPDATA%\AppName`
- Logs: `%LOCALAPPDATA%\AppName\logs`
- Cache: `%LOCALAPPDATA%\AppName\cache`

**macOS:**
- App Data: `~/Library/Application Support/AppName`
- Config: `~/Library/Preferences/AppName`
- Logs: `~/Library/Logs/AppName`
- Cache: `~/Library/Caches/AppName`

**Linux:**
- App Data: `~/.local/share/AppName`
- Config: `~/.config/AppName` (respects XDG_CONFIG_HOME)
- Logs: `~/.local/share/AppName/logs`
- Cache: `~/.cache/AppName` (respects XDG_CACHE_HOME)

### ProcessManager Class

Process and command execution utilities.

```python
from utils.os_utils import ProcessManager

# Execute commands
exit_code, stdout, stderr = ProcessManager.run_command(
    ["python", "--version"],
    timeout=10,           # Optional timeout in seconds
    capture_output=True,  # Capture stdout/stderr
    check=False          # Don't raise exception on non-zero exit
)

# Check command availability
if ProcessManager.is_command_available("git"):
    print("Git is installed")

# Process IDs
pid = ProcessManager.get_process_id()         # Current process ID
ppid = ProcessManager.get_parent_process_id() # Parent process ID
```

### EnvironmentManager Class

Environment variable and system settings management.

```python
from utils.os_utils import EnvironmentManager

# Environment variables
value = EnvironmentManager.get_env("HOME", default="/tmp")
EnvironmentManager.set_env("MY_VAR", "my_value")
has_var = EnvironmentManager.has_env("PATH")
all_vars = EnvironmentManager.get_all_env()

# PATH management
path_dirs = EnvironmentManager.get_path()  # List of PATH directories

# Python information
python_exe = EnvironmentManager.get_python_executable()
version = EnvironmentManager.get_python_version()  # Tuple (major, minor, micro)
```

### FileSystemUtils Class

Filesystem operations and utilities.

```python
from utils.os_utils import FileSystemUtils
from pathlib import Path

# Directory operations
path = FileSystemUtils.ensure_dir(Path("/tmp/myapp"))  # Creates if needed

# Permissions
is_readable = FileSystemUtils.is_readable(Path("/tmp/file.txt"))
is_writable = FileSystemUtils.is_writable(Path("/tmp/file.txt"))
is_executable = FileSystemUtils.is_executable(Path("/usr/bin/python"))

# File size
size = FileSystemUtils.get_file_size(Path("file.txt"))  # Size in bytes
formatted = FileSystemUtils.format_file_size(1024*1024)  # "1.00 MB"
```

### Convenience Functions

Quick access to common functionality.

```python
from utils.os_utils import get_os_info, get_system_summary

# Get OS info instance
os_info = get_os_info()

# Get comprehensive system summary
summary = get_system_summary()
# Returns dictionary with:
#   - os: OS information
#   - paths: Standard paths (home, temp, app dirs)
#   - python: Python executable and version
#   - process: Current and parent PIDs
```

## Examples

### Example 1: Cross-Platform Configuration

```python
from utils.os_utils import PathManager, OSInfo
import json
from pathlib import Path

os_info = OSInfo()
config_dir = PathManager.get_config_dir("MyApp")
config_file = config_dir / "settings.json"

# Save configuration
config = {
    "platform": os_info.get_system_name(),
    "version": "1.0.0",
}
with open(config_file, "w") as f:
    json.dump(config, f, indent=2)

print(f"Config saved to: {config_file}")
```

### Example 2: Command Execution

```python
from utils.os_utils import ProcessManager

# Check if git is available
if not ProcessManager.is_command_available("git"):
    print("Git is not installed")
    exit(1)

# Run git command
exit_code, stdout, stderr = ProcessManager.run_command(
    ["git", "status"],
    timeout=5
)

if exit_code == 0:
    print("Git status:", stdout)
else:
    print("Error:", stderr)
```

### Example 3: Platform-Specific Behavior

```python
from utils.os_utils import OSInfo, ProcessManager

os_info = OSInfo()

if os_info.is_windows:
    # Windows-specific command
    ProcessManager.run_command(["cmd", "/c", "dir"])
elif os_info.is_linux or os_info.is_macos:
    # Unix-specific command
    ProcessManager.run_command(["ls", "-la"])
```

### Example 4: System Information Display

```python
from utils.os_utils import get_system_summary
import json

summary = get_system_summary()
print(json.dumps(summary, indent=2))

# Output includes:
# - OS name, version, architecture
# - Standard directory paths
# - Python version and executable
# - Current process information
```

### Example 5: File Operations

```python
from utils.os_utils import FileSystemUtils
from pathlib import Path

# Create directory structure
log_dir = FileSystemUtils.ensure_dir(Path("./logs"))

# Check file properties
log_file = log_dir / "app.log"
if log_file.exists():
    size = FileSystemUtils.get_file_size(log_file)
    print(f"Log file size: {FileSystemUtils.format_file_size(size)}")
    
    if FileSystemUtils.is_writable(log_file):
        print("Log file is writable")
```

## Testing

Run the test suite:

```bash
python test_os_utils.py
```

Run the demo:

```bash
python examples/os_utils_demo.py
```

## Integration with NetworkBuster

The OS utilities can be used throughout NetworkBuster for:

1. **Configuration Management**: Store configs in platform-appropriate locations
2. **Logging**: Write logs to standard OS log directories
3. **Cache Management**: Cache data in platform-specific cache directories
4. **Process Execution**: Run platform-specific commands safely
5. **System Information**: Display system info in the dashboard

### Example Integration

```python
# In your NetworkBuster application
from utils.os_utils import PathManager, get_os_info

# Get appropriate directories
config_dir = PathManager.get_config_dir("NetworkBuster")
logs_dir = PathManager.get_logs_dir("NetworkBuster")
cache_dir = PathManager.get_cache_dir("NetworkBuster")

# Display system info in dashboard
os_info = get_os_info()
dashboard.display_system_info(
    platform=os_info.get_system_name(),
    version=os_info.release,
    architecture=os_info.machine,
)
```

## Module Structure

```
utils/
├── __init__.py
├── os_utils.py          # Main OS utilities module
├── platform.py          # Existing platform utilities (legacy)
└── helpers.py           # Other utility functions

examples/
└── os_utils_demo.py     # Demo script

test_os_utils.py         # Test suite (in root directory)
```

## Migration from platform.py

The new `os_utils` module is designed to complement and eventually replace `utils/platform.py`. Key differences:

| Feature | platform.py | os_utils.py |
|---------|-------------|-------------|
| OS Detection | ✓ | ✓ (Enhanced) |
| Path Management | ✓ (Basic) | ✓ (Comprehensive) |
| Process Management | ✗ | ✓ |
| Environment Management | ✗ | ✓ |
| Filesystem Utilities | ✓ (Limited) | ✓ (Enhanced) |
| System Information | ✓ (psutil) | ✓ (Built-in) |

## Best Practices

1. **Use PathManager for all directory paths** - Ensures cross-platform compatibility
2. **Check command availability** before running commands
3. **Use ProcessManager for subprocess execution** - Provides consistent error handling
4. **Cache OSInfo instance** - Create once and reuse
5. **Handle platform differences** - Use is_windows, is_linux, is_macos properties

## Future Enhancements

Potential additions to the module:

- Network interface detection
- Disk space monitoring
- System resource usage (CPU, memory)
- User and group management
- Registry operations (Windows)
- Service management
- Firewall configuration

## Support

For issues or questions about the OS utilities module:

1. Check the test suite for examples: `test_os_utils.py`
2. Run the demo script: `examples/os_utils_demo.py`
3. Review the source code: `utils/os_utils.py`

## License

Part of the NetworkBuster project.

---

**NetworkBuster OS Utilities** | v1.0.0
