#!/usr/bin/env python3
""" FIFOCache module. """

from collections import deque
from typing import Any, Optional

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache defines:
        - caching system using FIFO algorithm.
    """

    def __init__(self):
        """Initialization."""
        super().__init__()
        self.queue = deque()

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using FIFO algorithm."""
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.queue.append(key)
            if len(self.queue) > BaseCaching.MAX_ITEMS:
                discarded_key = self.queue.popleft()
                del self.cache_data[discarded_key]
                print("DISCARD: {}".format(discarded_key))

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        return self.cache_data.get(key) if key is not None else None
