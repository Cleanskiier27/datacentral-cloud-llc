"""
NetworkBuster Software - Log Monitor
Real-time HDD log file monitoring for Windows and Linux
"""

import os
import time
import threading
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional, List, Set
from collections import deque

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False


@dataclass
class LogEntry:
    """Represents a single log entry."""
    filepath: str
    line_number: int
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    level: Optional[str] = None  # error, warning, info, debug
    
    @property
    def is_error(self) -> bool:
        return self.level == "error"
    
    @property
    def is_warning(self) -> bool:
        return self.level == "warning"


if WATCHDOG_AVAILABLE:
    class LogFileHandler(FileSystemEventHandler):
        """Handles file system events for log files."""
    
        def __init__(self, monitor: 'LogMonitor'):
            self.monitor = monitor
    
        def on_modified(self, event):
            if not event.is_directory:
                self.monitor._handle_file_change(event.src_path)
    
        def on_created(self, event):
            if not event.is_directory:
                self.monitor._handle_file_change(event.src_path)

else:
    class LogFileHandler:
        """Fallback handler when watchdog is not available."""

        def __init__(self, monitor: 'LogMonitor'):
            self.monitor = monitor

        # No-op methods (observer won't call these in polling mode)
        def on_modified(self, event):
            pass

        def on_created(self, event):
            pass


