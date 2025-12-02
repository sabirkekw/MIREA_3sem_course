import tkinter as tk
from tkinter import ttk

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
        
        style = ttk.Style()
        style.configure("Disk.Treeview", rowheight=35)
        
        self.disk_tree = ttk.Treeview(
            tree_frame, 
            columns=columns, 
            show='headings', 
            height=8,
            style="Disk.Treeview"
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
        
        # Заполняем тестовыми данными
        sample_data = [
            ('C:', 'SSD', '476.9 GB', '298.4 GB', '178.5 GB', '62%', 'NTFS'),
            ('D:', 'HDD', '931.5 GB', '412.3 GB', '519.2 GB', '44%', 'NTFS'),
            ('E:', 'HDD', '465.7 GB', '89.2 GB', '376.5 GB', '19%', 'NTFS'),
        ]
        
        for item in sample_data:
            self.disk_tree.insert('', tk.END, values=item)
    
    def create_io_section(self):
        io_frame = ttk.LabelFrame(self.frame, text="Статистика ввода-вывода")
        io_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        
        # Создаем метки для статистики
        self.io_labels = {}
        io_info = [
            ("read", "Прочитано:", "15.2 GB"),
            ("written", "Записано:", "8.7 GB"),
            ("read_speed", "Скорость чтения:", "120 MB/s"),
            ("write_speed", "Скорость записи:", "65 MB/s"),
        ]
        
        for i, (key, label, value) in enumerate(io_info):
            if i % 2 == 0:
                row_frame = ttk.Frame(io_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            self.io_labels[key] = ttk.Label(row_frame, text=value)
            self.io_labels[key].pack(side=tk.LEFT, padx=10)
    
    def update_data(self):
        pass