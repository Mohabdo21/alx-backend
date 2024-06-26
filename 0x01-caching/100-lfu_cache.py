#!/usr/bin/env python3
""" LFUCache module """

from collections import defaultdict
from typing import Any, Optional

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines:
        - caching system using LFU algorithm.
    """

    def __init__(self) -> None:
        """Initialize LFU algorithm."""
        super().__init__()
        self.usage_count = defaultdict(int)
        self.key_order = []

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using LFU algorithm."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_count[key] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used item(s)
                min_cnt = min(self.usage_count.values())
                least_frequent_keys = [
                    k for k in self.key_order if self.usage_count[k] == min_cnt
                ]

                # If there are multiple least frequently used items, use FIFO
                if len(least_frequent_keys) > 1:
                    discard_key = least_frequent_keys[0]
                else:
                    discard_key = least_frequent_keys[0]

                self.cache_data.pop(discard_key)
                self.usage_count.pop(discard_key)
                self.key_order.remove(discard_key)
                print(f"DISCARD: {discard_key}")

            self.cache_data[key] = item
            self.usage_count[key] += 1
            self.key_order.append(key)

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        if key in self.cache_data:
            self.usage_count[key] += 1
            return self.cache_data[key]
        return None
