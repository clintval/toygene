from typing import Dict, Iterable, Iterator, List, Tuple, Union

from more_itertools import flatten
from more_itertools import partition as _partition
from samwell.sam import AlignedSegment
from samwell.overlap_detector import Interval
from toygene.interval_util import disjoint_bins

AlignedSegmentPair = Tuple[AlignedSegment, AlignedSegment]
FragmentOrPair = Union[AlignedSegment, AlignedSegmentPair]


def partition(
    iterable: Iterable[FragmentOrPair],
) -> Tuple[List[AlignedSegmentPair], List[AlignedSegment]]:
    pairs: Iterator[AlignedSegmentPair]
    fragments: Iterator[AlignedSegment]
    pairs, fragments = _partition(lambda i: isinstance(i, AlignedSegment), iterable)
    return list(pairs), list(fragments)


def to_interval(segment: AlignedSegment) -> Interval:
    if segment.is_unmapped:
        raise ValueError(f"Segment must be mapped, found: {segment}")
    return Interval(
        refname=segment.reference_name,
        start=segment.pos,
        end=segment.pos + segment.alen,
        negative=segment.is_reverse,
        name=segment.query_name,
    )


def segments_in_disjoint_bins(
    iterable: Iterable[FragmentOrPair],
) -> Dict[int, List[AlignedSegment]]:
    reads = [read for read in flatten(iterable) if not read.is_unmapped]
    bins = disjoint_bins([to_interval(read) for read in reads])
    return {tier: [reads[i] for i in indexes] for tier, indexes in bins.items()}
