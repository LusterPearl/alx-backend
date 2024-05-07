#!/usr/bin/python3
"""Module for MRUCache class."""

from base_caching import BaseCaching

class MRUCache(BaseCaching):
    """A caching system that uses MRU (Most Recently Used)
      replacement policy."""
    
    def __init__(self):
        """Initialize the MRUCache."""
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            mru_key = next(reversed(self.cache_data))
            del self.cache_data[mru_key]
            print("DISCARD:", mru_key)

        self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.pop(key)
        self.cache_data[key] = self.cache_data.pop(key)
        return self.cache_data[key]