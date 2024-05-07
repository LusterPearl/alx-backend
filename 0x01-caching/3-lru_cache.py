#!/usr/bin/python3
"""Module for LRUCache class."""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """A caching system that uses LRU (Least Recently Used)
      replacement policy."""

    def __init__(self):
        """Initialize the LRUCache."""
        super().__init__()
        self.lru_list = []

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            lru_key = self.lru_list.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD:", lru_key)

        self.cache_data[key] = item
        self.lru_list.append(key)

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None
        self.lru_list.remove(key)
        self.lru_list.append(key)
        return self.cache_data[key]
