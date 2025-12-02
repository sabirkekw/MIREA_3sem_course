import threading
import time
from datetime import datetime

from core.data_models import SystemSnapshot, SystemInfo, CPUInfo, MemoryInfo, DiskInfo, NetworkInterface, ProcessInfo
from collectors.system_collector import SystemCollector
from collectors.hardware_collector import HardwareCollector
from collectors.disk_collector import DiskCollector
from collectors.network_collector import NetworkCollector
from collectors.process_collector import ProcessCollector

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
        self.last_snapshot = None
        self.callback = None
    
    def collect_all(self):
        collected_data = {}
        
        for name, collector in self.collectors.items():
            collected_data[name] = collector.safe_collect()
        
        snapshot = SystemSnapshot()
        snapshot.timestamp = datetime.now()
        
        self._parse_system_data(snapshot, collected_data.get('system', {}))
        self._parse_hardware_data(snapshot, collected_data.get('hardware', {}))
        self._parse_disk_data(snapshot, collected_data.get('disk', {}))
        self._parse_network_data(snapshot, collected_data.get('network', {}))
        self._parse_process_data(snapshot, collected_data.get('process', {}))
        
        self.last_snapshot = snapshot
        return snapshot
    
    def _parse_system_data(self, snapshot, data):
        if 'error' in data:
            snapshot.system.os_name = f"Ошибка: {data['error']}"
            return
        
        snapshot.system.os_name = data.get('os_name', '')
        snapshot.system.os_version = data.get('os_version', '')
        snapshot.system.architecture = data.get('architecture', '')
        snapshot.system.hostname = data.get('hostname', '')
        snapshot.system.username = data.get('username', '')
        
        boot_time_str = data.get('boot_time')
        if boot_time_str:
            try:
                snapshot.system.boot_time = datetime.fromisoformat(boot_time_str)
            except:
                pass
    
    def _parse_hardware_data(self, snapshot, data):
        if 'error' in data:
            snapshot.cpu.name = f"Ошибка: {data['error']}"
            return
        
        cpu_data = data.get('cpu', {})
        if 'error' not in cpu_data:
            snapshot.cpu.name = cpu_data.get('name', '')
            snapshot.cpu.physical_cores = cpu_data.get('physical_cores', 0)
            snapshot.cpu.logical_cores = cpu_data.get('logical_cores', 0)
            snapshot.cpu.usage_percent = cpu_data.get('usage_percent', 0.0)
            
            freq = cpu_data.get('frequency', {})
            snapshot.cpu.frequency_current = freq.get('current', 0.0)
            snapshot.cpu.frequency_min = freq.get('min', 0.0)
            snapshot.cpu.frequency_max = freq.get('max', 0.0)
        
        memory_data = data.get('memory', {}).get('virtual', {})
        if 'error' not in memory_data:
            snapshot.memory.total = memory_data.get('total', 0)
            snapshot.memory.available = memory_data.get('available', 0)
            snapshot.memory.used = memory_data.get('used', 0)
            snapshot.memory.free = memory_data.get('free', 0)
            snapshot.memory.usage_percent = memory_data.get('percent', 0.0)
    
    def _parse_disk_data(self, snapshot, data):
        if 'error' in data:
            return
        
        partitions = data.get('partitions', [])
        for partition in partitions:
            if 'error' not in partition:
                disk = DiskInfo()
                disk.device = partition.get('device', '')
                disk.mountpoint = partition.get('mountpoint', '')
                disk.filesystem = partition.get('fstype', '')
                disk.total = partition.get('total', 0)
                disk.used = partition.get('used', 0)
                disk.free = partition.get('free', 0)
                disk.usage_percent = partition.get('percent', 0.0)
                snapshot.disks.append(disk)
    
    def _parse_network_data(self, snapshot, data):
        if 'error' in data:
            return
        
        interfaces = data.get('interfaces', [])
        for interface in interfaces:
            net_if = NetworkInterface()
            net_if.name = interface.get('name', '')
            
            addresses = interface.get('addresses', [])
            for addr in addresses:
                family = addr.get('family', '')
                address = addr.get('address', '')
                
                if not address:
                    continue
                
                # IPv4 адрес
                if family == 'AF_INET' and address not in ['127.0.0.1', '127.0.1.1']:
                    net_if.ip_address = address
                
                # MAC адрес
                elif family in ['AF_PACKET', 'AF_LINK'] and address != '00:00:00:00:00:00':
                    net_if.mac_address = address
            
            stats = interface.get('stats', {})
            net_if.status = 'Up' if stats.get('isup') else 'Down'
            
            snapshot.network_interfaces.append(net_if)
        
    def _parse_process_data(self, snapshot, data):
        if 'error' in data:
            return
        
        processes = data.get('processes', [])
        for proc in processes:
            process = ProcessInfo()
            process.pid = proc.get('pid', 0)
            process.name = proc.get('name', '')
            process.username = proc.get('username', '')
            process.cpu_percent = proc.get('cpu_percent', 0.0)
            process.memory_percent = proc.get('memory_percent', 0.0)
            process.memory_rss = proc.get('memory_rss', 0)
            process.status = proc.get('status', '')
            snapshot.processes.append(process)
    
    def start_collection(self, interval=5, callback=None):
        if self.is_collecting:
            return False
        
        self.is_collecting = True
        self.callback = callback
        
        def collection_loop():
            while self.is_collecting:
                try:
                    snapshot = self.collect_all()
                    
                    if callback:
                        callback(snapshot)
                    
                    for _ in range(interval * 10):
                        if not self.is_collecting:
                            break
                        time.sleep(0.1)
                        
                except Exception:
                    time.sleep(interval)
        
        self.collection_thread = threading.Thread(target=collection_loop, daemon=True)
        self.collection_thread.start()
        
        return True
    
    def stop_collection(self):
        if self.is_collecting:
            self.is_collecting = False
            if self.collection_thread:
                self.collection_thread.join(timeout=2)
    
    def get_last_snapshot(self):
        return self.last_snapshot
    
    def get_collector_status(self):
        return {name: True for name in self.collectors.keys()}