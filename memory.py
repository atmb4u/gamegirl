from datetime import datetime


class MemoryManager:
    """
    Manages the game memory, including reading, writing, and updating memory, as well as maintaining a history of changes.

    Attributes:
        memory (dict): The current memory state.
        history (list): A history of memory changes.
        version (int): The current version number of the memory.

    Methods:
        __init__: Initializes the memory manager.
        read: Reads a value from memory.
        write: Writes a value to memory and updates the history.
        update: Updates a value in memory and updates the history.
        get_latest_version: Gets the latest version number of the memory.
        get_history: Gets the history of memory changes.
    """

    def __init__(self):
        """Initializes the memory manager."""
        self.memory = {}
        self.history = []
        self.version = 0

    def read(self, key: str):
        """
        Reads a value from memory.

        Args:
            key (str): The key to read from memory.

        Returns:
            The value associated with the key, or None if the key does not exist.
        """
        return self.memory.get(key, None)

    def write(self, key: str, value):
        """
        Writes a value to memory and updates the history.

        Args:
            key (str): The key to write to memory.
            value: The value to write to memory.
        """
        self.version += 1
        timestamp = datetime.now().isoformat()
        self.memory[key] = value
        self.history.append((self.version, key, value, timestamp))

    def update(self, key: str, value):
        """
        Updates a value in memory and updates the history.

        Args:
            key (str): The key to update in memory.
            value: The new value to update in memory.
        """
        if key in self.memory:
            self.version += 1
            timestamp = datetime.now().isoformat()
            self.memory[key] = value
            self.history.append((self.version, key, value, timestamp))
        else:
            self.write(key, value)

    def get_latest_version(self):
        """
        Gets the latest version number of the memory.

        Returns:
            int: The latest version number.
        """
        return self.version

    def get_history(self):
        """
        Gets the history of memory changes.

        Returns:
            list: The history of memory changes.
        """
        return self.history