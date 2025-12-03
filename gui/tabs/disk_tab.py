import tkinter as tk
from tkinter import ttk
from utils.formatters import format_bytes, format_percent

class DiskTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.title = "Диски"
        self.create_tab()
    
    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_disk_table()
        
        self.create_io_section()
    
    def create_disk_table(self):
        columns = ('Диск', 'Тип', 'Всего', 'Использовано', 'Свободно', 'Использование', 'Файловая система')
        
        tree_frame = ttk.Frame(self.frame)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        
        self.disk_tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            height=8,
        )
        
        col_widths = [80, 100, 100, 100, 100, 100, 150]
        for col, width in zip(columns, col_widths):
            self.disk_tree.heading(col, text=col)
            self.disk_tree.column(col, width=width, minwidth=50)
        
        self.disk_tree.column('Файловая система', stretch=tk.YES)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.disk_tree.yview)
        self.disk_tree.configure(yscrollcommand=scrollbar.set)
        
        self.disk_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
    
    def create_io_section(self):
        self.io_frame = ttk.LabelFrame(self.frame, text="Статистика ввода-вывода")
        self.io_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        
        self.io_labels = {}
        io_fields = [
            ("total_space", "Общий объем:"),
            ("used_space", "Использовано:"),
            ("free_space", "Свободно:"),
            ("partitions", "Разделы:"),
        ]
        
        for i, (key, label) in enumerate(io_fields):
            if i % 2 == 0:
                row_frame = ttk.Frame(self.io_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            self.io_labels[key] = ttk.Label(row_frame, text="")
            self.io_labels[key].pack(side=tk.LEFT, padx=10)
    
    def update_data(self):
        pass
    
    def update_with_snapshot(self, snapshot):
        if not snapshot:
            return
        
        for item in self.disk_tree.get_children():
            self.disk_tree.delete(item)
        
        total_space = 0
        used_space = 0
        free_space = 0
        
        for disk in snapshot.disks:
            self.disk_tree.insert('', tk.END, values=(
                disk.device,
                self._get_disk_type(disk.filesystem),
                format_bytes(disk.total),
                format_bytes(disk.used),
                format_bytes(disk.free),
                f"{disk.usage_percent:.1f}%",
                disk.filesystem
            ))
            
            total_space += disk.total
            used_space += disk.used
            free_space += disk.free
        
        self.io_labels['total_space'].config(text=format_bytes(total_space))
        self.io_labels['used_space'].config(text=format_bytes(used_space))
        self.io_labels['free_space'].config(text=format_bytes(free_space))
        self.io_labels['partitions'].config(text=str(len(snapshot.disks)))
    
    def _get_disk_type(self, filesystem):
        fs_lower = filesystem.lower()
        if fs_lower in ['ext4', 'ext3', 'ext2', 'xfs', 'btrfs']:
            return 'Linux'
        elif fs_lower in ['ntfs', 'fat32', 'exfat']:
            return 'Windows'
        elif fs_lower == 'vfat':
            return 'EFI'
        elif fs_lower == 'apfs':
            return 'macOS'
        else:
            return 'Other'