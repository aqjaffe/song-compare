# main.py
# --------------
# This file executes the program.

from userIO import interface, user_input, scrape
import song
import compare
import ranking

# TODO: test this main method
def main():
    interface.print_intro()
    feature = user_input.get_feature()
    while(feature != 0):
        if feature == 1:
            interface.print_title('SONG V. SONG')
            songs = user_input.get_song_pair()
            results = compare.run_test_suite(songs[0], songs[1], True)
            interface.print_results(results)
        elif feature == 2:
            print 'Sorry, this feature is not yet implemented.'
        elif feature == 3:
            interface.print_title('SONG V. BILLBOARD')
            target_song = user_input.get_song_comparable()
            billboard_info = user_input.get_billboard_info()
            billboard_songs = scrape.get_billboard_songs(billboard_info[0], billboard_info[1])
            matches = ranking.get_best_match(target_song, billboard_songs, billboard_info[2])
            interface.print_ranking(matches)
        elif feature == 4:
            interface.print_title('BILLBOARD')
            billboard_info = user_input.get_billboard_info()
            billboard_songs = scrape.get_billboard_songs(billboard_info[0], billboard_info[1])            
            pairs = ranking.get_best_pairs(billboard_songs, billboard_info[2])
            interface.print_ranking(pairs)
        elif feature == 5:
            interface.print_title('SONGS')
            file_songs = user_input.get_songs_from_file()
            num_results = user_input.get_num_results()
            pairs = ranking.get_best_pairs(file_songs, num_results)
            interface.print_ranking(pairs)
        else:
            print 'ERROR: feature not found'
        feature = user_input.get_feature()
    print 'Thank you for running song-compare.py'

main()