class LogMonitor:
    """
    Monitors log files on HDD in real-time.
    Supports both Windows and Linux paths.
    """
    
    # Common log file extensions
    LOG_EXTENSIONS = {'.log', '.txt', '.out', '.err', '.syslog'}
    
    # Patterns to detect log levels
    LEVEL_PATTERNS = {
        'error': ['error', 'err', 'critical', 'fatal', 'exception', 'fail'],
        'warning': ['warning', 'warn', 'caution'],
        'info': ['info', 'notice'],
        'debug': ['debug', 'trace'],
    }
    
    def __init__(self, max_entries: int = 1000):
        """Initialize the log monitor."""
        self.max_entries = max_entries
        self.entries: deque = deque(maxlen=max_entries)
        self.watched_paths: Set[Path] = set()
        self.file_positions: dict = {}  # Track file read positions
        self.running = False
        self.observer = None
        self.on_entry_callback: Optional[Callable[[LogEntry], None]] = None
        self.on_error_callback: Optional[Callable[[LogEntry], None]] = None
        self._lock = threading.Lock()
        
        # Stats
        self.stats = {
            "total_entries": 0,
            "errors": 0,
            "warnings": 0,
            "files_monitored": 0,
        }
    
    def set_entry_callback(self, callback: Callable[[LogEntry], None]):
        """Set callback for new log entries."""
        self.on_entry_callback = callback
    
    def set_error_callback(self, callback: Callable[[LogEntry], None]):
        """Set callback for error entries."""
        self.on_error_callback = callback
    
    def add_watch_path(self, path: str) -> bool:
        """Add a path (file or directory) to monitor."""
        path_obj = Path(path)
        
        if not path_obj.exists():
            return False
        
        with self._lock:
            self.watched_paths.add(path_obj)
            self.stats["files_monitored"] = len(self.watched_paths)
        
        # If already running, need to restart observer
        if self.running and WATCHDOG_AVAILABLE:
            self._setup_observer()
        
        return True
    
    def remove_watch_path(self, path: str) -> bool:
        """Remove a path from monitoring."""
        path_obj = Path(path)
        
        with self._lock:
            if path_obj in self.watched_paths:
                self.watched_paths.discard(path_obj)
                self.stats["files_monitored"] = len(self.watched_paths)
                return True
        return False
    
    def _detect_level(self, content: str) -> Optional[str]:
        """Detect log level from content."""
        content_lower = content.lower()
        for level, patterns in self.LEVEL_PATTERNS.items():
            for pattern in patterns:
                if pattern in content_lower:
                    return level
        return None
    
    def _is_log_file(self, filepath: str) -> bool:
        """Check if a file is a log file."""
        path = Path(filepath)
        return path.suffix.lower() in self.LOG_EXTENSIONS or 'log' in path.name.lower()
    
    def _handle_file_change(self, filepath: str):
        """Handle a file modification event."""
        if not self._is_log_file(filepath):
            return
        
        try:
            path = Path(filepath)
            if not path.exists() or not path.is_file():
                return
            
            # Get last known position
            last_pos = self.file_positions.get(filepath, 0)
            current_size = path.stat().st_size
            
            # If file was truncated, start from beginning
            if current_size < last_pos:
                last_pos = 0
            
            # Read new content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(last_pos)
                new_lines = f.readlines()
                self.file_positions[filepath] = f.tell()
            
            # Process new lines
            for i, line in enumerate(new_lines):
                line = line.strip()
                if not line:
                    continue
                
                level = self._detect_level(line)
                entry = LogEntry(
                    filepath=filepath,
                    line_number=last_pos + i + 1,
                    content=line,
                    level=level
                )
                
                self._add_entry(entry)
                
        except Exception as e:
            # Log read errors silently
            pass
    
    def _add_entry(self, entry: LogEntry):
        """Add a log entry and trigger callbacks."""
        with self._lock:
            self.entries.append(entry)
            self.stats["total_entries"] += 1
            
            if entry.level == "error":
                self.stats["errors"] += 1
            elif entry.level == "warning":
                self.stats["warnings"] += 1
        
        # Trigger callbacks
        if self.on_entry_callback:
            self.on_entry_callback(entry)
        
        if entry.is_error and self.on_error_callback:
            self.on_error_callback(entry)
    
    def _setup_observer(self):
        """Set up the file system observer."""
        if not WATCHDOG_AVAILABLE:
            return
        
        # Stop existing observer
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2)
        
        self.observer = Observer()
        handler = LogFileHandler(self)
        
        for path in self.watched_paths:
            if path.is_dir():
                self.observer.schedule(handler, str(path), recursive=True)
            elif path.is_file():
                self.observer.schedule(handler, str(path.parent), recursive=False)
        
        if self.running:
            self.observer.start()
    
    def start(self):
        """Start monitoring."""
        if self.running:
            return
        
        self.running = True
        
        if WATCHDOG_AVAILABLE:
            self._setup_observer()
        else:
            # Fallback: polling mode
            self._start_polling()
    
    def _start_polling(self):
        """Start polling mode (fallback when watchdog not available)."""
        def poll_loop():
            while self.running:
                for path in list(self.watched_paths):
                    if path.is_file():
                        self._handle_file_change(str(path))
                    elif path.is_dir():
                        for file_path in path.glob("**/*"):
                            if file_path.is_file() and self._is_log_file(str(file_path)):
                                self._handle_file_change(str(file_path))
                time.sleep(2)  # Poll every 2 seconds
        
        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop monitoring."""
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2)
            self.observer = None
    
    def get_entries(self, count: int = 100, level_filter: Optional[str] = None) -> List[LogEntry]:
        """Get recent log entries."""
        with self._lock:
            entries = list(self.entries)
        
        if level_filter:
            entries = [e for e in entries if e.level == level_filter]
        
        return entries[-count:]
    
    def get_errors(self, count: int = 50) -> List[LogEntry]:
        """Get recent error entries."""
        return self.get_entries(count=count, level_filter="error")
    
    def clear_entries(self):
        """Clear all log entries."""
        with self._lock:
            self.entries.clear()
            self.stats["total_entries"] = 0
            self.stats["errors"] = 0
            self.stats["warnings"] = 0
    
    def get_stats(self) -> dict:
        """Get monitoring statistics."""
        with self._lock:
            return dict(self.stats)
    
    def scan_existing_logs(self, path: str, max_lines: int = 100):
        """Scan existing log files for recent entries."""
        path_obj = Path(path)
        
        if path_obj.is_file():
            files = [path_obj]
        elif path_obj.is_dir():
            files = [f for f in path_obj.glob("**/*") if f.is_file() and self._is_log_file(str(f))]
        else:
            return
        
        for file_path in files[:10]:  # Limit to 10 files
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[-max_lines:]
                    self.file_positions[str(file_path)] = f.tell()
                    
                    for i, line in enumerate(lines):
                        line = line.strip()
                        if not line:
                            continue
                        
                        level = self._detect_level(line)
                        entry = LogEntry(
                            filepath=str(file_path),
                            line_number=len(lines) - max_lines + i + 1,
                            content=line,
                            level=level
                        )
                        self._add_entry(entry)
            except Exception:
                pass
