import tkinter as tk
from collections import deque

class SimpleChart:
    def __init__(self, canvas, width=400, height=200, max_points=50):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.max_points = max_points
        
        self.cpu_data = deque(maxlen=max_points)
        self.memory_data = deque(maxlen=max_points)
        
        self.bg_color = '#f0f0f0'
        self.cpu_color = '#ff6b6b'
        self.memory_color = '#4ecdc4'
        self.grid_color = '#cccccc'
        self.text_color = '#333333'
        
        self._setup_canvas()
    
    def _setup_canvas(self):
        self.canvas.config(
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0
        )
        
        self._draw_grid()
        
        self._draw_legend()
    
    def _draw_grid(self):
        for i in range(0, 11):
            x = i * (self.width // 10)
            self.canvas.create_line(x, 0, x, self.height, fill=self.grid_color, width=1)
        
        for i in range(0, 11):
            y = i * (self.height // 10)
            self.canvas.create_line(0, y, self.width, y, fill=self.grid_color, width=1)
            
            percent = 100 - (i * 10)
            self.canvas.create_text(
                5, y - 10,
                text=f"{percent}%",
                fill=self.text_color,
                font=("Arial", 8),
                anchor="w"
            )
    
    def _draw_legend(self):
        self.canvas.create_rectangle(
            10, self.height - 30,
            25, self.height - 15,
            fill=self.cpu_color,
            outline=self.cpu_color
        )
        self.canvas.create_text(
            30, self.height - 22,
            text="CPU",
            fill=self.text_color,
            font=("Arial", 9),
            anchor="n"
        )
        
        self.canvas.create_rectangle(
            80, self.height - 30,
            95, self.height - 15,
            fill=self.memory_color,
            outline=self.memory_color
        )
        self.canvas.create_text(
            100, self.height - 22,
            text="Memory",
            fill=self.text_color,
            font=("Arial", 9),
            anchor="n"
        )
    
    def add_data_point(self, cpu_percent, memory_percent):
        self.cpu_data.append(cpu_percent)
        self.memory_data.append(memory_percent)
        self._redraw()
    
    def _redraw(self):
        self.canvas.delete("chart_line")
        
        if len(self.cpu_data) < 2:
            return
        
        cpu_points = []
        for i, value in enumerate(self.cpu_data):
            x = i * (self.width / (self.max_points - 1))
            y = self.height - (value * self.height / 100)
            cpu_points.extend([x, y])
        
        if len(cpu_points) >= 4:
            self.canvas.create_line(
                *cpu_points,
                fill=self.cpu_color,
                width=2,
                smooth=True,
                tags="chart_line"
            )
        
        memory_points = []
        for i, value in enumerate(self.memory_data):
            x = i * (self.width / (self.max_points - 1))
            y = self.height - (value * self.height / 100)
            memory_points.extend([x, y])
        
        if len(memory_points) >= 4:
            self.canvas.create_line(
                *memory_points,
                fill=self.memory_color,
                width=2,
                smooth=True,
                tags="chart_line"
            )
    
    def clear(self):
        self.cpu_data.clear()
        self.memory_data.clear()
        self.canvas.delete("chart_line")