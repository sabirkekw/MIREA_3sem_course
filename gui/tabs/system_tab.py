import tkinter as tk
from tkinter import ttk

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
        left_frame = ttk.LabelFrame(parent, text="Система")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.system_labels = {}
        system_info = [
            ("os", "Операционная система:", "Windows 10 Pro"),
            ("version", "Версия ОС:", "10.0.19045"),
            ("arch", "Архитектура:", "64-bit"),
            ("hostname", "Имя компьютера:", "DESKTOP-ABC123"),
            ("username", "Имя пользователя:", "Admin"),
            ("boot_time", "Время запуска:", "2024-01-15 08:30:15"),
        ]
        
        for key, label, value in system_info:
            row = ttk.Frame(left_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.system_labels[key] = ttk.Label(row, text=value, anchor="w")
            self.system_labels[key].pack(side=tk.LEFT)
    
    def create_hardware_info(self, parent):
        right_frame = ttk.LabelFrame(parent, text="Аппаратное обеспечение")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.hardware_labels = {}
        hardware_info = [
            ("cpu", "Процессор:", "Intel Core i7-9700"),
            ("cores", "Количество ядер:", "8 (4 физических)"),
            ("freq", "Частота:", "3.0 GHz"),
            ("ram", "Объем ОЗУ:", "16.0 GB"),
            ("gpu", "Видеокарта:", "NVIDIA GeForce RTX 3060"),
            ("vram", "Объем VRAM:", "12.0 GB"),
        ]
        
        for key, label, value in hardware_info:
            row = ttk.Frame(right_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.hardware_labels[key] = ttk.Label(row, text=value, anchor="w")
            self.hardware_labels[key].pack(side=tk.LEFT)
    
    def update_data(self):
        pass