# interface.py
# ----------------------------------------------------
# This module is for reading user input to the program

import interface
import song

def get_feature():
    print 'What feature would you like to run?'
    print ' (1) Compare two songs of your choice'
    print ' (2) Compare all songs by one artist'
    print ' (3) Compare one song to the billboard top hits'
    print ' (4) Compare all songs on the billboard top hits'
    print ' (5) Compare all songs from a .txt file'
    feature = raw_input('Enter a feature to run (or 0 to quit): ')
    return int(feature)

def get_song_info():
    title = raw_input(" Title: ")
    artist = raw_input(" Artist: ")
    return [title, artist]

def get_song():
    song_info = get_song_info()
    output = song.Song(song_info[0], song_info[1])
    while len(output.chord_sheets) == 0:
        print 'Song not found in our database. Please try another:'
        song_info = get_song_info()
        output = song.Song(song_info[0], song_info[1])
    return output

def get_song_pair():
    print 'Enter a song below:'
    s1 = get_song()
    print 'Enter another song here:'
    s2 = get_song()
    return [s1, s2]

def get_song_comparable():
    print 'What song would you like to compare?'
    song = get_song()
    return song

# TODO: add robustness here for the integer parsing section
def get_num_results():
    num_results = raw_input('How many results would you like to display? ')
    return int(num_results)

# TODO: and here
def get_billboard_info():
    year = raw_input('What year would you like to explore? ')
    max_num_songs = raw_input('How many songs would you like to examine? ')
    num_results = get_num_results()
    return [year, int(max_num_songs), num_results]

def get_songs_from_file():
    file_name = raw_input('What file would you like to open? ')
    f = open(file_name, 'r')
    songs = []
    for line in f:
        splitting_index = 1 + line[1:].index('\"')
        title = line[1:splitting_index]
        artist = line[splitting_index + 2:-1]        
        print '\"' + title + '\" by ' + artist + '...',
        s = song.Song(title, artist)
        if len(s.chord_sheets) == 0:
            print 'NOT FOUND'
        else:
            print 'done'
            songs.append(s)
    f.close()
    return songs