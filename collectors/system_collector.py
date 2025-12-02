import platform
import socket
import getpass
from datetime import datetime

from collectors.base_collector import BaseCollector

class SystemCollector(BaseCollector):
    def collect(self):
        data = {
            'os_name': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'hostname': socket.gethostname(),
            'username': getpass.getuser(),
            'python_version': platform.python_version(),
            'timestamp': datetime.now().isoformat()
        }
        return data