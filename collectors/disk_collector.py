from typing import Dict, Any, List
from collectors.base_collector import BaseCollector

class DiskCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        # Заглушка - в следующем коммите добавим реальный сбор данных
        data = {
            'partitions': [],
            'total_space': 0,
            'used_space': 0,
            'free_space': 0
        }
        
        return data