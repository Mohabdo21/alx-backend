#!/usr/bin/env python3
""" LFUCache module """

from collections import Counter
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
        self.keys = []
        self.counts = Counter()

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using LFU algorithm."""
        if key and item:
            if key not in self.cache_data:
                if len(self.keys) >= BaseCaching.MAX_ITEMS:
                    least_freq = min(self.counts.values())
                    least_freq_keys = [
                        k for k, v in self.counts.items() if v == least_freq
                    ]
                    if len(least_freq_keys) > 1:
                        for k in self.keys:
                            if k in least_freq_keys:
                                self.keys.remove(k)
                                del self.counts[k]
                                del self.cache_data[k]
                                print(f"DISCARD: {k}")
                                break
                    else:
                        discard = least_freq_keys[0]
                        self.keys.remove(discard)
                        del self.counts[discard]
                        del self.cache_data[discard]
                        print(f"DISCARD: {discard}")
                self.keys.append(key)
            self.cache_data[key] = item
            self.counts[key] += 1

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        if key in self.cache_data:
            self.counts[key] += 1
            return self.cache_data.get(key)
        return None
