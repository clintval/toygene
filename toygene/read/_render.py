import xml.etree.ElementTree as xml
from more_itertools import flatten
from multipledispatch import dispatch
from toyplot.coordinates import Cartesian
from toyplot.html import RenderContext, _draw_rect
from toyplot.html import _namespace as _toyplot_namespace

# from toygene.segment_util import to_interval
from toygene.read._toyread import ToyReadMark


class RenderToyRead(object):
    """A :class:`toygene.read.ToyRead` renderer."""

    def __init__(self, axes: Cartesian, mark: ToyReadMark, context: RenderContext) -> None:
        self.mark = mark
        self.axes = axes
        self.context = context

        self.mark_xml = xml.SubElement(
            self.context.parent,
            "g",
            id=self.context.get_id(self.mark),
            attrib={"class": "toyread-mark-Pileup"},
        )
        self.squares_xml = xml.SubElement(self.mark_xml, "g", attrib={"class": "toyread-Squares"})
        self.mark_squares()

    def mark_squares(self) -> None:  # TODO: project into SVG coordinates.
        for i, read in enumerate(flatten(self.mark.reads)):
            # interval = to_interval(read)
            attrib = dict(id=f"square-{i}-{read.query_name}")
            marker_xml = xml.SubElement(self.squares_xml, "g", attrib=attrib)
            # marker_xml.set('transform', f'translate({300:3f} {40})')
            _draw_rect(marker_xml, 20, width=10, height=10, angle=0)
            # _draw_read(marker_xml, 12, 10)
            # print(marker_xml.items())


@dispatch(Cartesian, ToyReadMark, RenderContext, namespace=_toyplot_namespace)
def _render(axes: Cartesian, mark: ToyReadMark, context: RenderContext) -> None:
    RenderToyRead(axes, mark, context)
