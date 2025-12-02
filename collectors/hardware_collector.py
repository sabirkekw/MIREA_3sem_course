from typing import Dict, Any
from collectors.base_collector import BaseCollector

class HardwareCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        # Заглушка - в следующем коммите добавим реальный сбор данных
        data = {
            'cpu': {
                'name': 'Не определено',
                'cores': 0,
                'usage_percent': 0.0
            },
            'memory': {
                'total': 0,
                'available': 0,
                'usage_percent': 0.0
            },
            'gpu': []
        }
        
        return data