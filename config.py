import os
from pathlib import Path

# Application Metadata
APP_NAME = "NetworkBuster"
APP_VERSION = "1.0.0"

# UI Settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Colors (NetworkBuster Dark Theme)
COLORS = {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_tertiary": "#0f3460",
    "text_primary": "#e1e1e1",
    "text_secondary": "#95a5a6",
    "accent": "#00ff88",
    "success": "#00ff88",
    "warning": "#f39c12",
    "error": "#e94560",
    "info": "#3498db"
}

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)
