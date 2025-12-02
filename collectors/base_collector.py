class BaseCollector:
    def __init__(self):
        self._data = {}
    
    def collect(self):
        pass
    
    def safe_collect(self):
        try:
            data = self.collect()
            return data
        except Exception as e:
            return {'error': str(e), 'collector': self.__class__.__name__}
    
    def get_name(self):
        return self.__class__.__name__
