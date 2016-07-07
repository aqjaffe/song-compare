# stochastic_cmp.py
# -------------------
# a comparison method for song objects.
# Treats the song list as a markov model and
# compares probability distributions between songs

import music
import Queue

max_n = 4;

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

def calc_song_difference(mt1, mt2, specs):
    # do we need this first conditional?
    if mt1 is None or mt2 is None:
        return 0.0
    total_error = 0
    weights = specs[2]
    for n in range(len(mt1)):
        n_error = 0
        count = 0
        for progression in mt1[n]:
            if progression not in mt2[n]:
                continue
            if specs[0] and (len(progression) < 2 or progression[:2] == '-1'):
                continue
            if specs[1] and (len(progression) < 2 or progression[-2:] == '-1'):
                continue
            error = bhattacharyya(mt1[n][progression], mt2[n][progression])
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

def sim(song1, song2):
    mt1 = make_markov_table(song1.chord_sheets, song1.weights)
    mt2 = make_markov_table(song2.chord_sheets, song2.weights)
    uniform_weights = [False, False, [0.20, 0.20, 0.20, 0.20, 0.20]]
    return calc_song_difference(mt1, mt2, uniform_weights)