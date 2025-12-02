import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.collector import DataCollectorManager

def format_bytes(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"

def test_backend():
    print("=== Тестирование SystemInfoMonitor Backend ===")
    print()
    
    manager = DataCollectorManager()
    
    print("1. Проверка статуса сборщиков:")
    status = manager.get_collector_status()
    for name, is_active in status.items():
        print(f"   - {name}: {'Активен' if is_active else 'Не активен'}")
    
    print()
    print("2. Однократный сбор данных:")
    snapshot = manager.collect_all()
    print(f"   Время снимка: {snapshot.timestamp}")
    print(f"   ОС: {snapshot.system.os_name} {snapshot.system.os_version}")
    print(f"   Архитектура: {snapshot.system.architecture}")
    print(f"   Хост: {snapshot.system.hostname}")
    print(f"   Пользователь: {snapshot.system.username}")
    
    print()
    print("3. Аппаратная информация:")
    print(f"   Процессор: {snapshot.cpu.name}")
    print(f"   Ядра: {snapshot.cpu.physical_cores} физических, {snapshot.cpu.logical_cores} логических")
    print(f"   Загрузка CPU: {snapshot.cpu.usage_percent:.1f}%")
    print(f"   Память: {format_bytes(snapshot.memory.used)} / {format_bytes(snapshot.memory.total)} ({snapshot.memory.usage_percent:.1f}%)")
    
    print()
    print("4. Диски:")
    for i, disk in enumerate(snapshot.disks[:3]):
        print(f"   {disk.device}: {format_bytes(disk.used)} / {format_bytes(disk.total)} ({disk.usage_percent:.1f}%)")
    if len(snapshot.disks) > 3:
        print(f"   ... и еще {len(snapshot.disks) - 3} дисков")
    
    print()
    print("5. Сеть:")
    for i, interface in enumerate(snapshot.network_interfaces[:2]):
        if interface.ip_address:
            print(f"   {interface.name}: {interface.ip_address} ({interface.status})")
    if len(snapshot.network_interfaces) > 2:
        print(f"   ... и еще {len(snapshot.network_interfaces) - 2} интерфейсов")
    
    print()
    print("6. Процессы (топ-5 по CPU):")
    for i, process in enumerate(snapshot.processes[:5]):
        print(f"   {process.pid}: {process.name} - CPU: {process.cpu_percent:.1f}%, MEM: {process.memory_percent:.1f}%")
    
    print()
    print("7. Конвертация в словарь:")
    data_dict = snapshot.to_dict()
    print(f"   Количество дисков: {len(data_dict['disks'])}")
    print(f"   Количество процессов: {len(data_dict['processes'])}")
    print(f"   Количество интерфейсов: {len(data_dict['network_interfaces'])}")
    
    print()
    print("=== Тест завершен успешно ===")
    return snapshot

if __name__ == "__main__":
    try:
        snapshot = test_backend()
        
        print()
        print("Дополнительно: Сохранение в JSON...")
        import json
        data_dict = snapshot.to_dict()
        with open('test_output.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
        print("Данные сохранены в test_output.json")
        
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()