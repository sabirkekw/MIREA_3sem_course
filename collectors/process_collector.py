import psutil
from datetime import datetime

from collectors.base_collector import BaseCollector
from core.config import Config

class ProcessCollector(BaseCollector):
    def __init__(self, max_processes=None):
        super().__init__()
        self.max_processes = max_processes or Config.MAX_PROCESSES_TO_DISPLAY
    
    def collect(self):
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                            'create_time', 'status', 'username', 'memory_info',
                                            'exe', 'cmdline', 'ppid', 'nice', 'num_threads']):
                try:
                    proc_info = proc.info
                    
                    process_data = {
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'cpu_percent': proc_info['cpu_percent'],
                        'memory_percent': proc_info['memory_percent'],
                        'memory_rss': proc_info['memory_info'].rss if proc_info['memory_info'] else 0,
                        'memory_vms': proc_info['memory_info'].vms if proc_info['memory_info'] else 0,
                        'create_time': datetime.fromtimestamp(proc_info['create_time']).isoformat() if proc_info['create_time'] else None,
                        'status': proc_info['status'],
                        'username': proc_info['username'] or '',
                        'exe': proc_info['exe'] or '',
                        'cmdline': ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else '',
                        'ppid': proc_info['ppid'],
                        'nice': proc_info['nice'],
                        'num_threads': proc_info['num_threads']
                    }
                    processes.append(process_data)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            return {
                'processes': processes[:self.max_processes],
                'total_processes': len(processes),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}