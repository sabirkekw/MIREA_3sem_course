# test_backend.py
#!/usr/bin/env python3
"""
Тестовый скрипт для проверки backend.
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.collector import DataCollectorManager

def test_backend():
    """Тестирование backend"""
    print("=== Тестирование SystemInfoMonitor Backend ===")
    print()
    
    # Создаем менеджер
    manager = DataCollectorManager()
    
    print("1. Проверка статуса сборщиков:")
    status = manager.get_collector_status()
    for name, is_active in status.items():
        print(f"   - {name}: {'Активен' if is_active else 'Не активен'}")
    
    print()
    print("2. Однократный сбор данных:")
    snapshot = manager.collect_all()
    print(f"   Время снимка: {snapshot.timestamp}")
    print(f"   Имя ОС: {snapshot.system.os_name}")
    print(f"   Хост: {snapshot.system.hostname}")
    print(f"   Пользователь: {snapshot.system.username}")
    
    print()
    print("3. Конвертация в словарь:")
    data_dict = snapshot.to_dict()
    print(f"   Количество дисков: {len(data_dict['disks'])}")
    print(f"   Количество процессов: {len(data_dict['processes'])}")
    print(f"   Количество интерфейсов: {len(data_dict['network_interfaces'])}")
    
    print()
    print("=== Тест завершен успешно ===")

if __name__ == "__main__":
    try:
        test_backend()
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()