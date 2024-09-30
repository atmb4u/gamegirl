from datetime import datetime


class MemoryManager:
    def __init__(self):
        self.memory = {}
        self.history = []
        self.version = 0

    def read(self, key: str):
        return self.memory.get(key, None)

    def write(self, key: str, value):
        self.version += 1
        timestamp = datetime.now().isoformat()
        self.memory[key] = value
        self.history.append((self.version, key, value, timestamp))

    def update(self, key: str, value):
        if key in self.memory:
            self.version += 1
            timestamp = datetime.now().isoformat()
            self.memory[key] = value
            self.history.append((self.version, key, value, timestamp))
        else:
            self.write(key, value)

    def get_latest_version(self):
        return self.version

    def get_history(self):
        return self.history