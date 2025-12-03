import csv
import os
from datetime import datetime
from core.config import Config

class CSVExporter:
    @staticmethod
    def export(snapshot, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_info_{timestamp}.csv"
        
        data_dir = Config.get_data_directory()
        filepath = os.path.join(data_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                writer.writerow(['Системный монитор - Экспорт данных'])
                writer.writerow([f'Время экспорта: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
                writer.writerow([])
                
                writer.writerow(['=== СИСТЕМНАЯ ИНФОРМАЦИЯ ==='])
                writer.writerow(['Параметр', 'Значение'])
                writer.writerow(['ОС', snapshot.system.os_name])
                writer.writerow(['Версия ОС', snapshot.system.os_version])
                writer.writerow(['Архитектура', snapshot.system.architecture])
                writer.writerow(['Имя компьютера', snapshot.system.hostname])
                writer.writerow(['Пользователь', snapshot.system.username])
                writer.writerow([])
                
                writer.writerow(['=== ПРОЦЕССОР ==='])
                writer.writerow(['Параметр', 'Значение'])
                writer.writerow(['Модель', snapshot.cpu.name])
                writer.writerow(['Физические ядра', snapshot.cpu.physical_cores])
                writer.writerow(['Логические ядра', snapshot.cpu.logical_cores])
                writer.writerow(['Загрузка', f"{snapshot.cpu.usage_percent}%"])
                writer.writerow([])
                
                writer.writerow(['=== ПАМЯТЬ ==='])
                writer.writerow(['Параметр', 'Значение'])
                writer.writerow(['Всего', snapshot.memory.total])
                writer.writerow(['Использовано', snapshot.memory.used])
                writer.writerow(['Свободно', snapshot.memory.free])
                writer.writerow(['Использование', f"{snapshot.memory.usage_percent}%"])
                writer.writerow([])
                
                writer.writerow(['=== ДИСКИ ==='])
                writer.writerow(['Устройство', 'Точка монтирования', 'Всего', 'Использовано', 'Свободно', 'Использование %'])
                for disk in snapshot.disks:
                    writer.writerow([
                        disk.device,
                        disk.mountpoint,
                        disk.total,
                        disk.used,
                        disk.free,
                        f"{disk.usage_percent}%"
                    ])
                writer.writerow([])
                
                writer.writerow(['=== ПРОЦЕССЫ (ТОП-10) ==='])
                writer.writerow(['PID', 'Имя', 'Пользователь', 'CPU %', 'Память %'])
                for proc in snapshot.processes[:10]:
                    writer.writerow([
                        proc.pid,
                        proc.name,
                        proc.username,
                        f"{proc.cpu_percent}%",
                        f"{proc.memory_percent}%"
                    ])
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'format': 'CSV'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'format': 'CSV'
            }