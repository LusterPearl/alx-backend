#!/usr/bin/python3
"""Module for BasicCache class."""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """A caching system with no limit."""

    def put(self, key, item):
        """Add an item to the cache."""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
