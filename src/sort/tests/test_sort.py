"""
Usage: pytest /relative/path/to/test_sort.py
"""

import random
from sort import quicksort

def test_random():
    newList = [random.randint(-100, 100) for i in range(20)]
    quicksort.quicksort(newList, 0, len(newList) - 1)
    j = 0
    for (i, _) in enumerate(newList[1:], start=1):
        assert(newList[i] >= newList[j])
        j += 1