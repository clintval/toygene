from samwell.overlap_detector import Interval
from samwell.sam.sambuilder import SamBuilder

from toygene.interval_util import disjoint_bins


class TestIntervalUtil(object):
    """Tests for :class:`toygene.interval_util`."""

    def test_disjoint_bins_empty(self):
        bins = disjoint_bins([])
        assert bins == {}

    def test_disjoint_bins_without_overlapping(self):
        interval1 = Interval("chr1", 100, 200)
        interval2 = Interval("chr1", 300, 400)
        bins = disjoint_bins([interval1, interval2])
        assert bins == {
            0: [0, 1],
        }

    def test_disjoint_bins_with_overlapping(self):
        interval1 = Interval("chr1", 100, 200)
        interval2 = Interval("chr1", 150, 250)
        interval3 = Interval("chr1", 300, 400)
        bins = disjoint_bins([interval1, interval2, interval3])
        assert bins == {
            0: [0, 2],
            1: [1],
        }

    def test_disjoint_bins_with_overlapping_reverse(self):
        interval1 = Interval("chr1", 100, 200)
        interval2 = Interval("chr1", 150, 250)
        interval3 = Interval("chr1", 300, 400)
        bins = disjoint_bins([interval3, interval2, interval1])
        assert bins == {
            0: [0, 1],
            1: [2],
        }

    def test_disjoint_bins_point_intervals(self):
        interval1 = Interval("chr1", 1, 2)
        interval2 = Interval("chr1", 2, 3)
        bins = disjoint_bins([interval1, interval2])
        assert bins == {
            0: [0, 1],
        }
