class Config:
    DEFAULT_COLLECTION_INTERVAL = 5
    MAX_PROCESSES_TO_DISPLAY = 20
    DATA_DIRECTORY = "data"
    EXPORT_FORMATS = ['JSON', 'CSV', 'SQLite']
    LOG_LEVEL = "INFO"
    LOG_FILE = "system_monitor.log"
    
    @staticmethod
    def get_data_directory():
        import os
        os.makedirs(Config.DATA_DIRECTORY, exist_ok=True)
        return Config.DATA_DIRECTORY