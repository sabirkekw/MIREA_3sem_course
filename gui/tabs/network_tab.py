import tkinter as tk
from tkinter import ttk

class NetworkTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.title = "Сеть"
        self.create_tab()
    
    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        
        self.create_network_info()
        
        self.create_interfaces_table()
        
        self.create_network_stats()
    
    def create_network_info(self):
        info_frame = ttk.LabelFrame(self.frame, text="Сетевая информация")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.network_labels = {}
        network_info = [
            ("ip", "IP адрес:", "192.168.1.100"),
            ("mask", "Маска подсети:", "255.255.255.0"),
            ("gateway", "Шлюз по умолчанию:", "192.168.1.1"),
            ("dns", "DNS сервер:", "8.8.8.8"),
            ("external_ip", "Внешний IP:", "89.108.76.54"),
            ("hostname", "Имя хоста:", "DESKTOP-ABC123"),
        ]
        
        for key, label, value in network_info:
            row = ttk.Frame(info_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.network_labels[key] = ttk.Label(row, text=value, anchor="w")
            self.network_labels[key].pack(side=tk.LEFT)
    
    def create_interfaces_table(self):
        iface_frame = ttk.LabelFrame(self.frame, text="Сетевые интерфейсы")
        iface_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Интерфейс', 'Состояние', 'IP адрес', 'MAC адрес', 'Скорость')
        
        tree_frame = ttk.Frame(iface_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.network_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=4)
        
        for col in columns:
            self.network_tree.heading(col, text=col)
            self.network_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=scrollbar.set)
        
        self.network_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        sample_ifaces = [
            ('Ethernet', 'Подключен', '192.168.1.100', '00-1A-2B-3C-4D-5E', '1 Gbps'),
            ('Wi-Fi', 'Подключен', '192.168.1.101', '00-1A-2B-3C-4D-5F', '300 Mbps'),
            ('Bluetooth', 'Отключен', 'Нет', '00-1A-2B-3C-4D-60', 'N/A'),
        ]
        
        for item in sample_ifaces:
            self.network_tree.insert('', tk.END, values=item)
    
    def create_network_stats(self):
        stats_frame = ttk.LabelFrame(self.frame, text="Сетевая статистика")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats_info = [
            ("sent", "Отправлено:", "2.4 GB"),
            ("received", "Получено:", "5.7 GB"),
            ("send_speed", "Текущая отправка:", "1.2 MB/s"),
            ("receive_speed", "Текущее получение:", "0.8 MB/s"),
        ]
        
        for i, (key, label, value) in enumerate(stats_info):
            if i % 2 == 0:
                row_frame = ttk.Frame(stats_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            self.stats_labels[key] = ttk.Label(row_frame, text=value)
            self.stats_labels[key].pack(side=tk.LEFT, padx=10)
    
    def update_data(self):
        pass