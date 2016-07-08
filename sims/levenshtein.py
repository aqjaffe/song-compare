# levensthein.py
# -----------------------
# This file computes the levenshtein distance
# between two chord sheets

from __future__ import division

def lev(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

def lev_ratio(seq1, seq2):
    max_len = max(len(seq1), len(seq2))
    return (max_len - lev(seq1, seq2)) / max_len

def sim(song1, song2):
    total = 0.0
    for chord_sheet1 in song1.chord_sheets:
        for chord_sheet2 in song2.chord_sheets:
            total += lev_ratio(chord_sheet1, chord_sheet2)
    return total / (len(song1.chord_sheets) * len(song2.chord_sheets))