"""
NetworkBuster Software - Data Recycler
Data transformation, storage, and reuse engine
"""

import json
import csv
import hashlib
import threading
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from collections import defaultdict


@dataclass
class DataRecord:
    """A single data record in the recycler."""
    id: str
    data: Dict[str, Any]
    source: str
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    recycled_count: int = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "data": self.data,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "tags": self.tags,
            "recycled_count": self.recycled_count,
        }
    
    @classmethod
    def from_dict(cls, d: dict) -> 'DataRecord':
        """Create from dictionary."""
        return cls(
            id=d["id"],
            data=d["data"],
            source=d["source"],
            created_at=datetime.fromisoformat(d.get("created_at", datetime.now().isoformat())),
            modified_at=datetime.fromisoformat(d.get("modified_at", datetime.now().isoformat())),
            tags=d.get("tags", []),
            recycled_count=d.get("recycled_count", 0),
        )


class DataTransformer:
    """Collection of data transformation functions."""
    
    @staticmethod
    def uppercase(data: dict) -> dict:
        """Transform all string values to uppercase."""
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                result[k] = v.upper()
            else:
                result[k] = v
        return result
    
    @staticmethod
    def lowercase(data: dict) -> dict:
        """Transform all string values to lowercase."""
        result = {}
        for k, v in data.items():
            if isinstance(v, str):
                result[k] = v.lower()
            else:
                result[k] = v
        return result
    
    @staticmethod
    def flatten(data: dict, prefix: str = "") -> dict:
        """Flatten nested dictionaries."""
        result = {}
        for k, v in data.items():
            new_key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                result.update(DataTransformer.flatten(v, new_key))
            else:
                result[new_key] = v
        return result
    
    @staticmethod
    def filter_keys(data: dict, keys: List[str]) -> dict:
        """Keep only specified keys."""
        return {k: v for k, v in data.items() if k in keys}
    
    @staticmethod
    def remove_keys(data: dict, keys: List[str]) -> dict:
        """Remove specified keys."""
        return {k: v for k, v in data.items() if k not in keys}
    
    @staticmethod
    def add_timestamp(data: dict) -> dict:
        """Add a timestamp to the data."""
        result = dict(data)
        result["_timestamp"] = datetime.now().isoformat()
        return result
    
    @staticmethod
    def merge(data1: dict, data2: dict) -> dict:
        """Merge two dictionaries."""
        result = dict(data1)
        result.update(data2)
        return result


