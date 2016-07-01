# compare.py
# ---------------------
# This file contains the methods used for comparing songs

import interface

test_suite = {'Uniform Weights': [False, False, [0.20, 0.20, 0.20, 0.20, 0.20]],
              'Distribution of Chords': [False, False, [1.0, 0, 0, 0, 0]],
              '3-Chord Progressions': [False, False, [0, 0, 1.0, 0, 0]],
              'All Chord Progressions': [False, False, [0, 0.25, 0.25, 0.25, 0.25]],
              'Intro Sequence':[True, False, [0, 0.4, 0.3, 0.2, 0.1]],
              'Outro Sequence':[False, True, [0, 0.25, 0.25, 0.25, 0.25]]}

#TODO: make this reflect some weighting
def get_average_results(results):
    total = 0
    for name in results:
        total += results[name]
    return total / len(results)

def run_test_suite(song1, song2, printing):
    results = {}
    if printing:
        interface.print_title('TEST SUITE RESULTS')
        print 'Song #1: ' + str(song1)
        print 'Song #2: ' + str(song2)
        interface.print_chars('~', interface.total_length)
        print
    for name in test_suite:
        results[name] = calc_song_difference(song1.markov_table, song2.markov_table, test_suite[name])
    return results

def calc_song_difference(song1, song2, specs):
    if song1 is None or song2 is None:
        return 0.0
    total_error = 0
    weights = specs[2]
    for n in range(len(song1)):
        n_error = 0
        count = 0
        for progression in song1[n]:
            if progression not in song2[n]:
                continue
            if specs[0] and (len(progression) < 2 or progression[:2] == '-1'):
                continue
            if specs[1] and (len(progression) < 2 or progression[-2:] == '-1'):
                continue
            error = bhattacharyya(song1[n][progression], song2[n][progression])
            n_error += error
            count += 1
        if count != 0:
            total_error += weights[n] * n_error / count
    return total_error

def bhattacharyya(pdf1, pdf2):
    bc = 0
    for chord in pdf1:
        if chord in pdf2:
            bc += (pdf1[chord] * pdf2[chord]) ** (0.5)
    return bc ** (0.5)