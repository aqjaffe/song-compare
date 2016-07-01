# scrape.py
# ----------------
# This program contains the methods for scraping
# www.ultimate-guitar.com to find chord sheets for each song

import requests
import types
import Queue
import re
from BeautifulSoup import BeautifulSoup

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

# simplifies the string in such a way that it can be used in url's for searching
def simplify_str(text):
    return ' '.join(re.sub(r'([^\s\w]|_)', '', text).split())

#TODO: fix this part of the program
# I accidentally broke it by updating to BeautifulSoup4
# For now, I reverted back to bs3, but I need to figure out how to update eventually
def get_chord_sheet_urls(title_url, artist):
    url = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=' + title_url.replace(' ', '+')
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    chord_sheet_urls = []
    search_results = soup.find('table', attrs={'class':'tresults'})
    if search_results is None:
        return url_data
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
    return chord_sheet_urls

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