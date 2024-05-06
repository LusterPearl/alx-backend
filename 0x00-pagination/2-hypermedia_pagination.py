#!/usr/bin/env python3
"""Module for Server class with hypermedia pagination"""

import csv
import math
from typing import List

def index_range(page: int, page_size: int) -> tuple[int, int]:
    """
    Return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those
    particular pagination parameters.
    """
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return start_idx, end_idx

class Server:
    """Server class to paginate a database of popular baby.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Return a dictionary containing hypermedia pagination.
        """
        assert (
                isinstance(page, int) and page > 0
              ), "Page must be a positive integer"
        assert (
                isinstance(page_size, int) and page_size > 0
               ), "Page size must be a positive integer"

        dataset = self.dataset()
        start, end = index_range(page, page_size)
        data = dataset[start:end]

        total_pages = math.ceil(len(dataset) / page_size)
        next_page = page + 1 if end < len(dataset) else None
        prev_page = page - 1 if start > 0 else None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }