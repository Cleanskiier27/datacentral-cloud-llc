"""
NetworkBuster Software - Data Panel
Data recycling interface for managing and transforming data
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from typing import Optional
import sys
import os
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_recycler import DataRecycler, DataRecord
from config import COLORS


class DataPanel(ttk.Frame):
    """
    Data recycling panel with data management and transformation tools.
    """
    
    def __init__(self, parent, data_recycler: DataRecycler, on_data_recycled=None):
        super().__init__(parent)
        self.data_recycler = data_recycler
        self.on_data_recycled_callback = on_data_recycled
        
        self._create_widgets()
        self._refresh_data()
    
    def _create_widgets(self):
        """Create the panel widgets."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # === Control Section ===
        control_frame = ttk.LabelFrame(self, text="♻️ Data Recycler Controls", padding=10)
        control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill="x")
        
        ttk.Button(
            btn_frame,
            text="➕ Add Data",
            command=self._add_data
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="📂 Import JSON",
            command=self._import_json
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="💾 Export JSON",
            command=self._export_json
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="📊 Export CSV",
            command=self._export_csv
        ).pack(side="left", padx=5)
        
        ttk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self._refresh_data
        ).pack(side="left", padx=5)
        
        # Stats
        stats_frame = ttk.Frame(control_frame)
        stats_frame.pack(fill="x", pady=10)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="Records: 0 | Recycled: 0 | Tags: 0",
            font=("Segoe UI", 10)
        )
        self.stats_label.pack(side="left")
        
        # Transform controls
        transform_frame = ttk.LabelFrame(control_frame, text="🔧 Transform Selected", padding=5)
        transform_frame.pack(fill="x", pady=5)
        
        transform_btns = ttk.Frame(transform_frame)
        transform_btns.pack(fill="x")
        
        for name, label in [
            ("uppercase", "ABC→"),
            ("lowercase", "abc→"),
            ("flatten", "Flatten"),
            ("add_timestamp", "+Time")
        ]:
            ttk.Button(
                transform_btns,
                text=label,
                command=lambda n=name: self._transform_selected(n),
                width=10
            ).pack(side="left", padx=2)
        
        ttk.Button(
            transform_btns,
            text="🗑️ Delete",
            command=self._delete_selected
        ).pack(side="right", padx=2)
        
        # === Data Display ===
        data_frame = ttk.LabelFrame(self, text="📦 Data Records", padding=5)
        data_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
        # Treeview for data records
        columns = ("id", "source", "tags", "recycled", "created")
        self.data_tree = ttk.Treeview(
            data_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Column configuration
        self.data_tree.heading("id", text="ID")
        self.data_tree.heading("source", text="Source")
        self.data_tree.heading("tags", text="Tags")
        self.data_tree.heading("recycled", text="Recycled")
        self.data_tree.heading("created", text="Created")
        
        self.data_tree.column("id", width=150, minwidth=100)
        self.data_tree.column("source", width=120, minwidth=80)
        self.data_tree.column("tags", width=150, minwidth=100)
        self.data_tree.column("recycled", width=80, minwidth=60)
        self.data_tree.column("created", width=150, minwidth=100)
        
        self.data_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(data_frame, orient="vertical", command=self.data_tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.data_tree.config(yscrollcommand=y_scroll.set)
        
        # Tag colors
        self.data_tree.tag_configure("recycled", foreground="#00d9ff")
        
        # Double-click to view details
        self.data_tree.bind("<Double-1>", self._show_record_details)
        self.data_tree.bind("<<TreeviewSelect>>", self._on_selection_change)
        
        # === Detail View ===
        detail_frame = ttk.LabelFrame(self, text="🔍 Record Details", padding=5)
        detail_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        self.detail_text = tk.Text(
            detail_frame,
            height=8,
            font=("Consolas", 9),
            bg="#0f0f1a",
            fg="#e0e0e0",
            relief="flat",
            state="disabled",
            wrap="word"
        )
        self.detail_text.pack(fill="both", expand=True)
    
    def _refresh_data(self):
        """Refresh the data display."""
        # Clear current entries
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Load records
        records = self.data_recycler.get_all(limit=500)
        
        for record in records:
            tags_str = ", ".join(record.tags) if record.tags else "-"
            created_str = record.created_at.strftime("%Y-%m-%d %H:%M")
            
            tags = ("recycled",) if "recycled" in record.tags else ()
            
            self.data_tree.insert(
                "",
                tk.END,
                iid=record.id,
                values=(record.id, record.source, tags_str, record.recycled_count, created_str),
                tags=tags
            )
        
        # Update stats
        stats = self.data_recycler.get_stats()
        self.stats_label.config(
            text=f"Records: {stats['total_records']} | Recycled: {stats['total_recycled']} | Tags: {stats['unique_tags']}"
        )
    
    def _on_selection_change(self, event):
        """Handle selection change."""
        selection = self.data_tree.selection()
        if selection:
            record_id = selection[0]
            record = self.data_recycler.get(record_id)
            if record:
                self._show_detail(record)
    
    def _show_detail(self, record: DataRecord):
        """Show record details in the detail panel."""
        self.detail_text.config(state="normal")
        self.detail_text.delete("1.0", tk.END)
        
        detail = f"ID: {record.id}\n"
        detail += f"Source: {record.source}\n"
        detail += f"Tags: {', '.join(record.tags) if record.tags else 'None'}\n"
        detail += f"Created: {record.created_at}\n"
        detail += f"Modified: {record.modified_at}\n"
        detail += f"Recycled Count: {record.recycled_count}\n"
        detail += f"\n--- Data ---\n"
        detail += json.dumps(record.data, indent=2, default=str)
        
        self.detail_text.insert("1.0", detail)
        self.detail_text.config(state="disabled")
    
    def _add_data(self):
        """Add new data manually."""
        # Simple dialog for adding data
        dialog = tk.Toplevel(self)
        dialog.title("Add Data")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter JSON data:").pack(anchor="w", padx=10, pady=5)
        
        text = tk.Text(dialog, height=10, font=("Consolas", 10))
        text.pack(fill="both", expand=True, padx=10, pady=5)
        text.insert("1.0", '{\n    "key": "value"\n}')
        
        ttk.Label(dialog, text="Tags (comma-separated):").pack(anchor="w", padx=10)
        tags_entry = ttk.Entry(dialog)
        tags_entry.pack(fill="x", padx=10, pady=5)
        
        def save():
            try:
                data = json.loads(text.get("1.0", tk.END))
                tags = [t.strip() for t in tags_entry.get().split(",") if t.strip()]
                self.data_recycler.add(data, source="manual", tags=tags)
                self._refresh_data()
                dialog.destroy()
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Invalid JSON: {e}")
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=10)
    
    def _transform_selected(self, transformer_name: str):
        """Transform the selected record."""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a record to transform.")
            return
        
        record_id = selection[0]
        new_record = self.data_recycler.recycle(record_id, transformer_name)
        
        if new_record:
            self._refresh_data()
            # Select the new record
            self.data_tree.selection_set(new_record.id)
            self.data_tree.see(new_record.id)
            
            # Notify callback
            if self.on_data_recycled_callback:
                self.on_data_recycled_callback(1)
            
            messagebox.showinfo("Success", f"Data recycled! New record: {new_record.id}")
        else:
            messagebox.showerror("Error", "Failed to transform data.")
    
    def _delete_selected(self):
        """Delete the selected record."""
        selection = self.data_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a record to delete.")
            return
        
        record_id = selection[0]
        if messagebox.askyesno("Confirm", f"Delete record {record_id}?"):
            self.data_recycler.delete(record_id)
            self._refresh_data()
    
    def _show_record_details(self, event):
        """Show full details in a dialog."""
        selection = self.data_tree.selection()
        if selection:
            record_id = selection[0]
            record = self.data_recycler.get(record_id)
            if record:
                detail = json.dumps(record.to_dict(), indent=2, default=str)
                
                dialog = tk.Toplevel(self)
                dialog.title(f"Record: {record_id}")
                dialog.geometry("500x400")
                
                text = tk.Text(dialog, font=("Consolas", 10), wrap="word")
                text.pack(fill="both", expand=True, padx=10, pady=10)
                text.insert("1.0", detail)
                text.config(state="disabled")
    
    def _import_json(self):
        """Import data from JSON file."""
        filepath = filedialog.askopenfilename(
            title="Import JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filepath:
            count = self.data_recycler.import_json(Path(filepath))
            self._refresh_data()
            messagebox.showinfo("Import Complete", f"Imported {count} records.")
    
    def _export_json(self):
        """Export data to JSON file."""
        filepath = filedialog.asksaveasfilename(
            title="Export JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filepath:
            self.data_recycler.export_json(Path(filepath))
            messagebox.showinfo("Export Complete", f"Data exported to {filepath}")
    
    def _export_csv(self):
        """Export data to CSV file."""
        filepath = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if filepath:
            count = self.data_recycler.export_csv(Path(filepath))
            messagebox.showinfo("Export Complete", f"Exported {count} records to {filepath}")
