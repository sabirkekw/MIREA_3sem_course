import json
import os
from datetime import datetime
from core.config import Config

class JSONExporter:
    @staticmethod
    def export(data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_info_{timestamp}.json"
        
        data_dir = Config.get_data_directory()
        filepath = os.path.join(data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'format': 'JSON'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'format': 'JSON'
            }