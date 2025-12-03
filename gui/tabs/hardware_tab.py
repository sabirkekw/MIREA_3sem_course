import tkinter as tk
from tkinter import ttk
from utils.formatters import format_bytes, format_percent

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
        
        self.cpu_label = ttk.Label(cpu_frame, text="Загрузка: 0%", font=("Arial", 14))
        self.cpu_label.pack(pady=20)
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(pady=10)
        self.cpu_progress['value'] = 0
        
        self.cpu_info_label = ttk.Label(cpu_frame, text="", font=("Arial", 10))
        self.cpu_info_label.pack(pady=5)
    
    def create_memory_section(self, parent):
        mem_frame = ttk.LabelFrame(parent, text="Оперативная память")
        mem_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.mem_label = ttk.Label(mem_frame, text="0 / 0 GB (0%)", font=("Arial", 14))
        self.mem_label.pack(pady=20)
        
        self.mem_progress = ttk.Progressbar(mem_frame, length=200, mode='determinate')
        self.mem_progress.pack(pady=10)
        self.mem_progress['value'] = 0
        
        self.mem_info_label = ttk.Label(mem_frame, text="", font=("Arial", 10))
        self.mem_info_label.pack(pady=5)
    
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
        pass
    
    def update_with_snapshot(self, snapshot):
        if not snapshot:
            return
        
        cpu = snapshot.cpu
        memory = snapshot.memory
        
        cpu_usage = cpu.usage_percent
        self.cpu_label.config(text=f"Загрузка: {cpu_usage:.1f}%")
        self.cpu_progress['value'] = cpu_usage
        
        cpu_info = f"{cpu.name} | {cpu.physical_cores} ядер"
        if cpu.frequency_current > 0:
            cpu_info += f" | {cpu.frequency_current:.1f} MHz"
        self.cpu_info_label.config(text=cpu_info)
        
        mem_usage = memory.usage_percent
        mem_text = f"{format_bytes(memory.used)} / {format_bytes(memory.total)} ({mem_usage:.1f}%)"
        self.mem_label.config(text=mem_text)
        self.mem_progress['value'] = mem_usage
        
        mem_info = f"Доступно: {format_bytes(memory.available)} | Свободно: {format_bytes(memory.free)}"
        self.mem_info_label.config(text=mem_info)