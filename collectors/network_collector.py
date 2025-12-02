import socket
from typing import Dict, Any
from collectors.base_collector import BaseCollector

class NetworkCollector(BaseCollector):
    def collect(self) -> Dict[str, Any]:
        data = {
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'interfaces': [],
            'connections': []
        }
        
        return data