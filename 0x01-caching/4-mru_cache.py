#!/usr/bin/env python3
""" MRUCache module. """

from typing import Any, Optional

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    MRUCache defines:
        - caching system using MRU algorithm.
    """

    def __init__(self) -> None:
        """Initialize MRU algorithm."""
        super().__init__()
        self.keys = []

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using MRU algorithm."""
        if key and item:
            if key in self.cache_data:
                self.keys.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.keys.pop()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        if key in self.cache_data:
            self.keys.remove(key)
            self.keys.append(key)
            return self.cache_data.get(key)
        return None
