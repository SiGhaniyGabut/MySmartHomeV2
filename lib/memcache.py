import gc

class CacheStore:
    def __init__(self):
        self.cache = None
        gc.collect()

    def set(self, cache):
        if type(cache).__name__ == 'NoneType': self.cache = cache
        elif type(cache).__name__ == 'str': self.cache = bytes(cache, 'utf-8')
        else: self.cache = bytes(str(cache), 'utf-8')

    def get(self):
        return self.cache.decode('utf-8') if self.cache is not None else None
