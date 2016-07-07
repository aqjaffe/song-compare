# scrape.py
# ----------------
# This program contains the methods for scraping
# www.ultimate-guitar.com to find chord sheets for each song

import requests
import types
import Queue
import re
import music
from bs4 import BeautifulSoup
import interface
import song

def get_chord_sheet(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find('pre', attrs={'class':'js-tab-content'})
    chord_sheet = []
    for chord in data.findAll('span'):
        chord_sheet.append(chord.string)
    rating_data = soup.find('div', attrs={'class':'raiting'})
    rating_value = float(rating_data.find('meta', attrs={'itemprop':'ratingValue'}).get('content'))
    rating_count = int(rating_data.find('span', attrs={'itemprop':'ratingCount'}).text.replace(',',''))
    output = [rating_value * rating_count, chord_sheet]
    return output

# simplifies the string in such a way that it can be used in url's for searching
def simplify_str(text):
    return ' '.join(re.sub(r'([^\s\w]|_)', '', text).split())

def get_chord_sheet_urls(title_url, artist):
    url = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=' + title_url.replace(' ', '+')
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    chord_sheet_urls = []
    search_results = soup.find('table', {'class' : 'tresults'})
    #print search_results.prettify()
    if search_results is None:
        return [] #is this the right return value?
    collecting = False
    # TODO: make this read several pages, if necessary
    for row in search_results.findAll('tr'):
        cells = row.findAll('td')
        #print cells
        if len(cells) < 4:
            continue
        if cells[0].text != u'\xa0':
            if cells[0].text.strip().lower() == artist.lower():
                collecting = True
            else:
                collecting = False
        if collecting == True and len(cells[2].contents) > 0 and cells[3].text == 'chords': # what does the cells[2] condition check???
            url = cells[1].a.get('href')                                                    # the program crashes when I remove it, but
            chord_sheet_urls.append(url)                                                    # I'm not sure why I wrote it in the first place
    return chord_sheet_urls

def urls_to_sheets(chord_sheet_urls):
    chord_sheets = []
    weights = []
    for url in chord_sheet_urls:
        sheet_data = get_chord_sheet(url)
        weights.append(sheet_data[0])
        raw_chord_sheet = sheet_data[1]
        processed_chord_sheet = music.process_chords(raw_chord_sheet)
        chord_sheets.append(processed_chord_sheet)
    return [chord_sheets, weights]

def get_billboard_songs(year, max_num_songs):
    interface.print_title('BILLBOARD TOP HITS')
    url = 'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_' + str(year)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find('div', attrs={'id':'mw-content-text'}).table
    songs = []
    num = 0
    for row in results.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) < 2:
            continue
        title = cells[len(cells) - 2].text.replace('\"','')
        artist = cells[len(cells) - 1].a.text.replace('\"','')
        print '\"' + title + '\" by ' + artist + '...', ### if we change the order here, then we can use str(s)...
        s = song.Song(title, artist)
        if len(s.chord_sheets) == 0:
            print 'NOT FOUND'
        else:
            print 'done'
        songs.append(s)
        num += 1
        if num >= max_num_songs:
            break
    return songs