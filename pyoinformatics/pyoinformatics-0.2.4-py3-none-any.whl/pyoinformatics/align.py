from .seq import Seq


def lcs_matrix(seq1: Seq, seq2: Seq):
    w, h = len(seq1), len(seq2)

    Matrix = [[0 for x in range(w + 1)] for y in range(h + 1)]

    for i, ibase in enumerate(seq1, 1):
        for j, jbase in enumerate(seq2, 1):
            if ibase == jbase:
                Matrix[j][i] = Matrix[j - 1][i - 1] + 1
            else:
                Matrix[j][i] = max(Matrix[j - 1][i], Matrix[j][i - 1])

    # remove zeros
    Matrix = [M[1:] for M in Matrix[1:]]

    return Matrix


def format_lcs_matrix(seq1, seq2, Matrix):
    fM = []
    fM.append("  " + " ".join([nt for nt in seq1]))
    for i, b in enumerate(seq2):
        fM.append(b + " " + " ".join([str(s) for s in Matrix[i]]))
    return fM


def lcs_traceback(seq1: Seq, seq2: Seq, Matrix):
    i, j = len(seq1) - 1, len(seq2) - 1
    LCS = []
    pos_seq1 = []
    pos_seq2 = []
    while i > -1 and j > -1:
        if seq1[i] == seq2[j]:
            LCS.append(seq1[i])
            pos_seq1.append(i + 1)
            pos_seq2.append(j + 1)
            j -= 1
            i -= 1
        elif Matrix[j][i - 1] == Matrix[j][i]:
            i -= 1
        elif Matrix[j - 1][i] == Matrix[j][i]:
            j -= 1
    LCS = "".join(LCS)[::-1]
    return Seq(LCS), pos_seq1[::-1], pos_seq2[::-1]


def lcs(seq1: Seq, seq2: Seq) -> Seq:
    """longest common subsequence of two sequences"""
    Matrix = lcs_matrix(seq1, seq2)
    LCS, *_ = lcs_traceback(seq1, seq2, Matrix)
    return LCS
