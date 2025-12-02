import platform
import socket
import getpass
import psutil
from datetime import datetime

from collectors.base_collector import BaseCollector

class SystemCollector(BaseCollector):
    def collect(self):
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        data = {
            'os_name': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.architecture()[0],
            'machine': platform.machine(),
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'fqdn': socket.getfqdn(),
            'username': getpass.getuser(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation(),
            'boot_time': boot_time.isoformat(),
            'uptime': int(datetime.now().timestamp() - psutil.boot_time()),
            'timestamp': datetime.now().isoformat(),
            'users': []
        }
        
        try:
            for user in psutil.users():
                data['users'].append({
                    'name': user.name,
                    'terminal': user.terminal or '',
                    'host': user.host or '',
                    'started': datetime.fromtimestamp(user.started).isoformat()
                })
        except:
            pass
        
        return data