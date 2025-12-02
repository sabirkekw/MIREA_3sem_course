import threading
import time
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import logging

from core.data_models import SystemSnapshot
from collectors.system_collector import SystemCollector
from collectors.hardware_collector import HardwareCollector
from collectors.disk_collector import DiskCollector
from collectors.network_collector import NetworkCollector
from collectors.process_collector import ProcessCollector

logger = logging.getLogger(__name__)

class DataCollectorManager:
    def __init__(self):
        self.collectors = {
            'system': SystemCollector(),
            'hardware': HardwareCollector(),
            'disk': DiskCollector(),
            'network': NetworkCollector(),
            'process': ProcessCollector()
        }
        
        self.is_collecting = False
        self.collection_thread = None
        self.last_snapshot: Optional[SystemSnapshot] = None
        self.callback: Optional[Callable[[SystemSnapshot], None]] = None
        
        logger.info("DataCollectorManager инициализирован")
    
    def collect_all(self) -> SystemSnapshot:
        logger.info("Начало сбора всех данных")
        
        collected_data = {}
        
        for name, collector in self.collectors.items():
            logger.debug(f"Сбор данных от {name}")
            collected_data[name] = collector.safe_collect()
        
        snapshot = SystemSnapshot()
        snapshot.timestamp = datetime.now()
        
        # Заполняем снимок данными (в следующем коммите добавим парсинг)
        self.last_snapshot = snapshot
        
        logger.info(f"Сбор данных завершен. Время: {snapshot.timestamp}")
        return snapshot
    
    def start_collection(self, 
                         interval: int = 5, 
                         callback: Optional[Callable[[SystemSnapshot], None]] = None) -> bool:
        if self.is_collecting:
            logger.warning("Попытка начать сбор данных, когда он уже выполняется")
            return False
        
        self.is_collecting = True
        self.callback = callback
        
        def collection_loop():
            while self.is_collecting:
                try:
                    snapshot = self.collect_all()
                    
                    if callback:
                        callback(snapshot)
                    
                    # Ждем указанный интервал
                    for _ in range(interval * 10):  # Проверяем каждые 0.1 секунды
                        if not self.is_collecting:
                            break
                        time.sleep(0.1)
                        
                except Exception as e:
                    logger.error(f"Ошибка в цикле сбора данных: {str(e)}")
                    time.sleep(interval)
        
        self.collection_thread = threading.Thread(target=collection_loop, daemon=True)
        self.collection_thread.start()
        
        logger.info(f"Запущен периодический сбор данных с интервалом {interval} секунд")
        return True
    
    def stop_collection(self):
        if self.is_collecting:
            self.is_collecting = False
            if self.collection_thread:
                self.collection_thread.join(timeout=2)
            logger.info("Сбор данных остановлен")
        else:
            logger.warning("Попытка остановить сбор данных, когда он не выполняется")
    
    def get_last_snapshot(self) -> Optional[SystemSnapshot]:
        return self.last_snapshot
    
    def get_collector_status(self) -> Dict[str, bool]:
        return {name: True for name in self.collectors.keys()}