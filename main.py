# main.py
# --------------
# This file executes the program.

import interface
import scrape
import song
import compare

def test():
    print 'Enter a song below:',
    song_info = interface.get_song_info()
    s1 = song.Song(song_info[0], song_info[1])
    while len(s1.chord_sheets) == 0:
        p
    print 'Enter a song below:',
    song_info = interface.get_song_info()
    s2 = song.Song(song_info[0], song_info[1])
    results = compare.run_test_suite(s1, s2, True)
    interface.print_results(results)

test()