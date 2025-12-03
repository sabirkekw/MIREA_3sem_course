import tkinter as tk
from tkinter import ttk
from utils.formatters import format_bytes

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
        self.info_frame = ttk.LabelFrame(self.frame, text="Сетевая информация")
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.network_labels = {}
        network_fields = [
            ("hostname", "Имя хоста:"),
            ("ip", "Основной IP:"),
            ("external_ip", "Внешний IP:"),
            ("fqdn", "Полное имя домена:"),
        ]
        
        for key, label in network_fields:
            row = ttk.Frame(self.info_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            self.network_labels[key] = ttk.Label(row, text="", anchor="w")
            self.network_labels[key].pack(side=tk.LEFT)
    
    def create_interfaces_table(self):
        iface_frame = ttk.LabelFrame(self.frame, text="Сетевые интерфейсы")
        iface_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ('Интерфейс', 'Тип', 'IP адрес', 'MAC адрес', 'Состояние')
        
        tree_frame = ttk.Frame(iface_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.network_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=4)
        
        col_widths = [120, 80, 120, 120, 80]
        for col, width in zip(columns, col_widths):
            self.network_tree.heading(col, text=col)
            self.network_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=scrollbar.set)
        
        self.network_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_network_stats(self):
        self.stats_frame = ttk.LabelFrame(self.frame, text="Сетевая статистика")
        self.stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_labels = {}
        stats_fields = [
            ("sent", "Отправлено:"),
            ("received", "Получено:"),
            ("packets_sent", "Пакетов отправлено:"),
            ("packets_recv", "Пакетов получено:"),
        ]
        
        for i, (key, label) in enumerate(stats_fields):
            if i % 2 == 0:
                row_frame = ttk.Frame(self.stats_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            self.stats_labels[key] = ttk.Label(row_frame, text="")
            self.stats_labels[key].pack(side=tk.LEFT, padx=10)
    
    def update_data(self):
        pass
    
    def update_with_snapshot(self, snapshot):
        if not snapshot:
            return
        
        system = snapshot.system
        self.network_labels['hostname'].config(text=system.hostname)
        self.network_labels['fqdn'].config(text=system.hostname)
        
        main_ip = ""
        for interface in snapshot.network_interfaces:
            if interface.ip_address and interface.ip_address not in ['127.0.0.1', '127.0.1.1']:
                main_ip = interface.ip_address
                break
        
        self.network_labels['ip'].config(text=main_ip)
        self.network_labels['external_ip'].config(text="(требуется интернет)")
        
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        for interface in snapshot.network_interfaces:
            iface_type = self._get_interface_type(interface.name)
            self.network_tree.insert('', tk.END, values=(
                interface.name,
                iface_type,
                interface.ip_address if interface.ip_address else "N/A",
                interface.mac_address if interface.mac_address else "N/A",
                interface.status
            ))
        
        self.stats_labels['sent'].config(text="N/A")
        self.stats_labels['received'].config(text="N/A")
        self.stats_labels['packets_sent'].config(text="N/A")
        self.stats_labels['packets_recv'].config(text="N/A")
    
    def _get_interface_type(self, name):
        name_lower = name.lower()
        if 'eth' in name_lower or 'enp' in name_lower or 'eno' in name_lower:
            return 'Ethernet'
        elif 'wlan' in name_lower or 'wlp' in name_lower or 'wifi' in name_lower:
            return 'Wi-Fi'
        elif 'lo' == name_lower:
            return 'Loopback'
        elif 'docker' in name_lower:
            return 'Docker'
        elif 'br-' in name_lower:
            return 'Bridge'
        elif 'veth' in name_lower:
            return 'Virtual'
        else:
            return 'Unknown'