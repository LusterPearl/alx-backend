#!/usr/bin/python3
"""Module for LFUCache class."""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """A caching system that uses LFU (Least Frequently Used)
      replacement policy."""

    def __init__(self):
        """Initialize the LFUCache."""
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            min_freq = min(self.frequency.values())
            keys_to_discard = [k for k, v in self.frequency.items()
                               if v == min_freq]
            if len(keys_to_discard) > 1:
                lru_key = min(self.cache_data, key=self.frequency.get)
                keys_to_discard = [lru_key]

            for k in keys_to_discard:
                del self.cache_data[k]
                del self.frequency[k]
                print("DISCARD:", k)

        self.cache_data[key] = item
        self.frequency[key] = 0

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None

        self.frequency[key] += 1
        return self.cache_data[key]