class DataRecycler:
    """
    Data recycling engine for NetworkBuster.
    Stores, transforms, and reuses data efficiently.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize the data recycler."""
        self.storage_path = storage_path or Path("data/recycler")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.records: Dict[str, DataRecord] = {}
        self.tags_index: Dict[str, set] = defaultdict(set)
        self.transformers: Dict[str, Callable] = {
            "uppercase": DataTransformer.uppercase,
            "lowercase": DataTransformer.lowercase,
            "flatten": DataTransformer.flatten,
            "add_timestamp": DataTransformer.add_timestamp,
        }
        self._lock = threading.Lock()
        
        # Stats
        self.stats = {
            "total_records": 0,
            "total_recycled": 0,
            "total_exported": 0,
            "total_imported": 0,
        }
        
        # Load existing data
        self._load_from_disk()
    
    def _generate_id(self, data: dict) -> str:
        """Generate a unique ID for data."""
        content = json.dumps(data, sort_keys=True, default=str)
        hash_val = hashlib.md5(content.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"rec_{timestamp}_{hash_val}"
    
    def add(self, data: Dict[str, Any], source: str = "manual", tags: List[str] = None) -> DataRecord:
        """Add new data to the recycler."""
        record_id = self._generate_id(data)
        
        record = DataRecord(
            id=record_id,
            data=data,
            source=source,
            tags=tags or []
        )
        
        with self._lock:
            self.records[record_id] = record
            self.stats["total_records"] += 1
            
            # Update tag index
            for tag in record.tags:
                self.tags_index[tag].add(record_id)
        
        self._save_to_disk()
        return record
    
    def get(self, record_id: str) -> Optional[DataRecord]:
        """Get a record by ID."""
        with self._lock:
            return self.records.get(record_id)
    
    def update(self, record_id: str, data: Dict[str, Any]) -> Optional[DataRecord]:
        """Update a record's data."""
        with self._lock:
            if record_id not in self.records:
                return None
            
            record = self.records[record_id]
            record.data = data
            record.modified_at = datetime.now()
        
        self._save_to_disk()
        return record
    
    def delete(self, record_id: str) -> bool:
        """Delete a record."""
        with self._lock:
            if record_id not in self.records:
                return False
            
            record = self.records[record_id]
            
            # Remove from tag index
            for tag in record.tags:
                self.tags_index[tag].discard(record_id)
            
            del self.records[record_id]
            self.stats["total_records"] -= 1
        
        self._save_to_disk()
        return True
    
    def recycle(self, record_id: str, transformer_name: str) -> Optional[DataRecord]:
        """
        Recycle (transform) a record's data and create a new record.
        """
        with self._lock:
            if record_id not in self.records:
                return None
            
            if transformer_name not in self.transformers:
                return None
            
            original = self.records[record_id]
            transformer = self.transformers[transformer_name]
        
        # Apply transformation
        new_data = transformer(original.data)
        
        # Create new record
        new_record = self.add(
            data=new_data,
            source=f"recycled:{original.id}:{transformer_name}",
            tags=original.tags + ["recycled"]
        )
        
        # Update original's recycled count
        with self._lock:
            original.recycled_count += 1
            self.stats["total_recycled"] += 1
        
        self._save_to_disk()
        return new_record
    
    def search_by_tags(self, tags: List[str]) -> List[DataRecord]:
        """Search records by tags (AND logic)."""
        with self._lock:
            if not tags:
                return list(self.records.values())
            
            # Find IDs that have all tags
            matching_ids = None
            for tag in tags:
                tag_ids = self.tags_index.get(tag, set())
                if matching_ids is None:
                    matching_ids = tag_ids.copy()
                else:
                    matching_ids &= tag_ids
            
            if not matching_ids:
                return []
            
            return [self.records[rid] for rid in matching_ids if rid in self.records]
    
    def get_all(self, limit: int = 100) -> List[DataRecord]:
        """Get all records."""
        with self._lock:
            records = list(self.records.values())
        return sorted(records, key=lambda r: r.created_at, reverse=True)[:limit]
    
    def export_json(self, filepath: Path = None) -> str:
        """Export all records to JSON."""
        with self._lock:
            records = [r.to_dict() for r in self.records.values()]
        
        output = json.dumps(records, indent=2, default=str)
        
        if filepath:
            filepath.write_text(output, encoding='utf-8')
            self.stats["total_exported"] += len(records)
        
        return output
    
    def export_csv(self, filepath: Path) -> int:
        """Export records to CSV."""
        with self._lock:
            records = list(self.records.values())
        
        if not records:
            return 0
        
        # Get all keys from all records
        all_keys = set()
        for record in records:
            all_keys.update(record.data.keys())
        
        fieldnames = ["id", "source", "created_at", "tags"] + sorted(all_keys)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for record in records:
                row = {
                    "id": record.id,
                    "source": record.source,
                    "created_at": record.created_at.isoformat(),
                    "tags": ",".join(record.tags),
                    **record.data
                }
                writer.writerow(row)
        
        self.stats["total_exported"] += len(records)
        return len(records)
    
    def import_json(self, filepath: Path) -> int:
        """Import records from JSON file."""
        try:
            content = filepath.read_text(encoding='utf-8')
            records_data = json.loads(content)
            
            count = 0
            for item in records_data:
                if isinstance(item, dict) and "data" in item:
                    record = DataRecord.from_dict(item)
                    with self._lock:
                        self.records[record.id] = record
                        for tag in record.tags:
                            self.tags_index[tag].add(record.id)
                    count += 1
                elif isinstance(item, dict):
                    # Treat the whole item as data
                    self.add(item, source=f"import:{filepath.name}")
                    count += 1
            
            self.stats["total_imported"] += count
            self._save_to_disk()
            return count
        except Exception as e:
            return 0
    
    def _save_to_disk(self):
        """Save records to disk."""
        try:
            data_file = self.storage_path / "records.json"
            with self._lock:
                records = [r.to_dict() for r in self.records.values()]
            data_file.write_text(json.dumps(records, indent=2, default=str), encoding='utf-8')
        except Exception:
            pass
    
    def _load_from_disk(self):
        """Load records from disk."""
        try:
            data_file = self.storage_path / "records.json"
            if data_file.exists():
                content = data_file.read_text(encoding='utf-8')
                records_data = json.loads(content)
                
                for item in records_data:
                    record = DataRecord.from_dict(item)
                    self.records[record.id] = record
                    for tag in record.tags:
                        self.tags_index[tag].add(record.id)
                
                self.stats["total_records"] = len(self.records)
        except Exception:
            pass
    
    def get_stats(self) -> dict:
        """Get recycler statistics."""
        with self._lock:
            stats = dict(self.stats)
            stats["unique_tags"] = len(self.tags_index)
            stats["storage_path"] = str(self.storage_path)
        return stats
    
    def clear_all(self):
        """Clear all records."""
        with self._lock:
            self.records.clear()
            self.tags_index.clear()
            self.stats["total_records"] = 0
        self._save_to_disk()
