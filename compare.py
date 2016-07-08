# compare.py
# ---------------------
# This file contains the methods used for comparing songs

from userIO import interface

# These are the similarity methods
from sims import stochastic, substring, subsequence, levenshtein

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
    results['Stochastic'] = stochastic.sim(song1, song2)
    results['Substring'] = substring.sim(song1, song2)
    results['Subsequence'] = subsequence.sim(song1, song2)
    results['Levenshtein'] = levenshtein.sim(song1, song2)
    results['Average'] = get_average_results(results)
    return results