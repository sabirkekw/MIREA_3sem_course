# core/data_models.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SystemInfo:
    os_name: str = ""
    os_version: str = ""
    architecture: str = ""
    hostname: str = ""
    username: str = ""
    boot_time: datetime = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class CPUInfo:
    name: str = ""
    physical_cores: int = 0
    logical_cores: int = 0
    usage_percent: float = 0.0
    frequency_current: float = 0.0
    frequency_min: float = 0.0
    frequency_max: float = 0.0

@dataclass
class MemoryInfo:
    total: int = 0
    available: int = 0
    used: int = 0
    free: int = 0
    usage_percent: float = 0.0

@dataclass
class DiskInfo:
    device: str = ""
    mountpoint: str = ""
    filesystem: str = ""
    total: int = 0
    used: int = 0
    free: int = 0
    usage_percent: float = 0.0

@dataclass
class NetworkInterface:
    name: str = ""
    ip_address: str = ""
    mac_address: str = ""
    status: str = ""

@dataclass
class ProcessInfo:
    pid: int = 0
    name: str = ""
    username: str = ""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_rss: int = 0
    status: str = ""

@dataclass
class SystemSnapshot:
    timestamp: datetime = field(default_factory=datetime.now)
    system: SystemInfo = field(default_factory=SystemInfo)
    cpu: CPUInfo = field(default_factory=CPUInfo)
    memory: MemoryInfo = field(default_factory=MemoryInfo)
    disks: list = field(default_factory=list)
    network_interfaces: list = field(default_factory=list)
    processes: list = field(default_factory=list)
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'system': {
                'os_name': self.system.os_name,
                'os_version': self.system.os_version,
                'architecture': self.system.architecture,
                'hostname': self.system.hostname,
                'username': self.system.username,
                'boot_time': self.system.boot_time.isoformat() if self.system.boot_time else None
            },
            'cpu': {
                'name': self.cpu.name,
                'physical_cores': self.cpu.physical_cores,
                'logical_cores': self.cpu.logical_cores,
                'usage_percent': self.cpu.usage_percent,
                'frequency_current': self.cpu.frequency_current,
                'frequency_min': self.cpu.frequency_min,
                'frequency_max': self.cpu.frequency_max
            },
            'memory': {
                'total': self.memory.total,
                'available': self.memory.available,
                'used': self.memory.used,
                'free': self.memory.free,
                'usage_percent': self.memory.usage_percent
            },
            'disks': [
                {
                    'device': disk.device,
                    'mountpoint': disk.mountpoint,
                    'filesystem': disk.filesystem,
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'usage_percent': disk.usage_percent
                }
                for disk in self.disks
            ],
            'network_interfaces': [
                {
                    'name': interface.name,
                    'ip_address': interface.ip_address,
                    'mac_address': interface.mac_address,
                    'status': interface.status
                }
                for interface in self.network_interfaces
            ],
            'processes': [
                {
                    'pid': process.pid,
                    'name': process.name,
                    'username': process.username,
                    'cpu_percent': process.cpu_percent,
                    'memory_percent': process.memory_percent,
                    'memory_rss': process.memory_rss,
                    'status': process.status
                }
                for process in self.processes
            ]
        }