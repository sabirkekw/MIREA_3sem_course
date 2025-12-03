import tkinter as tk
from tkinter import ttk
from utils.formatters import format_bytes

class SystemTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.title = "Общая информация"
        self.create_tab()
    
    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Обновить", command=self.update_data).pack(side=tk.RIGHT)
        
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_system_info(main_frame)
        
        self.create_hardware_info(main_frame)
    
    def create_system_info(self, parent):
        self.left_frame = ttk.LabelFrame(parent, text="Система")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.system_labels = {}
        system_fields = [
            ("os", "Операционная система:"),
            ("version", "Версия ОС:"),
            ("arch", "Архитектура:"),
            ("hostname", "Имя компьютера:"),
            ("username", "Имя пользователя:"),
            ("boot_time", "Время запуска:"),
        ]
        
        for key, label in system_fields:
            row = ttk.Frame(self.left_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.system_labels[key] = ttk.Label(row, text="", anchor="w")
            self.system_labels[key].pack(side=tk.LEFT)
    
    def create_hardware_info(self, parent):
        self.right_frame = ttk.LabelFrame(parent, text="Аппаратное обеспечение")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.hardware_labels = {}
        hardware_fields = [
            ("cpu", "Процессор:"),
            ("cores", "Количество ядер:"),
            ("freq", "Частота:"),
            ("ram", "Объем ОЗУ:"),
            ("ram_used", "Использовано ОЗУ:"),
            ("ram_percent", "Использование ОЗУ:"),
        ]
        
        for key, label in hardware_fields:
            row = ttk.Frame(self.right_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.hardware_labels[key] = ttk.Label(row, text="", anchor="w")
            self.hardware_labels[key].pack(side=tk.LEFT)
    
    def update_data(self):
        self.app.update_all_data()
    
    def update_with_snapshot(self, snapshot):
        if not snapshot:
            return
        
        system = snapshot.system
        self.system_labels['os'].config(text=f"{system.os_name}")
        self.system_labels['version'].config(text=system.os_version)
        self.system_labels['arch'].config(text=system.architecture)
        self.system_labels['hostname'].config(text=system.hostname)
        self.system_labels['username'].config(text=system.username)
        
        if system.boot_time:
            from datetime import datetime
            boot_time_str = system.boot_time.strftime("%Y-%m-%d %H:%M:%S")
            self.system_labels['boot_time'].config(text=boot_time_str)
        
        cpu = snapshot.cpu
        memory = snapshot.memory
        
        self.hardware_labels['cpu'].config(text=cpu.name)
        self.hardware_labels['cores'].config(text=f"{cpu.physical_cores} физических, {cpu.logical_cores} логических")
        self.hardware_labels['freq'].config(text=f"{cpu.frequency_current:.1f} MHz")
        self.hardware_labels['ram'].config(text=format_bytes(memory.total))
        self.hardware_labels['ram_used'].config(text=format_bytes(memory.used))
        self.hardware_labels['ram_percent'].config(text=f"{memory.usage_percent:.1f}%")