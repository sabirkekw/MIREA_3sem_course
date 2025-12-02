import tkinter as tk
from tkinter import messagebox, ttk

from gui.components.menu import MenuBar
from gui.components.toolbar import Toolbar
from gui.components.statusbar import StatusBar
from gui.components.notebook import MainNotebook

class MainWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=35)
        
        self.menu = MenuBar(root, app)
        self.toolbar = Toolbar(root, app)
        self.notebook = MainNotebook(root, app)
        self.statusbar = StatusBar(root, app)
    
    def update_status(self, text):
        self.statusbar.update_status(text)
    
    def update_time(self, time_str):
        self.statusbar.update_time(time_str)
    
    def set_collecting_state(self, is_collecting):
        self.toolbar.set_collecting_state(is_collecting)
    
    def get_interval(self):
        return self.toolbar.get_interval()
    
    def get_export_format(self):
        return self.toolbar.get_export_format()
    
    def update_all_tabs(self):
        self.notebook.update_all_tabs()
    
    def show_info(self, title, message):
        messagebox.showinfo(title, message)
    
    def show_warning(self, message):
        messagebox.showwarning("Внимание", message)