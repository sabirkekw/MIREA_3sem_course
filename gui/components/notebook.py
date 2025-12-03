import tkinter as tk
from tkinter import ttk

from gui.tabs.system_tab import SystemTab
from gui.tabs.hardware_tab import HardwareTab
from gui.tabs.disk_tab import DiskTab
from gui.tabs.network_tab import NetworkTab
from gui.tabs.processes_tab import ProcessesTab

class MainNotebook:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.create_notebook()
    
    def create_notebook(self):
        notebook_frame = ttk.Frame(self.root)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tabs = {
            'system': SystemTab(self.notebook, self.app),
            'hardware': HardwareTab(self.notebook, self.app),
            'disk': DiskTab(self.notebook, self.app),
            'network': NetworkTab(self.notebook, self.app),
            'processes': ProcessesTab(self.notebook, self.app)
        }
        
        for name, tab in self.tabs.items():
            self.notebook.add(tab.frame, text=tab.title)
    
    def update_all_tabs(self, snapshot):
        for tab in self.tabs.values():
            if hasattr(tab, 'update_with_snapshot'):
                tab.update_with_snapshot(snapshot)