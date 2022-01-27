class Database:
    
    FILENAME = "pydb.db"
    
    def __init__(self):
        self._db = {}
        self._history = []
        self._open_file()

    def get(self, key: str):
        return self._db.get(key, None)
    
    def set(self, key: str, value):
        if self._db.get(key, None):
            raise Exception("Key already exists, use update() instead")
        self._db[key] = value
        
    def update(self, key: str, value):
        if not self._db.get(key, None):
            raise Exception("Key does not exist, use set() instead")
        self._db[key] = value
        
    def delete(self, key: str):
        self._db.pop(key, None)
        
    def commit(self, dataset=None, check=True):
        
        if dataset is None:
            dataset = self._db
        
        with open(self.FILENAME, 'w') as f:
            f.seek(0)
            for key, value in dataset.items():
                f.write(f"{key}§{value}\n")
            f.truncate()
        self._add_history(check, dataset)
        
    def restore(self):
        self._history.pop()
        curr = self._history[-1]
        self.commit(curr, False)
    
    def _open_file(self):
        with open(self.FILENAME, 'r') as f:
            for line in f.readlines():
                key, value = line.split('§')
                self._db[key] = value[:-1]
                
    def _add_history(self, check: bool, dataset=None):
        if check:
            if len(self._history) == 10:
                del self._history[0]
            self._history.append(dataset.copy())
            