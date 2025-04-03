import utils as u

PUNCTUATION = ["'", "&", "~", "#", "{", "(", "[", "-", "|", "`", "_", ")", "°", "]", "=", "+", "}", "<", ">", ",", "?", ";", ".", ":", "!", "§"]


STOP_WORDS_ENGLISH = u.list_from_txt('stop_words_english.txt')
STOP_WORDS_FRENCH = u.list_from_txt('stop_words_french.txt')

print(STOP_WORDS_FRENCH)
