# test.py
# --------------
# This file is for testing purposes only
# Make sure to delete this later when the program works fully.

# CURRENTLY TESTING:
# -update from bs3 to bs4
# -finding Geronimo by Sheppard

import song

def test():
    print 'Running test now...'
    title = 'Geronimo'
    artist = 'Sheppard'
    s = song.Song(title, artist)
    if len(s.chord_sheets) == 0:
        print 'Song not found in our database.'
    else:
        print 'Song found! Yay!'

test()