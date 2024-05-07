#!/usr/bin/python3
"""Module for FIFOCache class."""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """A caching system that uses FIFO (First-In, First-Out)
    replacement policy."""

    def __init__(self):
        """Initialize the FIFOCache."""
        super().__init__()

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            discarded_key = next(iter(self.cache_data))
            del self.cache_data[discarded_key]
            print("DISCARD:", discarded_key)

        self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
