# interface.py
# ----------------------------------------------------
# This module is for printing the song-compare program
# to the console.

import sys
import compare

edit_date = "6.29.16"

num_percent_digits = 5
total_length = 48

def print_chars(char, num):
    for i in range(num):
        sys.stdout.write(char)

def print_title(text):
    sys.stdout.write('+')
    print_chars('-', total_length - 2)
    sys.stdout.write('+\n|')
    num_spaces = (total_length - len(text) - 2) / 2
    print_chars(' ', num_spaces)
    sys.stdout.write(text)
    print_chars(' ', total_length - len(text) - num_spaces - 2)
    sys.stdout.write('|\n+')
    print_chars('-', total_length - 2)
    sys.stdout.write('+\n')

def print_intro():
    print_title('SONG COMPARATOR')
    print 'Welcome to the song comparator!'
    print 'Developed by Adam Jaffe'
    print 'Version updated ' + edit_date

def print_markov_table(markov_table):
    for n in range(len(markov_table)):
        for progression in markov_table[n]:
            print progression
            for chord in markov_table[n][progression]:
                print '\t' + str(chord) + ' ' + str(markov_table[n][progression][chord])

def print_results(results):
    total = 0
    for name in results:
        sys.stdout.write(name)
        print_chars('.',total_length - num_percent_digits - 1 - len(name))
        total += results[name]
        print str(100 * results[name])[0:num_percent_digits] + '%'
    print '\tAverage Similarity: ' + str(100 * compare.get_average_results(results))[:num_percent_digits] + '%'

def print_ranking(ranking):
    print_title('BEST MATCHES')
    for i in range(len(ranking)):
        print '#' + str(i + 1) + '\t\"' + ranking[i][0] + '\" by ' + ranking[i][1] + ', and'
        print '\t\"' + ranking[i][2] + '\" by ' + ranking[i][3] + '\t' + str(ranking[i][4]) + '\n'

def get_song_info():
    title = raw_input("\tTitle: ")
    artist = raw_input("\t\tArtist: ")
    song_info = [title, artist]
    return song_info

def get_song_pair():
    print_title('SONG RETRIEVAL')
    print 'Song #1:',
    song1 = make_song('','')
    while song1[2] is None:
        print 'Song could not be found in database, please try another'
        print 'Song #1:',
        song1 = make_song('','')
    print '\nSong #2:',
    song2 = make_song('','')
    while song2[2] is None:
        print 'Song could not be found in database, please try another'
        print 'Song #2:',
        song2 = make_song('','')
    return [song1, song2]

def get_feature():
    print 'What feature would you like to run?'
    print ' (1) Compare two songs of your choice'
    print ' (2) Compare all songs by one artist'
    print ' (3) Compare one song to the billboard top hits'
    print ' (4) Compare all songs on the billboard top hits'
    feature = raw_input('Enter a feature to run (or 0 to quit): ')
    return int(feature)