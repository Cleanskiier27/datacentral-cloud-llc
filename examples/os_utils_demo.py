#!/usr/bin/env python3
"""
Example usage of NetworkBuster OS Utilities
Demonstrates the capabilities of the os_utils module
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.os_utils import (
    get_os_info,
    get_system_summary,
    PathManager,
    ProcessManager,
    EnvironmentManager,
    FileSystemUtils,
)


def print_section(title: str):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def demo_os_info():
    """Demonstrate OS information capabilities"""
    print_section("Operating System Information")
    
    os_info = get_os_info()
    
    print(f"System:           {os_info.get_system_name()}")
    print(f"Release:          {os_info.release}")
    print(f"Version:          {os_info.version}")
    print(f"Machine:          {os_info.machine}")
    print(f"Processor:        {os_info.processor}")
    print(f"Python Version:   {os_info.python_version}")
    print(f"\nPlatform Checks:")
    print(f"  Is Windows:     {os_info.is_windows}")
    print(f"  Is Linux:       {os_info.is_linux}")
    print(f"  Is macOS:       {os_info.is_macos}")
    print(f"  Is POSIX:       {os_info.is_posix}")


def demo_path_manager():
    """Demonstrate path management capabilities"""
    print_section("Path Management")
    
    print(f"Home Directory:   {PathManager.get_home_dir()}")
    print(f"Temp Directory:   {PathManager.get_temp_dir()}")
    print(f"\nNetworkBuster Directories:")
    print(f"  App Data:       {PathManager.get_app_data_dir()}")
    print(f"  Config:         {PathManager.get_config_dir()}")
    print(f"  Logs:           {PathManager.get_logs_dir()}")
    print(f"  Cache:          {PathManager.get_cache_dir()}")


def demo_process_manager():
    """Demonstrate process management capabilities"""
    print_section("Process Management")
    
    print(f"Current PID:      {ProcessManager.get_process_id()}")
    print(f"Parent PID:       {ProcessManager.get_parent_process_id()}")
    
    print(f"\nCommand Availability:")
    commands = ["python", "python3", "git", "pip", "node", "npm"]
    for cmd in commands:
        available = "✓" if ProcessManager.is_command_available(cmd) else "✗"
        print(f"  {available} {cmd}")
    
    # Run a simple command
    print(f"\nExecuting 'python --version':")
    exit_code, stdout, stderr = ProcessManager.run_command(["python", "--version"])
    output = stdout or stderr
    print(f"  Exit Code: {exit_code}")
    print(f"  Output: {output.strip()}")


def demo_environment_manager():
    """Demonstrate environment management capabilities"""
    print_section("Environment Management")
    
    print(f"Python Executable: {EnvironmentManager.get_python_executable()}")
    print(f"Python Version:    {'.'.join(map(str, EnvironmentManager.get_python_version()))}")
    
    print(f"\nPATH Directories ({len(EnvironmentManager.get_path())} total):")
    for i, path in enumerate(EnvironmentManager.get_path()[:5], 1):
        print(f"  {i}. {path}")
    if len(EnvironmentManager.get_path()) > 5:
        print(f"  ... and {len(EnvironmentManager.get_path()) - 5} more")
    
    print(f"\nCommon Environment Variables:")
    common_vars = ["HOME", "USER", "PATH", "SHELL", "LANG"]
    for var in common_vars:
        value = EnvironmentManager.get_env(var)
        if value:
            # Truncate long values
            display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"  {var}: {display_value}")


def demo_filesystem_utils():
    """Demonstrate filesystem utilities capabilities"""
    print_section("Filesystem Utilities")
    
    # Get info about the current script
    script_path = Path(__file__).resolve()
    
    print(f"Current Script:   {script_path.name}")
    print(f"Full Path:        {script_path}")
    
    if script_path.exists():
        size = FileSystemUtils.get_file_size(script_path)
        print(f"Size:             {size} bytes ({FileSystemUtils.format_file_size(size)})")
        print(f"Readable:         {FileSystemUtils.is_readable(script_path)}")
        print(f"Writable:         {FileSystemUtils.is_writable(script_path)}")
        print(f"Executable:       {FileSystemUtils.is_executable(script_path)}")
    
    # Demonstrate size formatting
    print(f"\nSize Formatting Examples:")
    sizes = [512, 1024, 1024*1024, 1024*1024*100, 1024*1024*1024*5]
    for size in sizes:
        print(f"  {size:>15} bytes = {FileSystemUtils.format_file_size(size)}")


def demo_system_summary():
    """Demonstrate system summary"""
    print_section("Complete System Summary")
    
    summary = get_system_summary()
    print(json.dumps(summary, indent=2))


def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print("  NetworkBuster OS Utilities Demo")
    print("="*60)
    
    try:
        demo_os_info()
        demo_path_manager()
        demo_process_manager()
        demo_environment_manager()
        demo_filesystem_utils()
        demo_system_summary()
        
        print("\n" + "="*60)
        print("  Demo Complete!")
        print("="*60)
        print("\nFor more information, see: utils/os_utils.py")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
