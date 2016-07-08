# song.py
# ------------
# This file defines the song class

import music
from userIO import scrape, interface

class Song(object):
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        chord_sheet_urls = scrape.get_chord_sheet_urls(scrape.simplify_str(title), self.artist)
        sheets = scrape.urls_to_sheets(chord_sheet_urls)
        self.chord_sheets = sheets[0]
        self.weights = sheets[1]
    
    def __str__(self):
        return '\"' + self.title + '\" by ' + self.artist