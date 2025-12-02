import tkinter as tk
from tkinter import ttk

class Toolbar:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_toolbar()
    
    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Кнопки
        self.collect_btn = ttk.Button(
            self.toolbar, 
            text="▶ Собрать данные", 
            command=self.app.collect_data,
            width=15
        )
        self.collect_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = ttk.Button(
            self.toolbar, 
            text="⏹ Остановить", 
            command=self.app.stop_collection,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.toolbar, text="Экспорт:").pack(side=tk.LEFT, padx=2)
        self.export_format = tk.StringVar(value="JSON")
        format_combo = ttk.Combobox(
            self.toolbar, 
            textvariable=self.export_format,
            values=["JSON", "CSV", "SQLite"],
            state="readonly",
            width=10
        )
        format_combo.pack(side=tk.LEFT, padx=2)
        
        self.export_btn = ttk.Button(
            self.toolbar, 
            text="📁 Экспорт", 
            command=self.app.export_data,
            width=10
        )
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5)
        ttk.Label(self.toolbar, text="Интервал (сек):").pack(side=tk.LEFT, padx=2)
        self.interval_var = tk.StringVar(value="5")
        interval_spin = ttk.Spinbox(
            self.toolbar,
            from_=1,
            to=60,
            textvariable=self.interval_var,
            width=5
        )
        interval_spin.pack(side=tk.LEFT, padx=2)
    
    def set_collecting_state(self, is_collecting):
        if is_collecting:
            self.collect_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
        else:
            self.collect_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def get_interval(self):
        try:
            return int(self.interval_var.get())
        except:
            return 5
    
    def get_export_format(self):
        return self.export_format.get()