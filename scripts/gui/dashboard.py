"""
NetworkBuster Software - Dashboard Panel
Real-time composition and activity overview
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.compositor import RealTimeCompositor, CompositionEvent
from config import COLORS


class DashboardPanel(ttk.Frame):
    """
    Real-time dashboard showing system activity and composition metrics.
    """
    
    def __init__(self, parent, compositor: RealTimeCompositor):
        super().__init__(parent)
        self.compositor = compositor
        
        # Register for events
        self.compositor.add_callback(self._on_event)
        
        self._create_widgets()
        self._start_updates()
    
    def _create_widgets(self):
        """Create the dashboard widgets."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Header Stats ===
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=10)
        
        # Stats cards
        self._create_stat_card(header_frame, "📊 Total Events", "total_events", 0)
        self._create_stat_card(header_frame, "⚡ Events/sec", "events_per_sec", 1)
        self._create_stat_card(header_frame, "📡 Sources", "sources", 2)
        self._create_stat_card(header_frame, "🏷️ Event Types", "event_types", 3)
        
        # === Left Column - Event Feed ===
        feed_frame = ttk.LabelFrame(self, text="📋 Live Event Feed", padding=5)
        feed_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        feed_frame.columnconfigure(0, weight=1)
        feed_frame.rowconfigure(0, weight=1)
        
        self.event_text = tk.Text(
            feed_frame,
            font=("Consolas", 9),
            bg="#0a0a14",
            fg="#e0e0e0",
            relief="flat",
            state="disabled",
            wrap="word"
        )
        self.event_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(feed_frame, orient="vertical", command=self.event_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.event_text.config(yscrollcommand=scrollbar.set)
        
        # Configure tags
        self.event_text.tag_configure("timestamp", foreground="#808080")
        self.event_text.tag_configure("source", foreground="#00d9ff")
        self.event_text.tag_configure("event_type", foreground="#ffaa00")
        self.event_text.tag_configure("data", foreground="#ffffff")
        self.event_text.tag_configure("log", foreground="#00ff88")
        self.event_text.tag_configure("error", foreground="#ff6666")
        
        # === Right Column - Visualization ===
        viz_frame = ttk.LabelFrame(self, text="📈 Activity Monitor", padding=5)
        viz_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Canvas for simple visualization
        self.viz_canvas = tk.Canvas(
            viz_frame,
            bg="#0a0a14",
            highlightthickness=0
        )
        self.viz_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Activity bars visualization
        self.activity_bars = []
        self.max_bars = 30
        
        # === Bottom - Source Summary ===
        summary_frame = ttk.LabelFrame(self, text="📡 Source Activity", padding=5)
        summary_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.source_labels = {}
        self.source_frame = ttk.Frame(summary_frame)
        self.source_frame.pack(fill="x")
        
        # Control buttons
        control_frame = ttk.Frame(summary_frame)
        control_frame.pack(fill="x", pady=5)
        
        ttk.Button(
            control_frame,
            text="🗑️ Clear Events",
            command=self._clear_events
        ).pack(side="left", padx=5)
        
        ttk.Button(
            control_frame,
            text="💾 Export Events",
            command=self._export_events
        ).pack(side="left", padx=5)
        
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            control_frame,
            text="Auto-scroll",
            variable=self.auto_scroll_var
        ).pack(side="right", padx=5)
    
    def _create_stat_card(self, parent, title: str, key: str, column: int):
        """Create a statistics card."""
        card = ttk.Frame(parent, relief="ridge", borderwidth=1)
        card.grid(row=0, column=column, padx=10, pady=5)
        
        ttk.Label(card, text=title, font=("Segoe UI", 9)).pack(pady=(5, 0))
        
        label = ttk.Label(card, text="0", font=("Segoe UI", 18, "bold"))
        label.pack(pady=(0, 5), padx=20)
        
        setattr(self, f"stat_{key}", label)
    
    def _on_event(self, event: CompositionEvent):
        """Handle new composition event."""
        self._add_event_to_feed(event)
        self._add_activity_bar(event.source)
    
    def _add_event_to_feed(self, event: CompositionEvent):
        """Add an event to the live feed."""
        self.event_text.config(state="normal")
        
        # Limit lines
        lines = int(self.event_text.index('end-1c').split('.')[0])
        if lines > 500:
            self.event_text.delete("1.0", "100.0")
        
        # Format event
        time_str = event.timestamp.strftime("%H:%M:%S")
        self.event_text.insert(tk.END, f"[{time_str}] ", "timestamp")
        self.event_text.insert(tk.END, f"{event.source}", "source")
        self.event_text.insert(tk.END, " → ", "data")
        
        # Color based on type
        tag = "event_type"
        if "error" in event.event_type.lower():
            tag = "error"
        elif "log" in event.event_type.lower():
            tag = "log"
        
        self.event_text.insert(tk.END, f"{event.event_type}", tag)
        
        # Add data summary
        data_str = str(event.data)[:50]
        if len(str(event.data)) > 50:
            data_str += "..."
        self.event_text.insert(tk.END, f" | {data_str}\n", "data")
        
        if self.auto_scroll_var.get():
            self.event_text.see(tk.END)
        
        self.event_text.config(state="disabled")
    
    def _add_activity_bar(self, source: str):
        """Add an activity bar to the visualization."""
        # Get canvas dimensions
        width = self.viz_canvas.winfo_width()
        height = self.viz_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Add new bar
        bar_width = 10
        bar_height = min(50, height - 20)
        spacing = 3
        
        # Shift existing bars left
        if len(self.activity_bars) >= self.max_bars:
            old_bar = self.activity_bars.pop(0)
            self.viz_canvas.delete(old_bar)
        
        for bar in self.activity_bars:
            self.viz_canvas.move(bar, -(bar_width + spacing), 0)
        
        # Add new bar on right
        x = width - bar_width - 10
        y = height - 10
        
        # Color based on source
        colors = {
            "log_monitor": "#00ff88",
            "data_recycler": "#00d9ff",
            "avatar": "#ffaa00",
            "system": "#e94560",
        }
        color = colors.get(source, "#ffffff")
        
        bar = self.viz_canvas.create_rectangle(
            x, y - bar_height, x + bar_width, y,
            fill=color,
            outline=""
        )
        self.activity_bars.append(bar)
    
    def _update_stats(self):
        """Update the statistics display."""
        stats = self.compositor.get_stats()
        
        self.stat_total_events.config(text=str(stats["total_events"]))
        self.stat_events_per_sec.config(text=f"{stats['events_per_second']:.1f}")
        self.stat_sources.config(text=str(stats["sources_count"]))
        self.stat_event_types.config(text=str(stats["event_types_count"]))
        
        # Update source summary
        sources = self.compositor.get_sources_summary()
        
        # Clear old labels
        for widget in self.source_frame.winfo_children():
            widget.destroy()
        
        for name, info in sources.items():
            color = "#00ff88" if info["enabled"] else "#808080"
            label = ttk.Label(
                self.source_frame,
                text=f"📡 {name}: {info['event_count']} events",
                font=("Segoe UI", 9)
            )
            label.pack(side="left", padx=10)
    
    def _start_updates(self):
        """Start periodic updates."""
        self._update_stats()
        self.after(1000, self._start_updates)
    
    def _clear_events(self):
        """Clear all events."""
        self.compositor.clear()
        self.event_text.config(state="normal")
        self.event_text.delete("1.0", tk.END)
        self.event_text.config(state="disabled")
        
        # Clear visualization
        for bar in self.activity_bars:
            self.viz_canvas.delete(bar)
        self.activity_bars.clear()
        
        self._update_stats()
    
    def _export_events(self):
        """Export events to file."""
        from tkinter import filedialog
        
        filepath = filedialog.asksaveasfilename(
            title="Export Events",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("NDJSON files", "*.ndjson")]
        )
        
        if filepath:
            format_type = "ndjson" if filepath.endswith(".ndjson") else "json"
            count = self.compositor.export_events(filepath, format=format_type)
            
            from tkinter import messagebox
            messagebox.showinfo("Export Complete", f"Exported {count} events to {filepath}")
