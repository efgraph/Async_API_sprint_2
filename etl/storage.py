import abc
import json
import os.path
from pathlib import Path


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state):
        pass

    @abc.abstractmethod
    def retrieve_state(self):
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        path = Path(self.file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            f.write('{}')

    def save_state(self, state):
        curr = self.retrieve_state()
        with open(self.file_path, 'w') as fs:
            json.dump({**curr, **state}, fs)

    def retrieve_state(self):
        with open(self.file_path) as fs:
            data = json.load(fs)
        return data


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key, value):
        self.storage.save_state({key: value})

    def get_state(self, key: str, default_value=None):
        state = self.storage.retrieve_state()
        res = state.get(key)
        if not res:
            return default_value
        return res