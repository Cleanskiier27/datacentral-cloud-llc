"""
NetworkBuster Software - Avatar System
Interactive avatar interface for user communication and feedback
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional
from datetime import datetime


class AvatarMood(Enum):
    """Avatar emotional states."""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    THINKING = "thinking"
    ALERT = "alert"
    WORKING = "working"
    SUCCESS = "success"
    ERROR = "error"


class AvatarState(Enum):
    """Avatar activity states."""
    IDLE = "idle"
    MONITORING = "monitoring"
    PROCESSING = "processing"
    ANALYZING = "analyzing"
    ALERTING = "alerting"


@dataclass
class AvatarMessage:
    """A message from the avatar."""
    text: str
    mood: AvatarMood
    timestamp: datetime
    priority: int = 0  # 0=normal, 1=important, 2=critical


class Avatar:
    """
    NetworkBuster Avatar - Interactive companion for the application.
    Provides feedback, status updates, and interacts with the user.
    """
    
    # Greeting messages
    GREETINGS = [
        "👋 Welcome to NetworkBuster! I'm your digital assistant.",
        "🚀 NetworkBuster initialized! Ready to monitor and analyze.",
        "💫 Hello! I'm here to help you manage your data and logs.",
        "🔮 System online! Let's get to work.",
    ]
    
    # Status messages for different states
    STATUS_MESSAGES = {
        AvatarState.IDLE: [
            "Standing by, ready for action...",
            "All systems nominal. Awaiting instructions.",
            "Monitoring the horizon for activity...",
        ],
        AvatarState.MONITORING: [
            "👀 Watching log files for changes...",
            "📡 Scanning for new log entries...",
            "🔍 Monitoring active - all eyes on your files!",
        ],
        AvatarState.PROCESSING: [
            "⚙️ Processing data streams...",
            "🔄 Crunching numbers...",
            "💫 Working on it!",
        ],
        AvatarState.ANALYZING: [
            "🧠 Analyzing patterns...",
            "📊 Running deep analysis...",
            "🔬 Examining the data closely...",
        ],
        AvatarState.ALERTING: [
            "⚠️ Attention required!",
            "🚨 Something needs your attention!",
            "❗ Alert detected!",
        ],
    }
    
    # Activity-specific responses
    ACTIVITY_RESPONSES = {
        "log_new": [
            "📝 New log entry detected!",
            "✨ Fresh log data incoming!",
            "📋 Got a new log entry here.",
        ],
        "log_error": [
            "🔴 Error detected in logs!",
            "⚠️ Spotted an error entry!",
            "❌ Something went wrong - check the logs!",
        ],
        "data_saved": [
            "💾 Data saved successfully!",
            "✅ Your data is safe and sound.",
            "📦 Data stored!",
        ],
        "data_recycled": [
            "♻️ Data recycled and transformed!",
            "🔄 Data has been processed and reused.",
            "✨ Transformation complete!",
        ],
    }
    
    def __init__(self, name: str = "Buster"):
        """Initialize the avatar."""
        self.name = name
        self.mood = AvatarMood.NEUTRAL
        self.state = AvatarState.IDLE
        self.message_history: list[AvatarMessage] = []
        self.on_message_callback: Optional[Callable[[AvatarMessage], None]] = None
        self.stats = {
            "logs_processed": 0,
            "data_recycled": 0,
            "alerts_sent": 0,
            "uptime_start": datetime.now(),
        }
        
        # Send greeting
        self._send_message(random.choice(self.GREETINGS), AvatarMood.HAPPY)
    
    def _send_message(self, text: str, mood: AvatarMood = None, priority: int = 0):
        """Internal method to send a message."""
        if mood:
            self.mood = mood
        
        message = AvatarMessage(
            text=text,
            mood=self.mood,
            timestamp=datetime.now(),
            priority=priority
        )
        
        self.message_history.append(message)
        
        # Keep history limited
        if len(self.message_history) > 100:
            self.message_history = self.message_history[-100:]
        
        # Call callback if set
        if self.on_message_callback:
            self.on_message_callback(message)
        
        return message
    
    def set_message_callback(self, callback: Callable[[AvatarMessage], None]):
        """Set callback for when avatar sends a message."""
        self.on_message_callback = callback
    
    def set_state(self, state: AvatarState):
        """Set the avatar's current activity state."""
        self.state = state
        message = random.choice(self.STATUS_MESSAGES.get(state, ["Working..."]))
        self._send_message(message, AvatarMood.WORKING if state != AvatarState.IDLE else AvatarMood.NEUTRAL)
    
    def notify_log_entry(self, is_error: bool = False):
        """Notify avatar of a new log entry."""
        self.stats["logs_processed"] += 1
        if is_error:
            message = random.choice(self.ACTIVITY_RESPONSES["log_error"])
            self._send_message(message, AvatarMood.ALERT, priority=1)
            self.stats["alerts_sent"] += 1
        else:
            message = random.choice(self.ACTIVITY_RESPONSES["log_new"])
            self._send_message(message, AvatarMood.NEUTRAL)
    
    def notify_data_saved(self):
        """Notify avatar that data was saved."""
        message = random.choice(self.ACTIVITY_RESPONSES["data_saved"])
        self._send_message(message, AvatarMood.SUCCESS)
    
    def notify_data_recycled(self, count: int = 1):
        """Notify avatar that data was recycled."""
        self.stats["data_recycled"] += count
        message = random.choice(self.ACTIVITY_RESPONSES["data_recycled"])
        self._send_message(message, AvatarMood.SUCCESS)
    
    def say(self, text: str, mood: AvatarMood = AvatarMood.NEUTRAL):
        """Make the avatar say something custom."""
        self._send_message(text, mood)
    
    def get_status_text(self) -> str:
        """Get a text description of current status."""
        uptime = datetime.now() - self.stats["uptime_start"]
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return (
            f"🤖 {self.name} | {self.mood.value.title()} | {self.state.value.title()}\n"
            f"📊 Logs: {self.stats['logs_processed']} | "
            f"♻️ Recycled: {self.stats['data_recycled']} | "
            f"⚠️ Alerts: {self.stats['alerts_sent']}\n"
            f"⏱️ Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}"
        )
    
    def get_last_message(self) -> Optional[AvatarMessage]:
        """Get the most recent message."""
        if self.message_history:
            return self.message_history[-1]
        return None
    
    def get_mood_emoji(self) -> str:
        """Get an emoji representing current mood."""
        mood_emojis = {
            AvatarMood.NEUTRAL: "😊",
            AvatarMood.HAPPY: "😄",
            AvatarMood.THINKING: "🤔",
            AvatarMood.ALERT: "😮",
            AvatarMood.WORKING: "💪",
            AvatarMood.SUCCESS: "🎉",
            AvatarMood.ERROR: "😟",
        }
        return mood_emojis.get(self.mood, "🤖")
    
    def get_avatar_art(self) -> str:
        """Get ASCII art representation of the avatar based on mood."""
        arts = {
            AvatarMood.NEUTRAL: """
    ╭──────────╮
    │  ◉    ◉  │
    │    ▽     │
    │   ───    │
    ╰──────────╯
       BUSTER
            """,
            AvatarMood.HAPPY: """
    ╭──────────╮
    │  ^    ^  │
    │    ▽     │
    │   ◡◡◡    │
    ╰──────────╯
       BUSTER
            """,
            AvatarMood.ALERT: """
    ╭──────────╮
    │  ⊙    ⊙  │
    │    ▽     │
    │    O     │
    ╰──────────╯
     ! ALERT !
            """,
            AvatarMood.WORKING: """
    ╭──────────╮
    │  ◉    ◉  │
    │    ▽     │
    │   ~~~    │
    ╰──────────╯
     WORKING...
            """,
            AvatarMood.THINKING: """
    ╭──────────╮
    │  ◉    ─  │
    │    ▽     │
    │   ~~~    │
    ╰──────────╯
    THINKING...
            """,
        }
        return arts.get(self.mood, arts[AvatarMood.NEUTRAL])
