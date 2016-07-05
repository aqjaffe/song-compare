# AUTHOR: Adam Jaffe
# UPDATED: 6.29.16
# ---------------------------------------------
# This program is my first experiment in web-scraping!
# It prompts the user for a song and artist and then collects
# relevant chord data from www.ultimate-guitar.com to compile
# a list of all of the user-generated chord sheets avaiable.
# It transposes these all to the same key for easy comparison.

import interface

### TODO: rewrite these method in terms of the song class
### (currently they are written with outdated song-as-list protocol)

def get_best_pairs(songs, num_results):
    pairs = []
    for i in range(len(songs)):
        for j in range(len(songs) - i - 1):
            element = [songs[i][0], songs[i][1], songs[i + j + 1][0], songs[i + j + 1][1]]
            results = compare.run_test_suite(songs[i], songs[i + j + 1], False)
            sim = compare.get_average_results(results)
            element.append(sim)
            if len(pairs) < num_results:
                pairs.append(element)
                pairs.sort(key=lambda el: -el[4])
            elif sim > pairs[num_results - 1][4]:
                pairs.append(element)
                pairs.sort(key=lambda el: -el[4])
                pairs.pop()
    return pairs

def get_best_match(target_song, songs, num_results):
    matches = []
    for i in range(len(songs)):
        element = [target_song[0], target_song[1], songs[i][0], songs[i][1]]
        results = run_test_suite(songs[i], target_song, False)
        sim = get_average_results(results)
        element.append(sim)
        if len(matches) < num_results:
            matches.append(element)
            matches.sort(key=lambda el: -el[4])
        elif sim > matches[num_results - 1][4]:
            matches.append(element)
            matches.sort(key=lambda el: -el[4])
            matches.pop()
    return matches