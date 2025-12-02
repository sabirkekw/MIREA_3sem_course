import psutil
import socket

from collectors.base_collector import BaseCollector

class NetworkCollector(BaseCollector):
    def collect(self):
        try:
            data = {
                'interfaces': [],
                'connections': [],
                'io_counters': {},
                'addresses': {}
            }
            
            for interface_name, addresses in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface_name,
                    'addresses': [],
                    'stats': {}
                }
                
                for addr in addresses:
                    family = addr.family
                    family_str = self._family_to_string(family)
                    
                    addr_info = {
                        'family': family_str,
                        'family_code': int(family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    }
                    interface_info['addresses'].append(addr_info)
                
                try:
                    stats = psutil.net_if_stats()
                    if interface_name in stats:
                        stat = stats[interface_name]
                        interface_info['stats'] = {
                            'isup': bool(stat.isup),
                            'duplex': self._duplex_to_string(stat.duplex),
                            'speed': stat.speed,
                            'mtu': stat.mtu
                        }
                except:
                    interface_info['stats'] = {'isup': False}
                
                data['interfaces'].append(interface_info)
            
            try:
                io = psutil.net_io_counters()
                data['io_counters'] = {
                    'bytes_sent': io.bytes_sent,
                    'bytes_recv': io.bytes_recv,
                    'packets_sent': io.packets_sent,
                    'packets_recv': io.packets_recv,
                    'errin': io.errin,
                    'errout': io.errout,
                    'dropin': io.dropin,
                    'dropout': io.dropout
                }
            except:
                pass
            
            try:
                for conn in psutil.net_connections(kind='inet'):
                    conn_info = {
                        'fd': conn.fd,
                        'family': self._family_to_string(conn.family),
                        'type': self._socktype_to_string(conn.type),
                        'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                        'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        'status': conn.status,
                        'pid': conn.pid
                    }
                    data['connections'].append(conn_info)
            except:
                pass
            
            data['addresses'] = {
                'hostname': socket.gethostname(),
                'fqdn': socket.getfqdn()
            }
            
            try:
                all_ips = []
                for interface_name, addresses in psutil.net_if_addrs().items():
                    for addr in addresses:
                        if addr.family == socket.AF_INET and addr.address:
                            if addr.address not in ['127.0.0.1', '127.0.1.1']:
                                all_ips.append(addr.address)
                
                if all_ips:
                    data['addresses']['ip_address'] = all_ips[0]
                else:
                    data['addresses']['ip_address'] = socket.gethostbyname(socket.gethostname())
            except:
                data['addresses']['ip_address'] = None
            
            try:
                import urllib.request
                external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
                data['addresses']['external_ip'] = external_ip
            except:
                data['addresses']['external_ip'] = None
            
            return data
        except Exception as e:
            return {'error': str(e)}
    
    def _family_to_string(self, family):
        try:
            import socket
            if family == socket.AF_INET:
                return 'AF_INET'
            elif family == socket.AF_INET6:
                return 'AF_INET6'
            elif family == socket.AF_PACKET:
                return 'AF_PACKET'
            elif hasattr(socket, 'AF_LINK') and family == socket.AF_LINK:
                return 'AF_LINK'
            else:
                import psutil
                if hasattr(psutil, 'AF_LINK') and family == getattr(psutil, 'AF_LINK', -1):
                    return 'AF_LINK'
                return str(family)
        except:
            return str(family)
    
    def _duplex_to_string(self, duplex):
        duplex_map = {
            0: 'UNKNOWN',
            1: 'HALF',
            2: 'FULL'
        }
        return duplex_map.get(duplex, str(duplex))
    
    def _socktype_to_string(self, socktype):
        try:
            import socket
            if socktype == socket.SOCK_STREAM:
                return 'SOCK_STREAM'
            elif socktype == socket.SOCK_DGRAM:
                return 'SOCK_DGRAM'
            elif socktype == socket.SOCK_RAW:
                return 'SOCK_RAW'
            else:
                return str(socktype)
        except:
            return str(socktype)