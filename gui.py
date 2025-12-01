# gui_app.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime

class SystemInfoGUI:
    """Основной класс GUI приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор v1.0")
        self.root.geometry("900x700")
        
        # collection state variables
        self.is_collecting = False
        self.collection_thread = None
        
        # ui
        self.setup_ui()
        
        self.center_window()
        
    def center_window(self):
        """Центрировать окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # menu
        self.create_menu()
        
        # toolbar
        self.create_toolbar()
        
        # mainspace
        self.create_notebook()
        
        # statusbar
        self.create_statusbar()
    
    def create_menu(self):
        """Создать меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # menu "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Собрать данные", command=self.collect_data)
        file_menu.add_command(label="Экспорт...", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # menu "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить", command=self.update_data)
        view_menu.add_checkbutton(label="Автообновление", command=self.toggle_auto_update)
        
        # menu "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_toolbar(self):
        """Создать панель инструментов"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        self.collect_btn = ttk.Button(
            toolbar, 
            text="▶ Собрать данные", 
            command=self.collect_data,
            width=15
        )
        self.collect_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = ttk.Button(
            toolbar, 
            text="⏹ Остановить", 
            command=self.stop_collection,
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5)
        
        # choosing export format
        ttk.Label(toolbar, text="Экспорт:").pack(side=tk.LEFT, padx=2)
        self.export_format = tk.StringVar(value="JSON")
        format_combo = ttk.Combobox(
            toolbar, 
            textvariable=self.export_format,
            values=["JSON", "CSV", "SQLite"],
            state="readonly",
            width=10
        )
        format_combo.pack(side=tk.LEFT, padx=2)
        
        self.export_btn = ttk.Button(
            toolbar, 
            text="📁 Экспорт", 
            command=self.export_data,
            width=10
        )
        self.export_btn.pack(side=tk.LEFT, padx=2)
        
        # update interval
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5)
        ttk.Label(toolbar, text="Интервал (сек):").pack(side=tk.LEFT, padx=2)
        self.interval_var = tk.StringVar(value="5")
        interval_spin = ttk.Spinbox(
            toolbar,
            from_=1,
            to=60,
            textvariable=self.interval_var,
            width=5
        )
        interval_spin.pack(side=tk.LEFT, padx=2)
    
    def create_notebook(self):
        """Создать блокнот с вкладками"""
        notebook_frame = ttk.Frame(self.root)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_system_tab()
        self.create_hardware_tab()
        self.create_disk_tab()
        self.create_network_tab()
        self.create_processes_tab()
    
    def create_system_tab(self):
        """Вкладка общей информации о системе"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Общая информация")
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(top_frame, text="Обновить", command=self.update_system_info).pack(side=tk.RIGHT)
        
        main_frame = ttk.Frame(frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_frame = ttk.LabelFrame(main_frame, text="Система")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        system_info = [
            ("Операционная система:", "Windows 10 Pro"),
            ("Версия ОС:", "10.0.19045"),
            ("Архитектура:", "64-bit"),
            ("Имя компьютера:", "DESKTOP-ABC123"),
            ("Имя пользователя:", "Admin"),
            ("Время запуска:", "2024-01-15 08:30:15"),
        ]
        
        for label, value in system_info:
            row = ttk.Frame(left_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            ttk.Label(row, text=value, anchor="w").pack(side=tk.LEFT)
        
        right_frame = ttk.LabelFrame(main_frame, text="Аппаратное обеспечение")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        hardware_info = [
            ("Процессор:", "Intel Core i7-9700"),
            ("Количество ядер:", "8 (4 физических)"),
            ("Частота:", "3.0 GHz"),
            ("Объем ОЗУ:", "16.0 GB"),
            ("Видеокарта:", "NVIDIA GeForce RTX 3060"),
            ("Объем VRAM:", "12.0 GB"),
        ]
        
        for label, value in hardware_info:
            row = ttk.Frame(right_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            ttk.Label(row, text=value, anchor="w").pack(side=tk.LEFT)
    
    def create_hardware_tab(self):
        """Вкладка мониторинга процессора и памяти"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Процессор и память")
        
        metrics_frame = ttk.Frame(frame)
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        cpu_frame = ttk.LabelFrame(metrics_frame, text="Процессор")
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.cpu_label = ttk.Label(cpu_frame, text="Загрузка: 45%", font=("Arial", 14))
        self.cpu_label.pack(pady=20)
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(pady=10)
        self.cpu_progress['value'] = 45
        
        mem_frame = ttk.LabelFrame(metrics_frame, text="Оперативная память")
        mem_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.mem_label = ttk.Label(mem_frame, text="8.2 / 16.0 GB (51%)", font=("Arial", 14))
        self.mem_label.pack(pady=20)
        
        self.mem_progress = ttk.Progressbar(mem_frame, length=200, mode='determinate')
        self.mem_progress.pack(pady=10)
        self.mem_progress['value'] = 51
        
        graph_frame = ttk.LabelFrame(frame, text="История использования")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        graph_placeholder = tk.Canvas(graph_frame, bg='#f0f0f0', height=200)
        graph_placeholder.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        graph_placeholder.create_text(
            150, 100,
            text="График загрузки CPU и памяти\n(будет реализован в следующей версии)",
            font=("Arial", 10),
            fill="gray"
        )
    
    def create_disk_tab(self):
        """Вкладка информации о дисках"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Диски")
        
        columns = ('Диск', 'Тип', 'Всего', 'Использовано', 'Свободно', 'Использование', 'Файловая система')
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.disk_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        col_widths = [50, 80, 80, 80, 80, 100, 120]
        for col, width in zip(columns, col_widths):
            self.disk_tree.heading(col, text=col)
            self.disk_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.disk_tree.yview)
        self.disk_tree.configure(yscrollcommand=scrollbar.set)
        
        self.disk_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        sample_data = [
            ('C:', 'SSD', '476.9 GB', '298.4 GB', '178.5 GB', '62%', 'NTFS'),
            ('D:', 'HDD', '931.5 GB', '412.3 GB', '519.2 GB', '44%', 'NTFS'),
            ('E:', 'HDD', '465.7 GB', '89.2 GB', '376.5 GB', '19%', 'NTFS'),
        ]
        
        for item in sample_data:
            self.disk_tree.insert('', tk.END, values=item)
        
        io_frame = ttk.LabelFrame(frame, text="Статистика ввода-вывода")
        io_frame.pack(fill=tk.X, padx=10, pady=10)
        
        io_info = [
            ("Прочитано:", "15.2 GB"),
            ("Записано:", "8.7 GB"),
            ("Скорость чтения:", "120 MB/s"),
            ("Скорость записи:", "65 MB/s"),
        ]
        
        for i, (label, value) in enumerate(io_info):
            if i % 2 == 0:
                row_frame = ttk.Frame(io_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            ttk.Label(row_frame, text=value).pack(side=tk.LEFT, padx=10)
    
    def create_network_tab(self):
        """Вкладка сетевой информации"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Сеть")
        
        info_frame = ttk.LabelFrame(frame, text="Сетевая информация")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        network_info = [
            ("IP адрес:", "192.168.1.100"),
            ("Маска подсети:", "255.255.255.0"),
            ("Шлюз по умолчанию:", "192.168.1.1"),
            ("DNS сервер:", "8.8.8.8"),
            ("Внешний IP:", "89.108.76.54"),
            ("Имя хоста:", "DESKTOP-ABC123"),
        ]
        
        for label, value in network_info:
            row = ttk.Frame(info_frame)
            row.pack(fill=tk.X, padx=10, pady=5)
            ttk.Label(row, text=label, width=25, anchor="w").pack(side=tk.LEFT)
            ttk.Label(row, text=value, anchor="w").pack(side=tk.LEFT)
        
        iface_frame = ttk.LabelFrame(frame, text="Сетевые интерфейсы")
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
        
        stats_frame = ttk.LabelFrame(frame, text="Сетевая статистика")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats_info = [
            ("Отправлено:", "2.4 GB"),
            ("Получено:", "5.7 GB"),
            ("Текущая отправка:", "1.2 MB/s"),
            ("Текущее получение:", "0.8 MB/s"),
        ]
        
        for i, (label, value) in enumerate(stats_info):
            if i % 2 == 0:
                row_frame = ttk.Frame(stats_frame)
                row_frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(row_frame, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            ttk.Label(row_frame, text=value).pack(side=tk.LEFT, padx=10)
    
    def create_processes_tab(self):
        """Вкладка с информацией о процессах"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Процессы")
        
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Показать процессов:").pack(side=tk.LEFT, padx=5)
        self.process_count = tk.StringVar(value="20")
        ttk.Spinbox(
            control_frame,
            from_=10,
            to=100,
            textvariable=self.process_count,
            width=5
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Обновить", command=self.update_processes).pack(side=tk.RIGHT, padx=5)
        
        columns = ('PID', 'Имя', 'Пользователь', 'CPU %', 'Память %', 'Память (MB)', 'Состояние')
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.process_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        col_widths = [50, 150, 100, 60, 80, 100, 100]
        for col, width in zip(columns, col_widths):
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=width)
        
        for col in columns:
            self.process_tree.heading(
                col, 
                text=col,
                command=lambda c=col: self.sort_processes(c)
            )
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        sample_processes = [
            (1245, 'chrome.exe', 'user', 45.2, 25.3, 1250, 'Выполняется'),
            (892, 'python.exe', 'user', 32.1, 12.4, 612, 'Выполняется'),
            (1567, 'Code.exe', 'user', 15.7, 18.9, 932, 'Выполняется'),
            (223, 'svchost.exe', 'SYSTEM', 5.2, 3.1, 152, 'Выполняется'),
            (478, 'explorer.exe', 'user', 3.8, 8.4, 415, 'Выполняется'),
            (912, 'Discord.exe', 'user', 12.6, 15.2, 750, 'Выполняется'),
            (335, 'steam.exe', 'user', 8.9, 22.1, 1090, 'Выполняется'),
            (667, 'Spotify.exe', 'user', 6.3, 9.8, 482, 'Выполняется'),
        ]
        
        for proc in sample_processes:
            self.process_tree.insert('', tk.END, values=proc)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Завершить процесс", 
            command=self.kill_process,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Подробнее", 
            command=self.show_process_details,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def create_statusbar(self):
        """Создать строку состояния"""
        self.statusbar = ttk.Frame(self.root)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.statusbar, text="Готов к работе", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.time_label = ttk.Label(self.statusbar, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), relief=tk.SUNKEN, anchor=tk.E)
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
        self.update_time()
    
    def update_time(self):
        """Обновить время в статусбаре"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    # stub
    def collect_data(self):
        """Собрать данные"""
        if not self.is_collecting:
            self.is_collecting = True
            self.collect_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Сбор данных...")
            
            # Имитация сбора данных в отдельном потоке
            self.collection_thread = threading.Thread(target=self.simulate_collection)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            
            messagebox.showinfo("Информация", "Начат сбор системной информации")
        else:
            messagebox.showwarning("Внимание", "Сбор данных уже выполняется")
    
    def stop_collection(self):
        """Остановить сбор данных"""
        if self.is_collecting:
            self.is_collecting = False
            self.collect_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Сбор данных остановлен")
            messagebox.showinfo("Информация", "Сбор данных остановлен")
    
    def simulate_collection(self):
        """Имитация сбора данных"""
        interval = int(self.interval_var.get())
        while self.is_collecting:
            time.sleep(interval)
            # Здесь будет реальный сбор данных
            self.update_data()
    
    def update_data(self):
        """Обновить все данные"""
        self.update_system_info()
        self.update_hardware_info()
        self.update_disk_info()
        self.update_network_info()
        self.update_processes()
        self.status_label.config(text=f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_system_info(self):
        """Обновить системную информацию"""
        # stub - в реальности будет собирать данные
        pass
    
    def update_hardware_info(self):
        """Обновить информацию о железе"""
        # Имитируем изменение значений
        import random
        cpu_usage = random.randint(10, 90)
        mem_usage = random.randint(20, 80)
        
        self.cpu_label.config(text=f"Загрузка: {cpu_usage}%")
        self.cpu_progress['value'] = cpu_usage
        
        self.mem_label.config(text=f"{random.randint(4, 12)}.{random.randint(0, 9)} / 16.0 GB ({mem_usage}%)")
        self.mem_progress['value'] = mem_usage
    
    def update_disk_info(self):
        """Обновить информацию о дисках"""
        # stub
        pass
    
    def update_network_info(self):
        """Обновить сетевую информацию"""
        # stub
        pass
    
    def update_processes(self):
        """Обновить список процессов"""
        # stub
        self.status_label.config(text="Список процессов обновлен")
    
    def sort_processes(self, column):
        """Сортировать процессы по столбцу"""
        # stub
        pass
    
    def export_data(self):
        """Экспортировать данные"""
        format_choice = self.export_format.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_info_{timestamp}.{format_choice.lower()}"
        
        # stub
        messagebox.showinfo(
            "Экспорт данных",
            f"Данные успешно экспортированы в формате {format_choice}\n"
            f"Файл: {filename}"
        )
    
    def toggle_auto_update(self):
        """Включить/выключить автообновление"""
        # stub
        pass
    
    def kill_process(self):
        """Завершить процесс"""
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            pid = item['values'][0]
            name = item['values'][1]
            
            response = messagebox.askyesno(
                "Завершение процесса",
                f"Вы уверены, что хотите завершить процесс?\n"
                f"PID: {pid}\n"
                f"Имя: {name}"
            )
            
            if response:
                # stub
                self.process_tree.delete(selection[0])
                messagebox.showinfo("Информация", f"Процесс {name} ({pid}) завершен")
        else:
            messagebox.showwarning("Внимание", "Выберите процесс для завершения")
    
    def show_process_details(self):
        """Показать подробную информацию о процессе"""
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            values = item['values']
            
            detail_window = tk.Toplevel(self.root)
            detail_window.title(f"Детали процесса: {values[1]}")
            detail_window.geometry("400x300")
            
            info_text = f"""
                        PID: {values[0]}
                        Имя: {values[1]}
                        Пользователь: {values[2]}
                        Использование CPU: {values[3]}%
                        Использование памяти: {values[4]}%
                        Память: {values[5]} MB
                        Состояние: {values[6]}
                        """
            
            text_widget = scrolledtext.ScrolledText(detail_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.INSERT, info_text)
            text_widget.config(state=tk.DISABLED)
            
            ttk.Button(detail_window, text="Закрыть", command=detail_window.destroy).pack(pady=10)
        else:
            messagebox.showwarning("Внимание", "Выберите процесс для просмотра деталей")
    
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
                    Системный монитор v1.0

                    Программа для автоматизированного сбора 
                    системной информации с локального компьютера.

                    Функции:
                        • Сбор общей информации о системе
                        • Мониторинг процессора и памяти
                        • Анализ дискового пространства
                        • Сетевая информация
                        • Управление процессами
                        • Экспорт данных в различные форматы

                    """
        messagebox.showinfo("О программе", about_text)


def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = SystemInfoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()