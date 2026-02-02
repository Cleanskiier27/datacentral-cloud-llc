"""
NetworkBuster Software - Log Panel
HDD log file monitoring interface
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.log_monitor import LogMonitor, LogEntry
from config import COLORS


class LogPanel(ttk.Frame):
    """
    Log monitoring panel with file watcher and log display.
    """
    
    def __init__(self, parent, log_monitor: LogMonitor, on_log_entry=None):
        super().__init__(parent)
        self.log_monitor = log_monitor
        self.on_log_entry_callback = on_log_entry
        
        # Set up callback for log entries
        self.log_monitor.set_entry_callback(self._on_log_entry)
        
        self._create_widgets()
        self._update_stats()
        
        # Start periodic update
        self._schedule_update()
    
    def _create_widgets(self):
        """Create the panel widgets."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        
        # === Control Section ===
        control_frame = ttk.LabelFrame(self, text="📁 Watched Paths", padding=10)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        control_frame.columnconfigure(0, weight=1)
        
        # Watched paths listbox
        paths_frame = ttk.Frame(control_frame)
        paths_frame.grid(row=0, column=0, sticky="ew")
        paths_frame.columnconfigure(0, weight=1)
        
        self.paths_listbox = tk.Listbox(
            paths_frame,
            height=3,
            font=("Consolas", 9),
            bg="#1a1a2e",
            fg="#e0e0e0",
            selectbackground="#3a3a5a",
            relief="flat"
        )
        self.paths_listbox.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Buttons
        btn_frame = ttk.Frame(paths_frame)
        btn_frame.grid(row=0, column=1)
        
        ttk.Button(
            btn_frame,
            text="+ Add Path",
            command=self._add_path
        ).pack(fill="x", pady=2)
        
        ttk.Button(
            btn_frame,
            text="- Remove",
            command=self._remove_path
        ).pack(fill="x", pady=2)
        
        ttk.Button(
            btn_frame,
            text="📂 Browse",
            command=self._browse_path
        ).pack(fill="x", pady=2)
        
        # Monitoring control
        monitor_frame = ttk.Frame(control_frame)
        monitor_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        self.start_btn = ttk.Button(
            monitor_frame,
            text="▶️ Start Monitoring",
            command=self._toggle_monitoring
        )
        self.start_btn.pack(side="left", padx=5)
        
        ttk.Button(
            monitor_frame,
            text="🗑️ Clear Logs",
            command=self._clear_logs
        ).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(
            monitor_frame,
            text="⏹️ Stopped",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(side="right", padx=10)
        
        # === Stats Section ===
        stats_frame = ttk.LabelFrame(self, text="📊 Statistics", padding=10)
        stats_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="Total: 0 | Errors: 0 | Warnings: 0 | Files: 0",
            font=("Segoe UI", 10)
        )
        self.stats_label.pack(anchor="w")
        
        # Filter controls
        filter_frame = ttk.Frame(stats_frame)
        filter_frame.pack(fill="x", pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side="left")
        
        self.filter_var = tk.StringVar(value="all")
        for text, value in [("All", "all"), ("Errors", "error"), ("Warnings", "warning"), ("Info", "info")]:
            ttk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                command=self._apply_filter
            ).pack(side="left", padx=5)
        
        # === Log Display ===
        log_frame = ttk.LabelFrame(self, text="📋 Log Entries", padding=5)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Treeview for log entries
        columns = ("time", "file", "level", "content")
        self.log_tree = ttk.Treeview(
            log_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Column configuration
        self.log_tree.heading("time", text="Time")
        self.log_tree.heading("file", text="File")
        self.log_tree.heading("level", text="Level")
        self.log_tree.heading("content", text="Content")
        
        self.log_tree.column("time", width=80, minwidth=80)
        self.log_tree.column("file", width=150, minwidth=100)
        self.log_tree.column("level", width=80, minwidth=60)
        self.log_tree.column("content", width=400, minwidth=200)
        
        self.log_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.log_tree.config(yscrollcommand=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(log_frame, orient="horizontal", command=self.log_tree.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.log_tree.config(xscrollcommand=x_scroll.set)
        
        # Configure tags for levels
        self.log_tree.tag_configure("error", foreground="#ff6666")
        self.log_tree.tag_configure("warning", foreground="#ffaa00")
        self.log_tree.tag_configure("info", foreground="#00d9ff")
        self.log_tree.tag_configure("debug", foreground="#808080")
        
        # Double-click to view details
        self.log_tree.bind("<Double-1>", self._show_entry_details)
    
    def _on_log_entry(self, entry: LogEntry):
        """Handle new log entry."""
        self._add_entry_to_tree(entry)
        self._update_stats()
        
        # Notify external callback
        if self.on_log_entry_callback:
            self.on_log_entry_callback(entry)
    
    def _add_entry_to_tree(self, entry: LogEntry):
        """Add an entry to the treeview."""
        current_filter = self.filter_var.get()
        
        # Apply filter
        if current_filter != "all" and entry.level != current_filter:
            return
        
        # Format values
        time_str = entry.timestamp.strftime("%H:%M:%S")
        file_name = Path(entry.filepath).name
        level = entry.level or "-"
        content = entry.content[:100] + "..." if len(entry.content) > 100 else entry.content
        
        # Insert at beginning (most recent first)
        tag = entry.level if entry.level else ""
        self.log_tree.insert(
            "",
            0,
            values=(time_str, file_name, level.upper(), content),
            tags=(tag,)
        )
        
        # Limit visible entries
        children = self.log_tree.get_children()
        if len(children) > 500:
            self.log_tree.delete(children[-1])
    
    def _update_stats(self):
        """Update the statistics display."""
        stats = self.log_monitor.get_stats()
        self.stats_label.config(
            text=f"Total: {stats['total_entries']} | Errors: {stats['errors']} | Warnings: {stats['warnings']} | Files: {stats['files_monitored']}"
        )
    
    def _apply_filter(self):
        """Apply the current filter and refresh display."""
        # Clear current entries
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        
        # Re-add entries with filter
        filter_value = self.filter_var.get()
        filter_level = None if filter_value == "all" else filter_value
        
        entries = self.log_monitor.get_entries(count=500, level_filter=filter_level)
        for entry in reversed(entries):  # Oldest first, so newest ends up at top
            self._add_entry_to_tree(entry)
    
    def _add_path(self):
        """Add a path manually."""
        from tkinter import simpledialog
        path = simpledialog.askstring("Add Path", "Enter path to monitor:")
        if path:
            if self.log_monitor.add_watch_path(path):
                self.paths_listbox.insert(tk.END, path)
            else:
                messagebox.showerror("Error", f"Path does not exist: {path}")
    
    def _browse_path(self):
        """Browse for a directory to watch."""
        path = filedialog.askdirectory(title="Select Directory to Monitor")
        if path:
            if self.log_monitor.add_watch_path(path):
                self.paths_listbox.insert(tk.END, path)
    
    def _remove_path(self):
        """Remove selected path."""
        selection = self.paths_listbox.curselection()
        if selection:
            path = self.paths_listbox.get(selection[0])
            self.log_monitor.remove_watch_path(path)
            self.paths_listbox.delete(selection[0])
    
    def _toggle_monitoring(self):
        """Toggle monitoring on/off."""
        if self.log_monitor.running:
            self.log_monitor.stop()
            self.start_btn.config(text="▶️ Start Monitoring")
            self.status_label.config(text="⏹️ Stopped")
        else:
            self.log_monitor.start()
            self.start_btn.config(text="⏸️ Stop Monitoring")
            self.status_label.config(text="▶️ Running")
    
    def _clear_logs(self):
        """Clear all log entries."""
        self.log_monitor.clear_entries()
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
        self._update_stats()
    
    def _show_entry_details(self, event):
        """Show details of a log entry."""
        selection = self.log_tree.selection()
        if selection:
            item = self.log_tree.item(selection[0])
            values = item["values"]
            
            details = f"Time: {values[0]}\nFile: {values[1]}\nLevel: {values[2]}\n\nContent:\n{values[3]}"
            messagebox.showinfo("Log Entry Details", details)
    
    def _schedule_update(self):
        """Schedule periodic updates."""
        self._update_stats()
        self.after(2000, self._schedule_update)  # Update every 2 seconds
    
    def add_default_paths(self):
        """Add default monitoring paths based on platform."""
        from config import DEFAULT_LOG_PATHS
        for path in DEFAULT_LOG_PATHS:
            if os.path.exists(path):
                self.log_monitor.add_watch_path(path)
                self.paths_listbox.insert(tk.END, path)
