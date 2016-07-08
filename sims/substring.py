# substring.py
# --------------------
# this method computes the length of the
# longest substring common to both songs

# find longest common substring
# and return its length, divided by the length
# of the shorter of the two chord sheets

from __future__ import division

# what value should this exponent be?
scale_factor = 1.0

# this code is taken from the wikibooks page
# on longest common substring
def lcss(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def lcss_ratio(str1, str2):
    denom = min(len(str1), len(str2))
    ss = len(lcss(str1, str2))
    return ss / denom

def sim(song1, song2):
    avg = 0.0
    for i in range(len(song1.chord_sheets)):
        for j in range(len(song2.chord_sheets)):
            avg += lcss_ratio(song1.chord_sheets[i], song2.chord_sheets[j]) * song1.weights[i] * song2.weights[j]
    return avg ** scale_factor