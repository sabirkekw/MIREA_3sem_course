import tkinter as tk
from tkinter import ttk, scrolledtext

class ProcessesTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.title = "Процессы"
        self.create_tab()
    
    def create_tab(self):
        self.frame = ttk.Frame(self.parent)
        
        self.create_control_panel()
        
        self.create_processes_table()
        
        self.create_control_buttons()
    
    def create_control_panel(self):
        control_frame = ttk.Frame(self.frame)
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
        
        ttk.Button(control_frame, text="Обновить", command=self.update_data).pack(side=tk.RIGHT, padx=5)
    
    def create_processes_table(self):
        columns = ('PID', 'Имя', 'Пользователь', 'CPU %', 'Память %', 'Память (MB)', 'Состояние')
        
        tree_frame = ttk.Frame(self.frame)
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
        
        self.process_tree.bind('<Double-1>', self.on_process_double_click)
    
    def create_control_buttons(self):
        btn_frame = ttk.Frame(self.frame)
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
    
    def update_data(self):
        self.app.update_all_data()
    
    def update_with_snapshot(self, snapshot):
        if not snapshot:
            return
        
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        try:
            max_processes = int(self.process_count.get())
        except:
            max_processes = 20

        processes = snapshot.processes
        
        processes.sort(key=lambda x: x.cpu_percent, reverse=True)
        
        for i, process in enumerate(processes[:max_processes]):
            memory_mb = process.memory_rss / (1024 * 1024)
            self.process_tree.insert('', tk.END, values=(
                process.pid,
                process.name[:30],
                process.username,
                f"{process.cpu_percent:.1f}",
                f"{process.memory_percent:.1f}",
                f"{memory_mb:.1f}",
                process.status
            ))
    
    def sort_processes(self, column):
        pass
    
    def on_process_double_click(self, event):
        self.show_process_details()
    
    def kill_process(self):
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            values = item['values']
            pid = values[0]
            name = values[1]
            
            if self.app.kill_process(pid, name):
                self.process_tree.delete(selection[0])
                self.app.main_window.update_status(f"Процесс {name} ({pid}) завершен")
        else:
            self.app.main_window.show_warning("Выберите процесс для завершения")
    
    def show_process_details(self):
        selection = self.process_tree.selection()
        if selection:
            item = self.process_tree.item(selection[0])
            values = item['values']
            
            detail_window = tk.Toplevel(self.app.root)
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
            self.app.main_window.show_warning("Выберите процесс для просмотра деталей")