from pyoinformatics.align import lcs, format_lcs_matrix
from pyoinformatics.seq import Seq


def test_lcs():
    assert lcs(Seq("AACCTTGG"), Seq("ACACTGTGA")) == Seq("AACTTG")


def test_format_lcs_matrix():
    Seq1 = Seq("AACCTTGG")
    Seq2 = Seq("ACACTGTGA")

    M = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 2, 2, 2, 2, 2],
        [1, 2, 2, 2, 2, 2, 2, 2],
        [1, 2, 3, 3, 3, 3, 3, 3],
        [1, 2, 3, 3, 4, 4, 4, 4],
        [1, 2, 3, 3, 4, 4, 5, 5],
        [1, 2, 3, 3, 4, 5, 5, 5],
        [1, 2, 3, 3, 4, 5, 6, 6],
        [1, 2, 3, 3, 4, 5, 6, 6],
    ]

    assert format_lcs_matrix(Seq1, Seq2, M) == [
        "  A A C C T T G G",
        "A 1 1 1 1 1 1 1 1",
        "C 1 1 2 2 2 2 2 2",
        "A 1 2 2 2 2 2 2 2",
        "C 1 2 3 3 3 3 3 3",
        "T 1 2 3 3 4 4 4 4",
        "G 1 2 3 3 4 4 5 5",
        "T 1 2 3 3 4 5 5 5",
        "G 1 2 3 3 4 5 6 6",
        "A 1 2 3 3 4 5 6 6",
    ]
