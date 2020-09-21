from collections import defaultdict
from more_itertools import first_true
from typing import Dict, List

from samwell.overlap_detector import Interval, OverlapDetector


def disjoint_bins(intervals: List[Interval]) -> Dict[int, List[int]]:
    bins: Dict[int, List[int]] = defaultdict(list)
    detectors: Dict[int, OverlapDetector] = defaultdict(OverlapDetector)
    for i, interval in enumerate(intervals):
        tier = (
            0
            if not bins
            else first_true(
                iterable=bins,
                pred=lambda tier: not detectors[tier].overlaps_any(interval),
                default=max(bins) + 1,
            )
        )
        bins[tier].append(i)
        detectors[tier].add(interval)
    return dict(bins)
