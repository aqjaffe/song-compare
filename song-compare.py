# AUTHOR: Adam Jaffe
# UPDATED: 6.29.16
# ---------------------------------------------
# This program is my first experiment in web-scraping!
# It prompts the user for a song and artist and then collects
# relevant chord data from www.ultimate-guitar.com to compile
# a list of all of the user-generated chord sheets avaiable.
# It transposes these all to the same key for easy comparison.

import sys
import requests
import types
import Queue
import re
from BeautifulSoup import BeautifulSoup

edit_date = "6.29.16"

num_for_str = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3,
                'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8,
                'A':9, 'A#':10, 'Bb':10, 'B':11, 'H':11}

chords_in_key0 = {'0', '2m', '4m', '5', '7', '9m'}

max_n = 4;

test_suite = {'Uniform Weights': [False, False, [0.20, 0.20, 0.20, 0.20, 0.20]],
              'Distribution of Chords': [False, False, [1.0, 0, 0, 0, 0]],
              '3-Chord Progressions': [False, False, [0, 0, 1.0, 0, 0]],
              'All Chord Progressions': [False, False, [0, 0.25, 0.25, 0.25, 0.25]],
              'Intro Sequence':[True, False, [0, 0.4, 0.3, 0.2, 0.1]],
              'Outro Sequence':[False, True, [0, 0.25, 0.25, 0.25, 0.25]]}

# These variables define the aesthetics of the console program
num_digits = 5
total_length = 48

def print_intro():
    print_title('SONG COMPARATOR')
    print 'Welcome to the song comparator!'
    print 'Developed by Adam Jaffe'
    print 'Version updated ' + edit_date

def print_chars(char, num):
    for i in range(num):
        sys.stdout.write(char)

def print_title(text):
    #print the top line and |
    sys.stdout.write('+')
    print_chars('-', total_length - 2)
    sys.stdout.write('+\n|')
    #print the middle section, including text and |\n+
    num_spaces = (total_length - len(text) - 2) / 2
    print_chars(' ', num_spaces)
    sys.stdout.write(text)
    print_chars(' ', total_length - len(text) - num_spaces - 2)
    sys.stdout.write('|\n+')
    #print the bottom line
    print_chars('-', total_length - 2)
    sys.stdout.write('+\n')

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
        print_chars('.',total_length - num_digits - 1 - len(name))
        total += results[name]
        print str(100 * results[name])[0:num_digits] + '%'
    print '\tAverage Similarity: ' + str(100 * get_average_results(results))[:num_digits] + '%'

def print_ranking(ranking):
    print_title('BEST MATCHES')
    for i in range(len(ranking)):
        print '#' + str(i + 1) + '\t\"' + ranking[i][0] + '\" by ' + ranking[i][1] + ', and'
        print '\t\"' + ranking[i][2] + '\" by ' + ranking[i][3] + '\t' + str(ranking[i][4]) + '\n'

#TODO: make this reflect some weighting
def get_average_results(results):
    total = 0
    for name in results:
        total += results[name]
    return total / len(results)

def run_test_suite(song1, song2, printing):
    results = {}
    if printing:
        print_title('TEST SUITE RESULTS')
        print 'Song #1: \"' + song1[0] + '\" by ' + song1[1]
        print 'Song #2: \"' + song2[0] + '\" by ' + song2[1]
        print_chars('~', total_length)
        print
    for name in test_suite:
        results[name] = calc_song_difference(song1[2], song2[2], test_suite[name])
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

def window_to_str(window):
    output = ''
    for chord in list(window.queue):
        output += chord + ' '
    return output

def window_to_str(window):
    output = ''
    for chord in list(window.queue):
        output += chord + ' '
    return output

def convert_to_percentage(markov_table):
    for n in range(len(markov_table)):
        for progression in markov_table[n]:
            total = 0
            for chord in markov_table[n][progression]:
                total += markov_table[n][progression][chord]
            for chord in markov_table[n][progression]:
                markov_table[n][progression][chord] /= float(total)

