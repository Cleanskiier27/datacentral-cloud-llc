"""
NetworkBuster Software - Main Window
Main application window with tabbed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT, COLORS, DATA_DIR
from core.avatar import Avatar, AvatarState
from core.log_monitor import LogMonitor
from core.data_recycler import DataRecycler
from core.compositor import RealTimeCompositor
from gui.avatar_panel import AvatarPanel
from gui.log_panel import LogPanel
from gui.data_panel import DataPanel
from gui.dashboard import DashboardPanel


class NetworkBusterApp:
    """
    Main NetworkBuster application window.
    """
    
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(800, 600)
        
        # Set icon (if exists)
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # Configure dark theme
        self._setup_theme()
        
        # Initialize core components
        self._init_components()
        
        # Create UI
        self._create_menu()
        self._create_widgets()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Start components
        self._start_components()
    
    def _setup_theme(self):
        """Set up the dark theme."""
        style = ttk.Style()
        
        # Try to use a theme that supports customization
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        
        # Configure colors
        bg = COLORS["bg_primary"]
        bg2 = COLORS["bg_secondary"]
        fg = COLORS["text_primary"]
        accent = COLORS["accent"]
        
        # Root window
        self.root.configure(bg=bg)
        
        # Frame styles
        style.configure("TFrame", background=bg)
        style.configure("TLabelframe", background=bg, foreground=fg)
        style.configure("TLabelframe.Label", background=bg, foreground=fg, font=("Segoe UI", 10, "bold"))
        
        # Label styles
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        
        # Button styles
        style.configure("TButton", background=bg2, foreground=fg, font=("Segoe UI", 9), padding=5)
        style.map("TButton",
            background=[("active", COLORS["bg_tertiary"])],
            foreground=[("active", fg)]
        )
        
        # Notebook (tabs) styles
        style.configure("TNotebook", background=bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=bg2, foreground=fg, padding=[15, 8], font=("Segoe UI", 10))
        style.map("TNotebook.Tab",
            background=[("selected", COLORS["bg_tertiary"]), ("active", bg2)],
            foreground=[("selected", accent), ("active", fg)]
        )
        
        # Entry style
        style.configure("TEntry", fieldbackground=bg2, foreground=fg)
        
        # Treeview style
        style.configure("Treeview",
            background=bg,
            foreground=fg,
            fieldbackground=bg,
            font=("Consolas", 9)
        )
        style.configure("Treeview.Heading",
            background=bg2,
            foreground=fg,
            font=("Segoe UI", 9, "bold")
        )
        style.map("Treeview",
            background=[("selected", COLORS["bg_tertiary"])],
            foreground=[("selected", accent)]
        )
        
        # Scrollbar style
        style.configure("Vertical.TScrollbar", background=bg2, troughcolor=bg)
        style.configure("Horizontal.TScrollbar", background=bg2, troughcolor=bg)
        
        # Radiobutton style
        style.configure("TRadiobutton", background=bg, foreground=fg)
        
        # Checkbutton style
        style.configure("TCheckbutton", background=bg, foreground=fg)
    
    def _init_components(self):
        """Initialize core components."""
        # Avatar
        self.avatar = Avatar(name="Buster")
        
        # Log Monitor
        self.log_monitor = LogMonitor(max_entries=1000)
        
        # Data Recycler
        self.data_recycler = DataRecycler(storage_path=DATA_DIR / "recycler")
        
        # Compositor
        self.compositor = RealTimeCompositor(max_events=10000)
        
        # Register compositor sources
        self.log_source = self.compositor.register_source("log_monitor")
        self.data_source = self.compositor.register_source("data_recycler")
        self.avatar_source = self.compositor.register_source("avatar")
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"])
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"])
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export All Data", command=self._export_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"])
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Avatar", command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Logs", command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Data", command=lambda: self.notebook.select(2))
        view_menu.add_command(label="Dashboard", command=lambda: self.notebook.select(3))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["bg_secondary"], fg=COLORS["text_primary"])
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create the main widgets."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill="x", padx=10, pady=5)
        
        title_label = ttk.Label(
            header,
            text=f"🚀 {APP_NAME}",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side="left")
        
        self.status_label = ttk.Label(
            header,
            text="● Online",
            font=("Segoe UI", 10),
            foreground=COLORS["success"]
        )
        self.status_label.pack(side="right")
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create panels
        self.avatar_panel = AvatarPanel(self.notebook, self.avatar)
        self.log_panel = LogPanel(
            self.notebook, 
            self.log_monitor,
            on_log_entry=self._on_log_entry
        )
        self.data_panel = DataPanel(
            self.notebook,
            self.data_recycler,
            on_data_recycled=self._on_data_recycled
        )
        self.dashboard_panel = DashboardPanel(self.notebook, self.compositor)
        
        # Add tabs
        self.notebook.add(self.avatar_panel, text="🤖 Avatar")
        self.notebook.add(self.log_panel, text="📋 Log Monitor")
        self.notebook.add(self.data_panel, text="♻️ Data Recycler")
        self.notebook.add(self.dashboard_panel, text="📊 Dashboard")
        
        # Status bar
        status_bar = ttk.Frame(main_frame)
        status_bar.pack(fill="x", side="bottom", padx=5, pady=5)
        
        self.footer_label = ttk.Label(
            status_bar,
            text=f"{APP_NAME} v{APP_VERSION} | Cross-platform (Windows/Linux)",
            font=("Segoe UI", 8)
        )
        self.footer_label.pack(side="left")
        
        self.event_count_label = ttk.Label(
            status_bar,
            text="Events: 0",
            font=("Segoe UI", 8)
        )
        self.event_count_label.pack(side="right")
    
    def _start_components(self):
        """Start background components."""
        # Start compositor
        self.compositor.start()
        
        # Set avatar state
        self.avatar.set_state(AvatarState.IDLE)
        
        # Emit startup event
        self.avatar_source.emit("startup", {"message": "NetworkBuster started"})
        
        # Start event count updater
        self._update_event_count()
    
    def _on_log_entry(self, entry):
        """Handle log entry event."""
        # Emit to compositor
        self.log_source.emit(
            "log_entry" if not entry.is_error else "log_error",
            {"file": entry.filepath, "content": entry.content[:100]}
        )
        
        # Notify avatar
        self.avatar.notify_log_entry(is_error=entry.is_error)
        
        # Update avatar state
        self.avatar.set_state(AvatarState.MONITORING)
    
    def _on_data_recycled(self, count: int):
        """Handle data recycled event."""
        # Emit to compositor
        self.data_source.emit("data_recycled", {"count": count})
        
        # Notify avatar
        self.avatar.notify_data_recycled(count)
    
    def _update_event_count(self):
        """Update the event count in status bar."""
        stats = self.compositor.get_stats()
        self.event_count_label.config(text=f"Events: {stats['total_events']}")
        self.root.after(1000, self._update_event_count)
    
    def _export_all(self):
        """Export all data."""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(title="Select Export Directory")
        if directory:
            dir_path = Path(directory)
            
            # Export data
            self.data_recycler.export_json(dir_path / "data_records.json")
            self.compositor.export_events(str(dir_path / "events.json"))
            
            messagebox.showinfo("Export Complete", f"Data exported to {directory}")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = f"""
{APP_NAME} v{APP_VERSION}

A cross-platform Python application for:
• Avatar-based interaction
• Real-time log monitoring
• Data recycling and transformation
• Live activity composition

Created for Windows and Linux
        """
        messagebox.showinfo("About", about_text.strip())
    
    def _on_close(self):
        """Handle window close."""
        # Stop components
        self.log_monitor.stop()
        self.compositor.stop()
        
        # Destroy window
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = NetworkBusterApp()
    app.run()


if __name__ == "__main__":
    main()
