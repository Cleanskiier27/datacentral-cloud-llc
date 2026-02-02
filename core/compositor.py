"""
NetworkBuster Software - Real-Time Compositor
Live data composition and aggregation engine
"""

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from collections import deque
import json


@dataclass
class CompositionEvent:
    """An event in the composition stream."""
    source: str
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class CompositionSnapshot:
    """A snapshot of the current composition state."""
    timestamp: datetime
    sources: Dict[str, int]  # source -> event count
    event_types: Dict[str, int]  # event_type -> count
    total_events: int
    events_per_second: float
    recent_events: List[CompositionEvent]
    
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "sources": self.sources,
            "event_types": self.event_types,
            "total_events": self.total_events,
            "events_per_second": round(self.events_per_second, 2),
            "recent_events_count": len(self.recent_events),
        }


class DataSource:
    """A data source that feeds into the compositor."""
    
    def __init__(self, name: str, compositor: 'RealTimeCompositor'):
        self.name = name
        self.compositor = compositor
        self.enabled = True
        self.event_count = 0
    
    def emit(self, event_type: str, data: Dict[str, Any]):
        """Emit an event to the compositor."""
        if self.enabled:
            self.event_count += 1
            self.compositor.receive_event(
                source=self.name,
                event_type=event_type,
                data=data
            )
    
    def disable(self):
        """Disable this source."""
        self.enabled = False
    
    def enable(self):
        """Enable this source."""
        self.enabled = True


class RealTimeCompositor:
    """
    Real-time data composition engine.
    Aggregates data from multiple sources and provides live visualization.
    """
    
    def __init__(self, max_events: int = 10000, window_seconds: int = 60):
        """
        Initialize the compositor.
        
        Args:
            max_events: Maximum events to keep in memory
            window_seconds: Time window for rate calculations
        """
        self.max_events = max_events
        self.window_seconds = window_seconds
        
        self.events: deque = deque(maxlen=max_events)
        self.sources: Dict[str, DataSource] = {}
        self.callbacks: List[Callable[[CompositionEvent], None]] = []
        self._lock = threading.Lock()
        
        # Aggregation state
        self.source_counts: Dict[str, int] = {}
        self.type_counts: Dict[str, int] = {}
        self.total_events = 0
        
        # Rate tracking
        self.window_events: deque = deque()  # Events in the current time window
        
        # Running state
        self.running = False
        self._worker_thread: Optional[threading.Thread] = None
    
    def register_source(self, name: str) -> DataSource:
        """Register a new data source."""
        with self._lock:
            if name not in self.sources:
                self.sources[name] = DataSource(name, self)
                self.source_counts[name] = 0
            return self.sources[name]
    
    def unregister_source(self, name: str):
        """Unregister a data source."""
        with self._lock:
            if name in self.sources:
                del self.sources[name]
    
    def get_source(self, name: str) -> Optional[DataSource]:
        """Get a registered source by name."""
        return self.sources.get(name)
    
    def receive_event(self, source: str, event_type: str, data: Dict[str, Any]):
        """Receive an event from a source."""
        event = CompositionEvent(
            source=source,
            event_type=event_type,
            data=data
        )
        
        with self._lock:
            self.events.append(event)
            self.window_events.append(event)
            self.total_events += 1
            
            # Update counts
            self.source_counts[source] = self.source_counts.get(source, 0) + 1
            self.type_counts[event_type] = self.type_counts.get(event_type, 0) + 1
        
        # Trigger callbacks
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception:
                pass
    
    def add_callback(self, callback: Callable[[CompositionEvent], None]):
        """Add a callback for new events."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[CompositionEvent], None]):
        """Remove a callback."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _clean_window_events(self):
        """Remove old events from the rate calculation window."""
        cutoff = datetime.now().timestamp() - self.window_seconds
        
        with self._lock:
            while self.window_events and self.window_events[0].timestamp.timestamp() < cutoff:
                self.window_events.popleft()
    
    def get_events_per_second(self) -> float:
        """Get the current events per second rate."""
        self._clean_window_events()
        
        with self._lock:
            if not self.window_events:
                return 0.0
            
            events = len(self.window_events)
            return events / self.window_seconds
    
    def get_snapshot(self, recent_count: int = 10) -> CompositionSnapshot:
        """Get a snapshot of the current composition state."""
        self._clean_window_events()
        
        with self._lock:
            recent_events = list(self.events)[-recent_count:]
            
            return CompositionSnapshot(
                timestamp=datetime.now(),
                sources=dict(self.source_counts),
                event_types=dict(self.type_counts),
                total_events=self.total_events,
                events_per_second=self.get_events_per_second(),
                recent_events=recent_events
            )
    
    def get_recent_events(self, count: int = 100, source: str = None, event_type: str = None) -> List[CompositionEvent]:
        """Get recent events with optional filtering."""
        with self._lock:
            events = list(self.events)
        
        if source:
            events = [e for e in events if e.source == source]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-count:]
    
    def get_sources_summary(self) -> Dict[str, dict]:
        """Get a summary of all sources."""
        with self._lock:
            summary = {}
            for name, source in self.sources.items():
                summary[name] = {
                    "name": name,
                    "enabled": source.enabled,
                    "event_count": source.event_count,
                }
            return summary
    
    def get_type_distribution(self) -> Dict[str, float]:
        """Get the distribution of event types as percentages."""
        with self._lock:
            if self.total_events == 0:
                return {}
            
            return {
                event_type: (count / self.total_events) * 100
                for event_type, count in self.type_counts.items()
            }
    
    def start(self):
        """Start the compositor's background processing."""
        if self.running:
            return
        
        self.running = True
        
        def worker():
            while self.running:
                self._clean_window_events()
                time.sleep(1)
        
        self._worker_thread = threading.Thread(target=worker, daemon=True)
        self._worker_thread.start()
    
    def stop(self):
        """Stop the compositor."""
        self.running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=2)
    
    def clear(self):
        """Clear all events and reset counts."""
        with self._lock:
            self.events.clear()
            self.window_events.clear()
            self.source_counts.clear()
            self.type_counts.clear()
            self.total_events = 0
    
    def export_events(self, filepath: str, format: str = "json") -> int:
        """Export events to a file."""
        with self._lock:
            events = [e.to_dict() for e in self.events]
        
        if format == "json":
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, default=str)
        elif format == "ndjson":
            with open(filepath, 'w', encoding='utf-8') as f:
                for event in events:
                    f.write(json.dumps(event, default=str) + "\n")
        
        return len(events)
    
    def get_stats(self) -> dict:
        """Get compositor statistics."""
        with self._lock:
            return {
                "total_events": self.total_events,
                "events_in_memory": len(self.events),
                "events_in_window": len(self.window_events),
                "events_per_second": round(self.get_events_per_second(), 2),
                "sources_count": len(self.sources),
                "event_types_count": len(self.type_counts),
                "running": self.running,
            }
