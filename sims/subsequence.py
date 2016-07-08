# subsequence.py
# ----------------
# Computes the longest common subsequence
# instead of the longest common substring

from __future__ import division

# what value should this exponent be?
scale_factor = 1.0

def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

def backTrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ''
    elif X[i-1] == Y[j-1]:
        return backTrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)

scale_factor = 1.0

def ratio(str1, str2):
    denom = min(len(str1), len(str2))
    ss = len(backTrack(LCS(str1, str2), str1, str2, len(str1), len(str2)))
    return ss / denom

def sim(song1, song2):
    avg = 0.0
    for i in range(len(song1.chord_sheets)):
        for j in range(len(song2.chord_sheets)):
            avg += ratio(song1.chord_sheets[i], song2.chord_sheets[j]) * song1.weights[i] * song2.weights[j]
    return avg ** scale_factor