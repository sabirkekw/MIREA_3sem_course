import tkinter as tk
from tkinter import ttk

class StatusBar:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_statusbar()
    
    def create_statusbar(self):
        self.statusbar = ttk.Frame(self.root)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.statusbar, text="Готов к работе", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(self.statusbar, text="", 
                                   relief=tk.SUNKEN, anchor=tk.E)
        self.time_label.pack(side=tk.RIGHT, padx=5)
    
    def update_status(self, text):
        self.status_label.config(text=text)
    
    def update_time(self, time_str):
        self.time_label.config(text=time_str)