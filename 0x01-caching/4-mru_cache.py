#!/usr/bin/python3
"""Module for MRUCache class."""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """A caching system that uses MRU (Most Recently Used)
      replacement policy."""

    def __init__(self):
        """Initialize the MRUCache."""
        super().__init__()
        self.recently_used = []

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            mru_key = self.recently_used.pop(0)
            del self.cache_data[mru_key]
            print("DISCARD:", mru_key)

        self.cache_data[key] = item
        self.recently_used.insert(0, key)

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None
        self.recently_used.remove(key)
        self.recently_used.insert(0, key)
        return self.cache_data[key]
