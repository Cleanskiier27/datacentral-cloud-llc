"""
Tests for OS utilities module
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.os_utils import (
    OSInfo,
    PathManager,
    ProcessManager,
    EnvironmentManager,
    FileSystemUtils,
    get_os_info,
    get_system_summary,
)


def test_os_info():
    """Test OSInfo class"""
    print("Testing OSInfo...")
    os_info = OSInfo()
    
    # Test basic attributes
    assert os_info.system is not None
    assert os_info.release is not None
    assert os_info.machine is not None
    assert os_info.python_version is not None
    
    # Test platform detection
    assert isinstance(os_info.is_windows, bool)
    assert isinstance(os_info.is_linux, bool)
    assert isinstance(os_info.is_macos, bool)
    assert isinstance(os_info.is_posix, bool)
    
    # Test system name
    system_name = os_info.get_system_name()
    assert system_name in ["Windows", "Linux", "macOS"] or system_name == os_info.system
    
    # Test to_dict
    info_dict = os_info.to_dict()
    assert "system" in info_dict
    assert "is_windows" in info_dict
    assert "python_version" in info_dict
    
    # Test string representation
    str_repr = str(os_info)
    assert os_info.get_system_name() in str_repr
    
    print(f"  ✓ OS: {os_info}")
    print(f"  ✓ Platform checks passed")


def test_path_manager():
    """Test PathManager class"""
    print("\nTesting PathManager...")
    
    # Test home directory
    home = PathManager.get_home_dir()
    assert home.exists()
    print(f"  ✓ Home: {home}")
    
    # Test temp directory
    temp = PathManager.get_temp_dir()
    assert temp.exists()
    print(f"  ✓ Temp: {temp}")
    
    # Test app directories
    app_data = PathManager.get_app_data_dir("TestApp")
    assert app_data.exists()
    print(f"  ✓ App Data: {app_data}")
    
    config = PathManager.get_config_dir("TestApp")
    assert config.exists()
    print(f"  ✓ Config: {config}")
    
    logs = PathManager.get_logs_dir("TestApp")
    assert logs.exists()
    print(f"  ✓ Logs: {logs}")
    
    cache = PathManager.get_cache_dir("TestApp")
    assert cache.exists()
    print(f"  ✓ Cache: {cache}")


def test_process_manager():
    """Test ProcessManager class"""
    print("\nTesting ProcessManager...")
    
    # Test command execution
    if ProcessManager.is_command_available("python") or ProcessManager.is_command_available("python3"):
        python_cmd = "python" if ProcessManager.is_command_available("python") else "python3"
        exit_code, stdout, stderr = ProcessManager.run_command([python_cmd, "--version"])
        assert exit_code == 0
        assert "Python" in stdout or "Python" in stderr
        print(f"  ✓ Command execution works")
    
    # Test command availability
    python_available = ProcessManager.is_command_available("python") or \
                       ProcessManager.is_command_available("python3")
    assert python_available
    print(f"  ✓ Command availability check works")
    
    # Test process IDs
    pid = ProcessManager.get_process_id()
    assert pid > 0
    print(f"  ✓ Process ID: {pid}")
    
    ppid = ProcessManager.get_parent_process_id()
    assert ppid > 0
    print(f"  ✓ Parent Process ID: {ppid}")


def test_environment_manager():
    """Test EnvironmentManager class"""
    print("\nTesting EnvironmentManager...")
    
    # Test PATH
    path_dirs = EnvironmentManager.get_path()
    assert len(path_dirs) > 0
    print(f"  ✓ PATH has {len(path_dirs)} directories")
    
    # Test Python executable
    python_exe = EnvironmentManager.get_python_executable()
    assert Path(python_exe).exists()
    print(f"  ✓ Python: {python_exe}")
    
    # Test Python version
    version = EnvironmentManager.get_python_version()
    assert len(version) == 3
    assert all(isinstance(v, int) for v in version)
    print(f"  ✓ Python version: {'.'.join(map(str, version))}")
    
    # Test environment variable operations
    test_key = "TEST_OS_UTILS_VAR"
    test_value = "test_value_12345"
    
    # Should not exist initially
    assert not EnvironmentManager.has_env(test_key)
    
    # Set and get
    EnvironmentManager.set_env(test_key, test_value)
    assert EnvironmentManager.has_env(test_key)
    assert EnvironmentManager.get_env(test_key) == test_value
    
    # Clean up
    del os.environ[test_key]
    print(f"  ✓ Environment variable operations work")


def test_filesystem_utils():
    """Test FileSystemUtils class"""
    print("\nTesting FileSystemUtils...")
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        test_file = Path(f.name)
        f.write("test content")
    
    try:
        # Test file size
        size = FileSystemUtils.get_file_size(test_file)
        assert size > 0
        print(f"  ✓ File size: {size} bytes")
        
        # Test formatted size
        formatted = FileSystemUtils.format_file_size(size)
        assert "B" in formatted
        print(f"  ✓ Formatted size: {formatted}")
        
        # Test permissions
        assert FileSystemUtils.is_readable(test_file)
        print(f"  ✓ File is readable")
        
        # Test directory creation
        test_dir = test_file.parent / "test_os_utils_dir"
        created_dir = FileSystemUtils.ensure_dir(test_dir)
        assert created_dir.exists()
        print(f"  ✓ Directory creation works")
        
        # Clean up directory
        created_dir.rmdir()
        
    finally:
        # Clean up test file
        test_file.unlink()


def test_convenience_functions():
    """Test convenience functions"""
    print("\nTesting convenience functions...")
    
    # Test get_os_info
    os_info = get_os_info()
    assert isinstance(os_info, OSInfo)
    print(f"  ✓ get_os_info() works")
    
    # Test get_system_summary
    summary = get_system_summary()
    assert "os" in summary
    assert "paths" in summary
    assert "python" in summary
    assert "process" in summary
    print(f"  ✓ get_system_summary() works")
    print(f"    OS: {summary['os']['system_name']}")
    print(f"    Python: {summary['python']['version']}")
    print(f"    PID: {summary['process']['pid']}")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Running OS Utils Tests")
    print("="*60)
    
    try:
        test_os_info()
        test_path_manager()
        test_process_manager()
        test_environment_manager()
        test_filesystem_utils()
        test_convenience_functions()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        return True
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
