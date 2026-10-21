"""
Thread-safe LRU Cache implementation addressing the Concurrency section.
Uses threading.RLock for synchronized access across multi-threaded environments.
"""

import threading
from typing import Any
from lru_cache import LRUCache


class ThreadSafeLRUCache:
    """
    A thread-safe wrapper around LRUCache using Reentrant Locks (RLock).
    Ensures safe concurrent reads, writes, and evictions across multiple threads.
    """

    def __init__(self, capacity: int):
        self._cache = LRUCache(capacity)
        self._lock = threading.RLock()
        self.hits: int = 0
        self.misses: int = 0
        self.evictions: int = 0

    def get(self, key: Any) -> Any:
        with self._lock:
            val = self._cache.get(key)
            if val != -1:
                self.hits += 1
            else:
                self.misses += 1
            return val

    def put(self, key: Any, value: Any) -> None:
        with self._lock:
            will_evict = (key not in self._cache.cache) and (len(self._cache.cache) >= self._cache.capacity)
            self._cache.put(key, value)
            if will_evict:
                self.evictions += 1

    def peek(self, key: Any) -> Any:
        """Inspects key without changing LRU recency order."""
        with self._lock:
            node = self._cache.cache.get(key)
            return node.value if node else -1

    def delete(self, key: Any) -> bool:
        """Explicitly deletes a key in O(1)."""
        with self._lock:
            if key not in self._cache.cache:
                return False
            node = self._cache.cache[key]
            self._cache._remove(node)
            del self._cache.cache[key]
            return True

    def clear(self) -> None:
        with self._lock:
            self._cache.cache.clear()
            self._cache.head.next = self._cache.tail
            self._cache.tail.prev = self._cache.head

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = self.hits + self.misses
            hit_ratio = round(self.hits / total, 4) if total > 0 else 0.0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "evictions": self.evictions,
                "hit_ratio": hit_ratio,
                "size": len(self._cache),
                "capacity": self._cache.capacity
            }

    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)
