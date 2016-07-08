# test.py
# --------------
# This file is for testing purposes only
# Make sure to delete this later when the program works fully.

# CURRENTLY TESTING:
# -update from bs3 to bs4
# -finding Geronimo by Sheppard

import song
import compare
from userIO import interface

def test():
    s1 = song.Song('Under Pressure', 'David Bowie')
    s1.chord_sheets[0] = ['-1', 'a', 'b', 'c', '-1']
    s2 = song.Song('Under Pressure', 'Queen')
    s2.chord_sheets[0] = ['-1', 'a', 'b', 'c', '-1']
    results = compare.run_test_suite(s1, s2, True)
    interface.print_results(results)

test()