"""
NetworkBuster Software - Avatar Panel
Interactive avatar display and communication interface
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.avatar import Avatar, AvatarMood, AvatarState, AvatarMessage
from config import COLORS


class AvatarPanel(ttk.Frame):
    """
    Avatar interaction panel with visual display and message feed.
    """
    
    def __init__(self, parent, avatar: Avatar):
        super().__init__(parent)
        self.avatar = avatar
        
        # Set up callback for avatar messages
        self.avatar.set_message_callback(self._on_avatar_message)
        
        self._create_widgets()
        self._update_display()
    
    def _create_widgets(self):
        """Create the panel widgets."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Avatar Display Section ===
        avatar_frame = ttk.LabelFrame(self, text="🤖 NetworkBuster Avatar", padding=10)
        avatar_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        avatar_frame.columnconfigure(1, weight=1)
        
        # ASCII Art Display
        self.art_label = tk.Text(
            avatar_frame,
            height=8,
            width=20,
            font=("Consolas", 10),
            bg="#1a1a2e",
            fg="#00d9ff",
            relief="flat",
            state="disabled"
        )
        self.art_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        
        # Avatar Info
        info_frame = ttk.Frame(avatar_frame)
        info_frame.grid(row=0, column=1, sticky="nw", padx=10)
        
        self.name_label = ttk.Label(
            info_frame,
            text=f"Name: {self.avatar.name}",
            font=("Segoe UI", 11, "bold")
        )
        self.name_label.pack(anchor="w")
        
        self.mood_label = ttk.Label(
            info_frame,
            text=f"Mood: {self.avatar.get_mood_emoji()} {self.avatar.mood.value.title()}",
            font=("Segoe UI", 10)
        )
        self.mood_label.pack(anchor="w", pady=2)
        
        self.state_label = ttk.Label(
            info_frame,
            text=f"State: {self.avatar.state.value.title()}",
            font=("Segoe UI", 10)
        )
        self.state_label.pack(anchor="w", pady=2)
        
        # Stats Display
        stats_frame = ttk.Frame(avatar_frame)
        stats_frame.grid(row=1, column=1, sticky="nw", padx=10, pady=5)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="📊 Logs: 0 | ♻️ Recycled: 0 | ⚠️ Alerts: 0",
            font=("Segoe UI", 9)
        )
        self.stats_label.pack(anchor="w")
        
        # Current Message
        message_frame = ttk.LabelFrame(avatar_frame, text="💬 Latest Message", padding=5)
        message_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        self.current_message = ttk.Label(
            message_frame,
            text="...",
            font=("Segoe UI", 10),
            wraplength=400
        )
        self.current_message.pack(anchor="w", fill="x")
        
        # === Action Buttons ===
        button_frame = ttk.Frame(avatar_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame,
            text="👋 Greet",
            command=self._greet
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="📊 Status",
            command=self._show_status
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="🎲 Random Mood",
            command=self._random_mood
        ).pack(side="left", padx=5)
        
        # === Message History ===
        history_frame = ttk.LabelFrame(self, text="📜 Message History", padding=5)
        history_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        self.history_text = tk.Text(
            history_frame,
            height=15,
            font=("Consolas", 9),
            bg="#0f0f1a",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            selectbackground="#3a3a5a",
            relief="flat",
            state="disabled",
            wrap="word"
        )
        self.history_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        # Configure tags for message types
        self.history_text.tag_configure("timestamp", foreground="#808080")
        self.history_text.tag_configure("message", foreground="#ffffff")
        self.history_text.tag_configure("happy", foreground="#00ff88")
        self.history_text.tag_configure("alert", foreground="#ff6666")
        self.history_text.tag_configure("success", foreground="#00d9ff")
    
    def _on_avatar_message(self, message: AvatarMessage):
        """Handle new avatar message."""
        self._update_display()
        self._add_to_history(message)
    
    def _update_display(self):
        """Update the avatar display."""
        # Update ASCII art
        art = self.avatar.get_avatar_art()
        self.art_label.config(state="normal")
        self.art_label.delete("1.0", tk.END)
        self.art_label.insert("1.0", art)
        self.art_label.config(state="disabled")
        
        # Update mood and state
        self.mood_label.config(text=f"Mood: {self.avatar.get_mood_emoji()} {self.avatar.mood.value.title()}")
        self.state_label.config(text=f"State: {self.avatar.state.value.title()}")
        
        # Update stats
        stats = self.avatar.stats
        self.stats_label.config(
            text=f"📊 Logs: {stats['logs_processed']} | ♻️ Recycled: {stats['data_recycled']} | ⚠️ Alerts: {stats['alerts_sent']}"
        )
        
        # Update current message
        last_msg = self.avatar.get_last_message()
        if last_msg:
            self.current_message.config(text=last_msg.text)
    
    def _add_to_history(self, message: AvatarMessage):
        """Add a message to the history."""
        self.history_text.config(state="normal")
        
        # Add timestamp
        timestamp = message.timestamp.strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message with mood-based color
        tag = "message"
        if message.mood == AvatarMood.HAPPY or message.mood == AvatarMood.SUCCESS:
            tag = "happy"
        elif message.mood == AvatarMood.ALERT or message.mood == AvatarMood.ERROR:
            tag = "alert"
        
        self.history_text.insert(tk.END, f"{message.text}\n", tag)
        
        # Scroll to bottom
        self.history_text.see(tk.END)
        self.history_text.config(state="disabled")
    
    def _greet(self):
        """Make avatar greet."""
        import random
        greetings = [
            "Hello there! 👋",
            "Nice to see you! How can I help?",
            "Greetings, human! Ready to bust some networks?",
            "Hey! Let's get to work! 💪",
        ]
        self.avatar.say(random.choice(greetings), AvatarMood.HAPPY)
    
    def _show_status(self):
        """Show avatar status."""
        status = self.avatar.get_status_text()
        self.avatar.say(status, AvatarMood.NEUTRAL)
    
    def _random_mood(self):
        """Set a random mood."""
        import random
        moods = list(AvatarMood)
        mood = random.choice(moods)
        self.avatar.mood = mood
        self.avatar.say(f"Feeling {mood.value} now! {self.avatar.get_mood_emoji()}", mood)
