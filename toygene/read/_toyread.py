from typing import Dict, List, Optional, Tuple

from attr import attrs, attrib
from cached_property import cached_property
from samwell.sam import AlignedSegment
from toyplot.coordinates import Cartesian
from toyplot import Canvas
from toyplot.mark import Mark

from toygene.segment_util import (
    AlignedSegmentPair,
    FragmentOrPair,
    partition,
    segments_in_disjoint_bins,
)
from toygene.read._style import ToyReadStyle


class ToyReadMark(Mark):
    def __init__(self, reads: List[FragmentOrPair]) -> None:
        Mark.__init__(self)
        self.reads = list(reads)


@attrs(auto_attribs=True, frozen=True, repr=False)
class ToyRead(object):
    reads: List[FragmentOrPair] = attrib(converter=list)
    pairs: List[AlignedSegmentPair] = attrib(init=False)
    fragments: List[AlignedSegment] = attrib(init=False)

    def __attrs_post_init__(self) -> None:
        pairs, fragments = partition(self.reads)
        object.__setattr__(self, "fragments", fragments)
        object.__setattr__(self, "pairs", pairs)

    def __len__(self) -> int:
        return len(self.reads)

    @property
    def height(self) -> int:
        return len(self.segments_in_disjoint_bins)

    @cached_property
    def segments_in_disjoint_bins(self) -> Dict[int, List[AlignedSegment]]:
        return segments_in_disjoint_bins(self.reads)

    def draw(
        self, style: Optional[ToyReadStyle] = None, axes: Optional[Cartesian] = None,
    ) -> Tuple[Canvas, Cartesian, ToyReadMark]:
        style = style if style is not None else ToyReadStyle()
        height = self.height if style.height is None else style.height
        width = len(self) if style.width is None else style.width
        canvas = Canvas(height=height, width=width)
        axes = canvas.cartesian(padding=style.padding, ymin=0, ymax=self.height, xmin=-0.5, xmax=150.5)
        mark = ToyReadMark(self.reads)
        axes.add_mark(mark)
        return canvas, axes, mark

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__qualname__} with "
            f"{len(self.fragments)} fragments and "
            f"{len(self.pairs)} paired segments>"
        )
