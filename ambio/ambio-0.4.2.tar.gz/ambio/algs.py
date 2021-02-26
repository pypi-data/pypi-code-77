"""
A collection of Bioinformatics Algorithms, mainly involving strings.

Features the most famous and useful algorithms used for matching and analizing DNA sequences.


Functions
---------

hammingDistance()
    Calculates the Hamming distance between two strings. 

alignmentScoreTable()
    Generates the table of scores for finding the alignment score with the Needleman-Wunsch algorithm.

alignmentScore()
    Calculates the alignment score of two strings with the Needleman–Wunsch algorithm.

showAlignment()
    Returns a visual representation of the alignment of two given strings using the Needleman–Wunsch algorithm.
"""


def hammingDistance(
    string1,
    string2
):
    """
    Calculates the Hamming distance between two strings.

    Args:
        string1 (str): The first string.
        string2 (str): The second string.

    Raises:
        ValueError: If the two strings are not the same length.

    Returns:
        distance (int): The Hamming distance between `string1` and `string2`.
    """

    if len(string1) != len(string2):
        raise ValueError("The two given strings are not the same length.")

    dist = 0
    for i in range(len(string1)):
        if string1[i] != string2[i]:
            dist += 1

    return dist


def alignmentScoreTable(
        string1,
        string2,
        paths=False,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """
    Generates the table of scores needed for finding the alignment score with the Needleman-Wunsch algorithm.

    Args:
        string1 (str): The first string to align.
        string2 (str): The second string to align.
        paths (bool): When True the table used for backtracking is also returned.
        insertionDeletionWeight (int): The cost of an insertion or deletion, default is -2.
        substitutionWeight (int): The cost of a substitution, default is -1.
        matchWeight (int): The profit of a matching character, default is 1.

    Returns:
        table (list): A matrix containing the alignment scores, and optionally another matrix with the origin cells.
    """

    tab = [[0 for i in range(len(string1) + 1)]
           for j in range(len(string2) + 1)]

    prevsTab = [[(-1, -1) for i in range(len(string1) + 1)]
                for j in range(len(string2) + 1)]

    string1 = "-" + string1
    string2 = "-" + string2

    for j in range(len(string2)):

        for i in range(len(string1)):

            choose = []
            prevs = []

            if j > 0:
                choose.append(tab[j-1][i] + insertionDeletionWeight)
                prevs.append((j-1, i))

            if i > 0:
                choose.append(tab[j][i-1] + insertionDeletionWeight)
                prevs.append((j, i-1))

            if j > 0 and i > 0:
                if string1[i] == string2[j]:
                    choose.append(tab[j-1][i-1] + matchWeight)
                else:
                    choose.append(tab[j-1][i-1] + substitutionWeight)
                prevs.append((j-1, i-1))

            if len(choose) > 0:
                tab[j][i] = max(choose)
                prevsTab[j][i] = prevs[choose.index(max(choose))]

    if paths:
        return tab, prevsTab
    else:
        return tab


def alignmentScore(
        string1,
        string2,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """
    Calculate the alignment score of two given strings using the Needleman–Wunsch algorithm.

    Args:
        string1 (str): The first string to align.
        string2 (str): The second string to align.
        paths (bool): When True the table used for backtracking is also returned.
        insertionDeletionWeight (int): The cost of an insertion or deletion, default is -2.
        substitutionWeight (int): The cost of a substitution, default is -1.
        matchWeight (int): The profit of a matching character, default is 1.

    Returns:
        table (list): A matrix containing the alignment scores, and optionally another matrix with the origin cells.
    """

    table = alignmentScoreTable(
        string1, string2, False, insertionDeletionWeight, substitutionWeight, matchWeight)

    return table[-1][-1]


def showAlignment(
        string1,
        string2,
        insertionDeletionWeight=-2,
        substitutionWeight=-1,
        matchWeight=1
):
    """
    Returns a visual representation of the alignment of two given strings using the Needleman–Wunsch algorithm.

    Args:
        string1 (str): The first string to align.
        string2 (str): The second string to align.
        insertionDeletionWeight (int): The cost of an insertion or deletion, default is -2.
        substitutionWeight (int): The cost of a substitution, default is -1.
        matchWeight (int): The profit of a matching character, default is 1.

    Returns:
        aligned_strings (list): A list containing the two strings modified to show which edits have been made for them to be aligned.
    """

    _, track = alignmentScoreTable(
        string1, string2, True, insertionDeletionWeight, substitutionWeight, matchWeight)

    edited1 = edited2 = ""
    j = len(string2)
    i = len(string1)

    while i != 0 and j != 0:

        prev_j, prev_i = track[j][i]

        # diagonal move
        if prev_j == j-1 and prev_i == i-1:
            edited1 = string1[i-1] + edited1
            edited2 = string2[j-1] + edited2
        # vertical move
        elif prev_j == j-1:
            edited1 = "-" + edited1
            edited2 = string2[j-1] + edited2
        # horizontal move
        else:
            edited1 = string1[i-1] + edited1
            edited2 = "-" + edited2

        j = prev_j
        i = prev_i

    return [edited1, edited2]
