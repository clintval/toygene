from more_itertools import flatten, interleave_longest
from pytest import raises
from samwell.overlap_detector import Interval
from samwell.sam import AlignedSegment
from samwell.sam.sambuilder import SamBuilder

from toygene.segment_util import partition, segments_in_disjoint_bins, to_interval


class TestSegmentUtil(object):
    """Tests for :class:`toygene.segment_util`."""

    def test_partition(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=200)
        pair2 = builder.add_pair(chrom="chr1", start1=50, start2=250)
        pair3 = builder.add_pair(chrom="chr1", start1=400, start2=500)

        expected_pairs = [pair1, pair2, pair3]
        expected_fragments = list(flatten(expected_pairs))
        reads = interleave_longest(expected_pairs, expected_fragments)
        actual_pairs, actual_fragments = partition(reads)

        assert actual_fragments == expected_fragments
        assert actual_pairs == expected_pairs

    def test_to_interval(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        unmapped1, unmapped2 = builder.add_pair()
        read1, read2 = builder.add_pair(name="read1", chrom="chr1", start1=100, start2=200)
        expected1 = Interval("chr1", 100, 150, negative=False, name="read1")
        expected2 = Interval("chr1", 200, 250, negative=True, name="read1")

        assert to_interval(read1) == expected1
        assert to_interval(read2) == expected2

        with raises(ValueError):
            to_interval(unmapped1)
        with raises(ValueError):
            to_interval(unmapped2)

    def test_segments_in_disjoint_bins_empty(self):
        bins = segments_in_disjoint_bins([])
        assert bins == {}

    def test_segments_in_disjoint_bins_without_overlapping(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=200)
        pair2 = builder.add_pair(chrom="chr1", start1=300, start2=400)
        bins = segments_in_disjoint_bins([pair1, pair2])
        assert bins == {
            0: [*pair1, *pair2],
        }

    def test_segments_in_disjoint_bins_with_overlapping(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=200)
        pair2 = builder.add_pair(chrom="chr1", start1=125, start2=225)
        pair3 = builder.add_pair(chrom="chr1", start1=300, start2=400)
        bins = segments_in_disjoint_bins([pair1, pair2, pair3])
        assert bins == {0: [*pair1, *pair3], 1: [*pair2]}

    def test_segments_in_disjoint_bins_with_overlapping_reverse(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=200)
        pair2 = builder.add_pair(chrom="chr1", start1=125, start2=225)
        pair3 = builder.add_pair(chrom="chr1", start1=300, start2=400)
        bins = segments_in_disjoint_bins([pair3, pair2, pair1])
        assert bins == {0: [*pair3, *pair2], 1: [*pair1]}

    def test_segments_in_disjoint_bins_point_intervals(self):
        builder = SamBuilder(r1_len=1, r2_len=1)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=200)
        pair2 = builder.add_pair(chrom="chr1", start1=101, start2=201)
        bins = segments_in_disjoint_bins([pair1, pair2])
        assert bins == {0: [*pair1, *pair2]}

    def test_segments_in_disjoint_bins_template_within_template(self):
        builder = SamBuilder(r1_len=50, r2_len=50)
        pair1 = builder.add_pair(chrom="chr1", start1=100, start2=400)
        pair2 = builder.add_pair(chrom="chr1", start1=200, start2=300)
        bins = segments_in_disjoint_bins([pair1, pair2])
        assert bins == {0: [*pair1, *pair2]}
