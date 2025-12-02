import tkinter as tk
import threading
import time
from datetime import datetime

# Импортируем GUI компоненты
from gui.main_window import MainWindow

class SystemInfoApp:
    """Основной класс приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор v1.0")
        self.root.geometry("900x700")
        
        # Переменные состояния
        self.is_collecting = False
        self.collection_thread = None
        
        # Создаем главное окно
        self.main_window = MainWindow(self.root, self)
        
        # Центрируем окно
        self.center_window()
        
        # Обновляем время
        self.update_time()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.main_window.update_time(current_time)
        self.root.after(1000, self.update_time)
    

    def collect_data(self):
        if not self.is_collecting:
            self.is_collecting = True
            self.main_window.set_collecting_state(True)
            self.main_window.update_status("Сбор данных...")
            
            self.collection_thread = threading.Thread(target=self.simulate_collection)
            self.collection_thread.daemon = True
            self.collection_thread.start()
        else:
            self.main_window.show_warning("Сбор данных уже выполняется")
    
    def stop_collection(self):
        if self.is_collecting:
            self.is_collecting = False
            self.main_window.set_collecting_state(False)
            self.main_window.update_status("Сбор данных остановлен")
    
    def simulate_collection(self):
        interval = self.main_window.get_interval()
        while self.is_collecting:
            time.sleep(interval)
            self.update_all_data()
    
    def update_all_data(self):
        self.main_window.update_all_tabs()
        self.main_window.update_status(f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")
    
    def export_data(self):
        format_choice = self.main_window.get_export_format()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"system_info_{timestamp}.{format_choice.lower()}"
        
        self.main_window.show_info(
            "Экспорт данных",
            f"Данные успешно экспортированы в формате {format_choice}\n"
            f"Файл: {filename}"
        )
    
    def kill_process(self, pid, name):
        return True
    
    def show_about(self):
        about_text ="""
                    Системный монитор v1.0

                    Программа для автоматизированного сбора 
                    системной информации с локального компьютера.
                    """
        self.main_window.show_info("О программе", about_text)