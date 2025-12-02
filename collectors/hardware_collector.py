import psutil
import platform
import subprocess
import re

from collectors.base_collector import BaseCollector

class HardwareCollector(BaseCollector):
    def collect(self):
        data = {
            'cpu': self._get_cpu_info(),
            'memory': self._get_memory_info(),
            'gpu': self._get_gpu_info(),
            'sensors': self._get_sensors_info()
        }
        return data
    
    def _get_cpu_info(self):
        try:
            cpu_info = {
                'name': self._get_cpu_name(),
                'physical_cores': psutil.cpu_count(logical=False) or 0,
                'logical_cores': psutil.cpu_count(logical=True) or 0,
                'usage_percent': psutil.cpu_percent(interval=0.1),
                'usage_per_core': psutil.cpu_percent(interval=0.1, percpu=True),
                'frequency': {},
                'stats': {},
                'times': {}
            }
            
            try:
                freq = psutil.cpu_freq()
                if freq:
                    cpu_info['frequency'] = {
                        'current': freq.current,
                        'min': freq.min,
                        'max': freq.max
                    }
            except:
                pass
            
            try:
                stats = psutil.cpu_stats()
                cpu_info['stats'] = {
                    'ctx_switches': stats.ctx_switches,
                    'interrupts': stats.interrupts,
                    'soft_interrupts': stats.soft_interrupts,
                    'syscalls': stats.syscalls
                }
            except:
                pass
            
            try:
                times = psutil.cpu_times()
                cpu_info['times'] = {
                    'user': times.user,
                    'system': times.system,
                    'idle': times.idle
                }
            except:
                pass
            
            return cpu_info
        except Exception as e:
            return {'error': str(e)}
    
    def _get_cpu_name(self):
        try:
            if platform.system() == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                name = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                winreg.CloseKey(key)
                return name.strip()
            elif platform.system() == "Linux":
                with open('/proc/cpuinfo', 'r') as f:
                    for line in f:
                        if 'model name' in line:
                            return line.split(':')[1].strip()
            elif platform.system() == "Darwin":
                return subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
        except:
            pass
        return platform.processor() or "Unknown CPU"
    
    def _get_memory_info(self):
        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()
            
            memory_info = {
                'virtual': {
                    'total': virtual_memory.total,
                    'available': virtual_memory.available,
                    'used': virtual_memory.used,
                    'free': virtual_memory.free,
                    'percent': virtual_memory.percent,
                    'units': 'bytes'
                },
                'swap': {
                    'total': swap_memory.total,
                    'used': swap_memory.used,
                    'free': swap_memory.free,
                    'percent': swap_memory.percent,
                    'sin': swap_memory.sin,
                    'sout': swap_memory.sout
                }
            }
            return memory_info
        except Exception as e:
            return {'error': str(e)}
    
    def _get_gpu_info(self):
        gpu_info = []
        
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                gpu_info.append({
                    'name': gpu.name,
                    'memory_total': gpu.memoryTotal,
                    'memory_used': gpu.memoryUsed,
                    'memory_free': gpu.memoryFree,
                    'temperature': gpu.temperature,
                    'utilization': gpu.load * 100,
                    'vendor': 'NVIDIA' if 'nvidia' in gpu.name.lower() else 'AMD/Other'
                })
            return gpu_info
        except:
            pass
        
        try:
            if platform.system() == "Windows":
                import wmi
                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    gpu_info.append({
                        'name': gpu.Name,
                        'memory_total': int(gpu.AdapterRAM) if gpu.AdapterRAM else 0,
                        'vendor': gpu.AdapterCompatibility or 'Unknown'
                    })
            elif platform.system() == "Linux":
                result = subprocess.run(['lspci'], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'VGA' in line or '3D' in line:
                            gpu_info.append({
                                'name': line.split(': ')[-1],
                                'vendor': 'Unknown'
                            })
        except:
            pass
        
        return gpu_info
    
    def _get_sensors_info(self):
        sensors = {}
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    sensors[name] = []
                    for entry in entries:
                        sensors[name].append({
                            'label': entry.label or name,
                            'current': entry.current,
                            'high': entry.high,
                            'critical': entry.critical
                        })
        except:
            pass
        return sensors