def make_markov_table(all_chords, weights):
    markov_table = []
    for n in range(max_n + 1):
        n_grams = {}
        index = 0
        for chord_list in all_chords:
            if len(chord_list) < n:
                continue
            window = Queue.Queue()
            for i in range(n):
                window.put(chord_list[i])
            for i in range(len(chord_list) - n):
                window_str = window_to_str(window)
                if window_str in n_grams:
                    if chord_list[i + n] in n_grams[window_str]:
                        n_grams[window_str][chord_list[i + n]] += weights[index]
                    else:
                        n_grams[window_str][chord_list[i + n]] = weights[index]
                else:
                    n_grams[window_str] = {}
                    n_grams[window_str][chord_list[i + n]] = weights[index]
                # advance to the next window
                if not window.empty():
                    window.put(chord_list[i + n])
                    window.get()
            index += 1
        markov_table.append(n_grams)
    convert_to_percentage(markov_table)
    return markov_table

# Adds '-1' delimiters to mark the beginning and end of each sheet
def add_delimiters(chord_sheet):
    chord_sheet.insert(0, str(-1))
    chord_sheet.append(str(-1))
    return chord_sheet


# These functions are for transposing chord lists
# into the best possibly key for further processing
def transpose(chord_sheet, key):
    transposed_chord_sheet = []
    for chord in chord_sheet:
        if chord[len(chord) - 1] == 'm':
            chord = chord[:-1]
            transposed_chord = str((int(chord) + key) % 12) + 'm'
        else:
            transposed_chord = str((int(chord)+ key) % 12)
        transposed_chord_sheet.append(transposed_chord)
    return transposed_chord_sheet

def errors_for_key(chord_sheet, key):
    errors = 0
    chords_in_curr_key = transpose(chords_in_key0, key)
    for chord in chord_sheet:
        if chord not in chords_in_curr_key:
            errors += 1
    return errors

def get_best_key(chord_sheet):
    min_errors = sys.maxint
    best_key = -1
    for key in range(12):
        errors = errors_for_key(chord_sheet, key)
        if errors < min_errors:
            min_errors = errors
            best_key = key
    return best_key

def transpose_to_key0(chord_sheet):
    key = get_best_key(chord_sheet)
    return transpose(chord_sheet, -key)


# These functions are for translating between numerical
# and alphabetical chord symbols
def str_to_num(chord):
    chord_str = chord[0]
    next_char = 1;
    if len(chord) > 1 and (chord[1] == 'b' or chord[1] == '#'):
        chord_str += chord[1]
        next_char += 1
    output = str(num_for_str[chord_str])
    if len(chord) > next_char and chord[next_char] == 'm':
        output += chord[next_char]
    return output

def chords_to_nums(chord_sheet):
    num_sheet = []
    for chord in chord_sheet:
        num_sheet.append(str_to_num(chord))
    return num_sheet


# These functions are for scraping the internet
# for the chord lists
def get_chord_sheet(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    data = soup.find('pre', attrs={'class':'js-tab-content'})
    chord_sheet = []
    for chord in data.findAll('span'):
        chord_sheet.append(chord.string)
    rating_data = soup.find('div', attrs={'class':'raiting'})
    rating_value = float(rating_data.find('meta', attrs={'itemprop':'ratingValue'}).get('content'))
    rating_count = int(rating_data.find('span', attrs={'itemprop':'ratingCount'}).text.replace(',',''))
    output = [rating_value * rating_count, chord_sheet]
    return output

def get_song_info():
    title = raw_input("\tTitle: ")
    artist = raw_input("\t\tArtist: ")
    song_info = [title, artist]
    return song_info

# simplifies the string in such a way that it can be used in url's for searching
def simplify_str(text):
    return ' '.join(re.sub(r'([^\s\w]|_)', '', text).split())

#TODO: fix this part of the program
# I accidentally broke it by updating to BeautifulSoup4
# For now, I reverted back to bs3, but I need to figure out how to update eventually
def get_chord_sheet_urls(title, artist):
    url = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=' + simplify_str(title).replace(' ', '+')
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    url_data = [title, artist]
    search_results = soup.find('table', attrs={'class':'tresults'})
    if search_results is None:
        url_data.append(None)
        return url_data
    chord_sheet_urls = []
    collecting = False
    # TODO: make this read several pages, if necessary
    for row in search_results.findAll('tr'):
        cells = row.findAll('td')
        # TODO: why doesn't this work for Geronimo by Sheppard?
        # For some reason it only reads 2 'td' sections then stops, instead of reading all 4.
        # Uncomment the below line to see what I mean:
        #print cells
        if len(cells) != 4:
            continue
        if cells[0].text != '&nbsp;':
            if cells[0].text.strip().lower() == artist.lower():
                collecting = True
            else:
                collecting = False
        if collecting == True and len(cells[2].contents) > 0 and cells[3].text == 'chords':
            url = cells[1].a.get('href')
            chord_sheet_urls.append(url)
    if len(chord_sheet_urls) == 0:
        url_data.append(None)
        return url_data
    url_data.append(chord_sheet_urls)
    return url_data

def process_chords(raw_chord_sheet):
    return add_delimiters(transpose_to_key0(chords_to_nums(raw_chord_sheet)))

def make_song(title, artist):
    if title == '' and artist == '':
        song_info = get_song_info()
    else:
        song_info = []
        song_info.append(title)
        song_info.append(artist)
    url_data = get_chord_sheet_urls(song_info[0], song_info[1])
    song = [url_data[0], url_data[1]]
    if url_data[2] is None:
        song.append(None)
        return song
    chord_sheets = []
    weights = []
    for url in url_data[2]:
        sheet_data = get_chord_sheet(url)
        weights.append(sheet_data[0])
        raw_chord_sheet = sheet_data[1]
        processed_chord_sheet = process_chords(raw_chord_sheet)
        chord_sheets.append(processed_chord_sheet)
    song.append(make_markov_table(chord_sheets, weights))
    return song

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

def get_billboard_songs(year, max_num_songs):
    print_title('BILLBOARD TOP HITS')
    url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_' + str(year)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    results = soup.find('div', attrs={'id':'mw-content-text'}).table
    songs = []
    num = 0
    for row in results.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) < 2:
            continue
        title = cells[len(cells) - 2].text.replace('\"','')
        artist = cells[len(cells) - 1].a.text.replace('\"','')
        print '\"' + title + '\"' + ' by ' + artist + '...',
        song = make_song(title, artist)
        if song[2] is None:
            print 'NOT FOUND'
        else:
            print 'done'
        songs.append(song)
        num += 1
        if num >= max_num_songs:
            break
    return songs

