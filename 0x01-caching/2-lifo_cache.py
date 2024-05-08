#!/usr/bin/python3
"""Module for LIFOCache class."""

from base_caching import BaseCaching
from collections import deque


class LIFOCache(BaseCaching):
    """A caching system that uses LIFO (Last-In, First-Out)
      replacement policy."""

    def __init__(self):
        """Initialize the LIFOCache."""
        super().__init__()
        self.insertion_order = deque()

    def put(self, key, item):
        """Add an item to the cache."""
        if key is None or item is None:
            return

        if len(self.cache_data) >= self.MAX_ITEMS:
            discarded_key = self.insertion_order.pop()
            del self.cache_data[discarded_key]
            print("DISCARD:", discarded_key)

        self.cache_data[key] = item
        self.insertion_order.appendleft(key)

    def get(self, key):
        """Retrieve an item from the cache."""
        if key is None or key not in self.cache_data:
            return None

        self.insertion_order.remove(key)
        self.insertion_order.appendleft(key)
        return self.cache_data[key]
