from typing import Dict, Any, List
from collectors.base_collector import BaseCollector
from core.config import Config

class ProcessCollector(BaseCollector):
    def __init__(self, max_processes: int = None):
        super().__init__()
        self.max_processes = max_processes or Config.MAX_PROCESSES_TO_DISPLAY
    
    def collect(self) -> Dict[str, Any]:
        # Заглушка - в следующем коммите добавим реальный сбор данных
        data = {
            'processes': [],
            'total_processes': 0,
            'timestamp': '2024-01-01T00:00:00'
        }
        
        return data