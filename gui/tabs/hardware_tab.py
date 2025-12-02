import tkinter as tk
from tkinter import ttk
import random

class HardwareTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.title = "Процессор и память"
        self.create_tab()
    
    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        
        metrics_frame = ttk.Frame(self.frame)
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_cpu_section(metrics_frame)
        
        self.create_memory_section(metrics_frame)
        
        # Графики (заглушки)
        self.create_graph_section()
    
    def create_cpu_section(self, parent):
        cpu_frame = ttk.LabelFrame(parent, text="Процессор")
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.cpu_label = ttk.Label(cpu_frame, text="Загрузка: 45%", font=("Arial", 14))
        self.cpu_label.pack(pady=20)
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(pady=10)
        self.cpu_progress['value'] = 45
    
    def create_memory_section(self, parent):
        mem_frame = ttk.LabelFrame(parent, text="Оперативная память")
        mem_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.mem_label = ttk.Label(mem_frame, text="8.2 / 16.0 GB (51%)", font=("Arial", 14))
        self.mem_label.pack(pady=20)
        
        self.mem_progress = ttk.Progressbar(mem_frame, length=200, mode='determinate')
        self.mem_progress.pack(pady=10)
        self.mem_progress['value'] = 51
    
    def create_graph_section(self):
        graph_frame = ttk.LabelFrame(self.frame, text="История использования")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.graph_placeholder = tk.Canvas(graph_frame, bg='#f0f0f0', height=200)
        self.graph_placeholder.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def draw_centered_text():
            width = self.graph_placeholder.winfo_width()
            height = self.graph_placeholder.winfo_height()
            
            if width < 10:
                width = 400
                height = 200
            
            self.graph_placeholder.delete("all")
            self.graph_placeholder.create_text(
                width // 2,
                height // 2,
                text="График загрузки CPU и памяти\n(будет реализован в следующей версии)",
                font=("Arial", 10),
                fill="gray",
                anchor="center",
                justify="center"
            )
        
        self.graph_placeholder.bind("<Configure>", lambda e: draw_centered_text())
        draw_centered_text()
    
    def update_data(self):
        # Имитируем изменение значений
        cpu_usage = random.randint(10, 90)
        mem_usage = random.randint(20, 80)
        
        self.cpu_label.config(text=f"Загрузка: {cpu_usage}%")
        self.cpu_progress['value'] = cpu_usage
        
        used_gb = random.randint(4, 12)
        used_mb = random.randint(0, 9)
        self.mem_label.config(text=f"{used_gb}.{used_mb} / 16.0 GB ({mem_usage}%)")
        self.mem_progress['value'] = mem_usage