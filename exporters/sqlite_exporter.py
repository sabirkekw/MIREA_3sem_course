import sqlite3
import os
import json
from datetime import datetime
from core.config import Config

class SQLiteExporter:
    def __init__(self, db_path=None):
        if db_path is None:
            data_dir = Config.get_data_directory()
            db_path = os.path.join(data_dir, 'system_monitor.db')
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                data_json TEXT NOT NULL,
                os_name TEXT,
                hostname TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snapshot_metadata (
                snapshot_id INTEGER,
                cpu_usage REAL,
                memory_usage REAL,
                total_disks INTEGER,
                total_processes INTEGER,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def export(self, snapshot):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            data_json = json.dumps(snapshot.to_dict(), ensure_ascii=False)
            timestamp = snapshot.timestamp.isoformat()
            
            cursor.execute('''
                INSERT INTO snapshots (timestamp, data_json, os_name, hostname)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, data_json, snapshot.system.os_name, snapshot.system.hostname))
            
            snapshot_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO snapshot_metadata 
                (snapshot_id, cpu_usage, memory_usage, total_disks, total_processes)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                snapshot_id,
                snapshot.cpu.usage_percent,
                snapshot.memory.usage_percent,
                len(snapshot.disks),
                len(snapshot.processes)
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'filepath': self.db_path,
                'snapshot_id': snapshot_id,
                'format': 'SQLite'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'format': 'SQLite'
            }
    
    def get_all_snapshots(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.id, s.timestamp, s.os_name, s.hostname, 
                       m.cpu_usage, m.memory_usage
                FROM snapshots s
                LEFT JOIN snapshot_metadata m ON s.id = m.snapshot_id
                ORDER BY s.timestamp DESC
            ''')
            
            snapshots = cursor.fetchall()
            conn.close()
            
            return snapshots
        except:
            return []