#!/usr/bin/env python3
"""tuple of size two containing a start index and an end index"""

import csv
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
    """ class init with dataset"""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """arguments are integers greater than 0"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Page must be a positive integer"""
        assert (
    isinstance(page, int) and page > 0
              ), "Page must be a positive integer"
        assert (
    isinstance(page_size, int) and page_size > 0
               ), "Page size must be a positive integer"

        dataset = self.dataset()
        start, end = index_range(page, page_size)
        return dataset[start:end]
