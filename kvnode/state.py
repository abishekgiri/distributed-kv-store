from typing import Dict, Any
from threading import Lock

class KVState:
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = Lock()
        self._version = 0  # simple monotonic counter for writes

    def get(self, key: str):
        with self._lock:
            return self._store.get(key), self._version

    def put(self, key: str, value: Any):
        with self._lock:
            self._store[key] = value
            self._version += 1
            return self._version

    def dump_all(self):
        with self._lock:
            return dict(self._store), self._version

kv_state = KVState()
