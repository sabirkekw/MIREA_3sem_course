#!/usr/bin/env python3
"""
Тест интеграции GUI с Backend.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.gui import SystemInfoApp

def test_integration():
    """Тестирование интеграции"""
    print("=== Тест интеграции GUI с Backend ===")
    
    # Создаем корневое окно
    root = tk.Tk()
    root.withdraw()  # Скрываем окно
    
    # Создаем приложение
    app = SystemInfoApp(root)
    
    print("\n1. Проверка инициализации:")
    print(f"   DataCollectorManager создан: {app.data_manager is not None}")
    print(f"   Главное окно создано: {app.main_window is not None}")
    
    print("\n2. Проверка сбора данных:")
    snapshot = app.data_manager.collect_all()
    print(f"   Снимок создан: {snapshot is not None}")
    print(f"   Время снимка: {snapshot.timestamp}")
    print(f"   ОС: {snapshot.system.os_name}")
    print(f"   CPU: {snapshot.cpu.name}")
    print(f"   Память: {snapshot.memory.total} bytes")
    print(f"   Диски: {len(snapshot.disks)} шт")
    print(f"   Интерфейсы: {len(snapshot.network_interfaces)} шт")
    print(f"   Процессы: {len(snapshot.processes)} шт")
    
    print("\n3. Проверка обновления GUI:")
    # Обновляем GUI данными
    app.main_window.update_all_tabs(snapshot)
    print("   GUI обновлен с данными")
    
    print("\n4. Проверка методов приложения:")
    print(f"   Метод collect_data: {hasattr(app, 'collect_data')}")
    print(f"   Метод stop_collection: {hasattr(app, 'stop_collection')}")
    print(f"   Метод export_data: {hasattr(app, 'export_data')}")
    print(f"   Метод kill_process: {hasattr(app, 'kill_process')}")
    
    print("\n=== Тест завершен успешно ===")
    
    # Закрываем корневое окно
    root.destroy()
    
    return True

if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()