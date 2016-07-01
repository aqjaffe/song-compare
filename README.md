# song-compare
This program runs a comparison between the chord progressions of songs.

CURRENT BUGS:
    -Some issues with BeautifulSoup: It only reads two td's of the tbody when running on Geronimo by Sheppard. More Generally, it fails to notice many songs inputs in the ultimate-guitar database.
    -Need to make the program able to scroll through multiple pages of results, in case the artist is not on the first page.

NEXT STEPS (in order of urgency and difficulty):
    -Add a test suite to run through GitHub, to make sure that the project is working correctly after each modification
    -Find better weights/specs for the tests to be run, which will involve much more musical knowledge
    -(Look into a few modules of code for more details on what to fix/add/update.)

FUTURE PLANS:
    -Run code on a server to add songs into a database (MySQL or another for example) so that lookup can be done without accessing the internet
    -Run the song comparison algorithm(s) in a different language (most likely C++) and read from the database
