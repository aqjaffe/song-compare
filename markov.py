# markov.py

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
