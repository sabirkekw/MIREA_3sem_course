import psutil
import os

from collectors.base_collector import BaseCollector

class DiskCollector(BaseCollector):
    def collect(self):
        try:
            data = {
                'partitions': [],
                'io_counters': {},
                'total': {
                    'total': 0,
                    'used': 0,
                    'free': 0
                }
            }
            
            for partition in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    partition_info = {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'opts': partition.opts,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    }
                    data['partitions'].append(partition_info)
                    
                    data['total']['total'] += usage.total
                    data['total']['used'] += usage.used
                    data['total']['free'] += usage.free
                except:
                    continue
            
            try:
                io = psutil.disk_io_counters()
                if io:
                    data['io_counters'] = {
                        'read_count': io.read_count,
                        'write_count': io.write_count,
                        'read_bytes': io.read_bytes,
                        'write_bytes': io.write_bytes,
                        'read_time': io.read_time,
                        'write_time': io.write_time
                    }
            except:
                pass
            
            return data
        except Exception as e:
            return {'error': str(e)}