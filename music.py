# music.py
# ------------------------
# This file contains the methods for analyzing
# chord symbols, transposing songs, etc.

import sys

num_for_str = {'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3,
                'E':4, 'F':5, 'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8,
                'A':9, 'A#':10, 'Bb':10, 'B':11, 'H':11}

chords_in_key0 = {'0', '2m', '4m', '5', '7', '9m'}

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

# Adds '-1' delimiters to mark the beginning and end of each sheet
def add_delimiters(chord_sheet):
    chord_sheet.insert(0, str(-1))
    chord_sheet.append(str(-1))
    return chord_sheet

def chords_to_nums(chord_sheet):
    num_sheet = []
    for chord in chord_sheet:
        num_sheet.append(str_to_num(chord))
    return num_sheet

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

def process_chords(raw_chord_sheet):
    return add_delimiters(transpose_to_key0(chords_to_nums(raw_chord_sheet)))