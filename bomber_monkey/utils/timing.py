import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass

import numpy as np


@dataclass
class TimeEntry:
    name: str


_TIMES = defaultdict(list)

_ACTIVE = False


@contextmanager
def timing(name: str):
    if not _ACTIVE:
        yield
    else:
        start = time.time()
        yield
        total = time.time() - start
        _TIMES[name].append(total)


def show_timing():
    try:
        if _ACTIVE:
            from tabulate import tabulate
            from numpy import average

            def compute_line(key, values):
                total_time = sum(values)
                if len(values) == 1:
                    return [key, total_time, len(values), None, None, None, None]
                return [key, total_time, len(values), min(values), max(values), np.mean(values), np.std(values)]

            print(tabulate(
                headers=['label', 'total (s)', 'count', 'min', 'max', 'mean', 'std'],
                floatfmt='.5f',
                tabular_data=sorted([
                    compute_line(key, values)
                    for key, values in _TIMES.items()
                ], key=lambda row: row[1], reverse=True),
            ))
    except Exception as e:
        print(e)


def setup_timing(status: bool = True):
    global _ACTIVE
    _ACTIVE = status


if __name__ == '__main__':
    setup_timing()
    with timing('toto'):
        time.sleep(.2)
    show_timing()
