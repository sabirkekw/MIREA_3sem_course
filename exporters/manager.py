from exporters.json_exporter import JSONExporter
from exporters.csv_exporter import CSVExporter
from exporters.sqlite_exporter import SQLiteExporter

class ExportManager:
    def __init__(self):
        self.exporters = {
            'JSON': JSONExporter(),
            'CSV': CSVExporter(),
            'SQLite': SQLiteExporter()
        }
    
    def export(self, snapshot, format_type='JSON', filename=None):
        if format_type not in self.exporters:
            return {
                'success': False,
                'error': f'Неподдерживаемый формат: {format_type}',
                'format': format_type
            }
        
        exporter = self.exporters[format_type]
        
        if format_type == 'JSON':
            return exporter.export(snapshot.to_dict(), filename)
        elif format_type == 'CSV':
            return exporter.export(snapshot, filename)
        elif format_type == 'SQLite':
            return exporter.export(snapshot)
    
    def get_available_formats(self):
        return list(self.exporters.keys())