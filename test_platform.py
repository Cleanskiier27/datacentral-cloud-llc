"""
Unit tests for the platform utilities.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
from utils import platform as platform_utils


class TestPlatformUtils(unittest.TestCase):
    """Test cases for platform utilities."""

    @patch('platform.system')
    def test_get_platform(self, mock_system):
        """Test getting the platform name."""
        mock_system.return_value = 'Windows'
        self.assertEqual(platform_utils.get_platform(), 'windows')
        
        mock_system.return_value = 'Linux'
        self.assertEqual(platform_utils.get_platform(), 'linux')

    @patch('platform.system')
    def test_is_windows(self, mock_system):
        """Test Windows detection."""
        mock_system.return_value = 'Windows'
        self.assertTrue(platform_utils.is_windows())
        
        mock_system.return_value = 'Linux'
        self.assertFalse(platform_utils.is_windows())

    @patch('platform.system')
    def test_is_linux(self, mock_system):
        """Test Linux detection."""
        mock_system.return_value = 'Linux'
        self.assertTrue(platform_utils.is_linux())
        
        mock_system.return_value = 'Windows'
        self.assertFalse(platform_utils.is_linux())

    @patch('pathlib.Path.home')
    def test_get_home_directory(self, mock_home):
        """Test getting home directory."""
        expected_path = Path('/home/testuser')
        mock_home.return_value = expected_path
        self.assertEqual(platform_utils.get_home_directory(), expected_path)

    @patch('utils.platform.is_windows')
    def test_get_logs_directory(self, mock_is_windows):
        """Test getting logs directory."""
        # Test Windows
        mock_is_windows.return_value = True
        self.assertEqual(platform_utils.get_logs_directory(), Path(r"C:\Windows\Logs"))
        
        # Test Linux
        mock_is_windows.return_value = False
        self.assertEqual(platform_utils.get_logs_directory(), Path("/var/log"))

    @patch('utils.platform.is_windows')
    @patch.dict(os.environ, {"TEMP": r"C:\CustomTemp"})
    def test_get_default_monitor_paths(self, mock_is_windows):
        """Test getting default monitor paths."""
        # Test Windows
        mock_is_windows.return_value = True
        expected_windows = [Path(r"C:\Windows\Logs"), Path(r"C:\CustomTemp")]
        self.assertEqual(platform_utils.get_default_monitor_paths(), expected_windows)
        
        # Test Linux
        mock_is_windows.return_value = False
        expected_linux = [Path("/var/log"), Path("/tmp")]
        self.assertEqual(platform_utils.get_default_monitor_paths(), expected_linux)

    @patch('utils.platform.is_windows')
    @patch('subprocess.Popen')
    def test_open_file_explorer(self, mock_popen, mock_is_windows):
        """Test opening file explorer."""
        test_path = Path("/some/path")
        
        # Test Windows
        mock_is_windows.return_value = True
        platform_utils.open_file_explorer(test_path)
        mock_popen.assert_called_with(f'explorer "{test_path}"')
        
        # Test Linux
        mock_is_windows.return_value = False
        platform_utils.open_file_explorer(test_path)
        mock_popen.assert_called_with(["xdg-open", str(test_path)])

    def test_format_bytes(self):
        """Test byte formatting."""
        self.assertEqual(platform_utils.format_bytes(500), "500.00 B")
        self.assertEqual(platform_utils.format_bytes(1024), "1.00 KB")
        self.assertEqual(platform_utils.format_bytes(1024 * 1024), "1.00 MB")
        self.assertEqual(platform_utils.format_bytes(1024 * 1024 * 1024), "1.00 GB")
        self.assertEqual(platform_utils.format_bytes(1500), "1.46 KB")

    @patch('utils.platform.is_windows')
    @patch('platform.system')
    def test_get_system_info(self, mock_sys, mock_is_win):
        """Test getting system info with mocked psutil."""
        mock_sys.return_value = "TestOS"
        mock_is_win.return_value = False
        
        # Mock psutil since it is imported inside the function
        mock_psutil = MagicMock()
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.virtual_memory.return_value.total = 8000000
        mock_psutil.disk_usage.return_value.percent = 50.0
        
        with patch.dict(sys.modules, {'psutil': mock_psutil}):
            info = platform_utils.get_system_info()
            self.assertEqual(info['platform'], "TestOS")
            self.assertEqual(info['cpu_count'], 4)

if __name__ == "__main__":
    unittest.main()