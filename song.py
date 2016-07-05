# song.py
# ------------
# This file defines the song class

# the song class will contain the song's
# -title
# -artist
# -chord sheet list
# -markov table

import scrape
import music
import markov
import interface

class Song(object):
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.title_url = scrape.simplify_str(title) 
        chord_sheet_urls = scrape.get_chord_sheet_urls(self.title_url, self.artist)
        sheets = scrape.urls_to_sheets(chord_sheet_urls)
        self.chord_sheets = sheets[0]
        self.weights = sheets[1]
        self.markov_table = markov.make_markov_table(self.chord_sheets, self.weights)
    
    def __str__(self):
        return '\"' + self.title + '\" by ' + self.artist