def rank_song_pairs(songs, num_results):
    ranking = []
    for i in range(len(songs)):
        for j in range(len(songs) - i - 1):
            element = [songs[i][0], songs[i][1], songs[i + j + 1][0], songs[i + j + 1][1]]
            results = run_test_suite(songs[i], songs[i + j + 1], False)
            sim = get_average_results(results)
            element.append(sim)
            if len(ranking) < num_results:
                ranking.append(element)
                ranking.sort(key=lambda el: -el[4])
            elif sim > ranking[num_results - 1][4]:
                ranking.append(element)
                ranking.sort(key=lambda el: -el[4])
                ranking.pop()
    return ranking

def get_best_match(target_song, songs, num_results):
    ranking = []
    for i in range(len(songs)):
        element = [target_song[0], target_song[1], songs[i][0], songs[i][1]]
        results = run_test_suite(songs[i], target_song, False)
        sim = get_average_results(results)
        element.append(sim)
        if len(ranking) < num_results:
            ranking.append(element)
            ranking.sort(key=lambda el: -el[4])
        elif sim > ranking[num_results - 1][4]:
            ranking.append(element)
            ranking.sort(key=lambda el: -el[4])
            ranking.pop()
    return ranking

# This function executes the program
#TODO: decompose better, in general
def main():
    print_intro()
    feature = get_feature()
    while(feature != 0):
        if feature == 1:
            songs = get_song_pair()
            results = run_test_suite(songs[0], songs[1], True)
            print_results(results)
        elif feature == 2:
            print 'Sorry, this feature is not yet implemented'
        elif feature == 3:
            print_title('SONG RETRIEVAL')
            print 'What song would you like to check?\n\t',
            target_song = make_song('','')
            year = raw_input('What year would you like to explore? ')
            max_num_songs = raw_input('How many songs would you like to examine? ')
            num_results = raw_input('How many results would you like to display? ')
            songs = get_billboard_songs(year, int(max_num_songs))
            ranking = get_best_match(target_song, songs, int(num_results))
            print_ranking(ranking)
        elif feature == 4:
            year = raw_input('What year would you like to explore? ')
            max_num_songs = raw_input('How many songs would you like to examine? ')
            num_results = raw_input('How many results would you like to display? ')
            songs = get_billboard_songs(year, int(max_num_songs))
            ranking = rank_song_pairs(songs, int(num_results))
            print_ranking(ranking)
        else:
            print 'ERROR: feature not found'
        feature = get_feature()
    print 'Thank you for running song-compare.py'

main()
