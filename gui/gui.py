"""
Основной класс приложения SystemInfoApp.
Теперь с интеграцией backend.
"""

import tkinter as tk
import threading
import time
from datetime import datetime

from gui.main_window import MainWindow
from core.collector import DataCollectorManager
from utils.formatters import format_bytes, format_percent
from exporters.manager import ExportManager

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор v1.0")
        self.root.geometry("900x700")
        
        self.data_manager = DataCollectorManager()
        
        self.is_collecting = False
        self.collection_thread = None
        self.current_snapshot = None

        self.export_manager = ExportManager()
        
        self.main_window = MainWindow(self.root, self)
        
        self.center_window()
        
        self.update_time()
        
        self.load_initial_data()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_initial_data(self):
        try:
            snapshot = self.data_manager.collect_all()
            self.current_snapshot = snapshot
            self.main_window.update_all_tabs(snapshot)
            self.main_window.update_status("Данные загружены")
        except Exception as e:
            self.main_window.update_status(f"Ошибка загрузки: {str(e)}")
    
    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.main_window.update_time(current_time)
        self.root.after(1000, self.update_time)
    
    def collect_data(self):
        if not self.is_collecting:
            self.is_collecting = True
            self.main_window.set_collecting_state(True)
            self.main_window.update_status("Сбор данных...")
            
            interval = self.main_window.get_interval()
            success = self.data_manager.start_collection(
                interval=interval,
                callback=self.on_data_collected
            )
            
            if not success:
                self.is_collecting = False
                self.main_window.set_collecting_state(False)
                self.main_window.update_status("Ошибка запуска сбора")
        else:
            self.main_window.show_warning("Сбор данных уже выполняется")
    
    def stop_collection(self):
        if self.is_collecting:
            self.is_collecting = False
            self.data_manager.stop_collection()
            self.main_window.set_collecting_state(False)
            self.main_window.update_status("Сбор данных остановлен")
    
    def on_data_collected(self, snapshot):
        self.current_snapshot = snapshot
        self.main_window.update_all_tabs(snapshot)
        self.main_window.update_status(f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_all_data(self):
        try:
            snapshot = self.data_manager.collect_all()
            self.current_snapshot = snapshot
            self.main_window.update_all_tabs(snapshot)
            self.main_window.update_status(f"Данные обновлены: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            self.main_window.update_status(f"Ошибка обновления: {str(e)}")
    
    def export_data(self):
        if not self.current_snapshot:
            self.main_window.show_warning("Нет данных для экспорта")
            return
        
        format_choice = self.main_window.get_export_format()
        
        result = self.export_manager.export(
            snapshot=self.current_snapshot,
            format_type=format_choice
        )
        
        if result['success']:
            self.main_window.show_info(
                "Экспорт данных",
                f"Данные успешно экспортированы в формате {format_choice}\n"
                f"Файл: {result.get('filename', result.get('filepath', 'N/A'))}"
            )
            self.main_window.update_status(f"Данные экспортированы в {format_choice}")
        else:
            self.main_window.show_warning(
                f"Ошибка экспорта в {format_choice}:\n{result.get('error', 'Неизвестная ошибка')}"
            )
    
    def kill_process(self, pid, name):
        import psutil
        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except Exception as e:
            self.main_window.show_warning(f"Не удалось завершить процесс {name} ({pid}): {str(e)}")
            return False
    
    def show_about(self):
        about_text = """Системный монитор v1.0
        Программа для автоматизированного сбора системной информации с локального компьютера.

        Функции:
        • Сбор общей информации о системе
        • Мониторинг процессора и памяти
        • Анализ дискового пространства
        • Сетевая информация
        • Управление процессами
        • Экспорт данных (в разработке)

        Разработано в рамках курсовой работы.
        """
        self.main_window.show_info("О программе", about_text)
    
    def get_current_snapshot(self):
        return self.current_snapshot