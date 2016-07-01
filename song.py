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
        
        self.chord_sheets = []
        self.weights = []
        
        chord_sheet_urls = scrape.get_chord_sheet_urls(self.title_url, self.artist)
        for url in chord_sheet_urls:
            sheet_data = scrape.get_chord_sheet(url)
            self.weights.append(sheet_data[0])
            raw_chord_sheet = sheet_data[1]
            processed_chord_sheet = music.process_chords(raw_chord_sheet)
            self.chord_sheets.append(processed_chord_sheet)
        self.markov_table = markov.make_markov_table(self.chord_sheets, self.weights)
    
    def __str__(self):
        return '\"' + self.title + '\" by ' + self.artist
