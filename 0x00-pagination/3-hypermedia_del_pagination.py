#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE, encoding="utf-8") as f:
                reader = csv.reader(f)
                dataset = list(reader)
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {i: dataset[i]
                                      for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """
        Returns paginated data starting from the given index.

        Args:
            index (int): Starting index for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Paginated data and related information.
        """
        f_dataset = []
        dataset = self.indexed_dataset()
        index = 0 if index is None else index
        keys = sorted(dataset.keys())
        assert index >= 0 and index <= keys[-1]
        [f_dataset.append(i)
         for i in keys if i >= index and len(f_dataset) <= page_size]
        data = [dataset[v] for v in f_dataset[:-1]]
        next_index = f_dataset[-1] if len(f_dataset) - page_size == 1 else None
        return {'index': index, 'data': data,
                'page_size': len(data), 'next_index': next_index}
