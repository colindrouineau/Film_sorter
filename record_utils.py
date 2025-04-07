from pymediainfo import MediaInfo
from CONFIG import *


def convert_milliseconds(milliseconds):
    # Calculate total seconds
    total_seconds = milliseconds // 1000

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds


# return duration as (hours, minutes, seconds), languages and subtitles as a list of the available ones.
def extract_mkv_metadata(file_path, test=False):
    media_info = MediaInfo.parse(file_path)
    duration = None
    languages = []
    subtitles = []

    for track in media_info.tracks:
        if track.track_type == "General":
            duration = convert_milliseconds(track.duration)
        elif track.track_type == "Audio":
            languages.append(track.other_language[0])
        elif track.track_type == "Text":
            subtitles.append(track.other_language[0])

    if test:
        print(f"Duration: {duration}")
        print(f"audio : {languages}")
        print(f"subtitles : {subtitles}")

    return duration, languages, subtitles


def punctuation_split(text):
    splitting = []
    word = ""
    for c in text:
        if c in PUNCTUATION:
            if word != "":
                splitting.append(word)
            word = ""
        else:
            word += c
    if word != "":
        splitting.append(word)
    return splitting


def text_formatter(text, test=False):
    punc_sep = punctuation_split(text)
    extension = punc_sep.pop()
    formatted_text = " ".join(punc_sep)
    formatted_text += "." + extension
    # First letter in capital
    formatted_text = formatted_text[0].upper() + formatted_text[1:].lower()
    if test:
        print(formatted_text)
    return formatted_text


def significant_beginning(text, test=False):
    text = punctuation_split(text)
    # On enlève l'extension
    text.pop()
    n_sig_words = 0
    i = 0
    while n_sig_words < 2:
        if text[i] not in STOP_WORDS_ENGLISH and text[i] not in STOP_WORDS_FRENCH:
            n_sig_words += 1
            print("sig:  ", text[i])
        i += 1
    sig_beg = " ".join(text[:i])
    if test:
        print(sig_beg)
    return sig_beg


# Computes the Levanshtein distance between 2 parts of 2 texts
# The parts are selected by stopping after 2 significant words.
def significant_str_distance(text1, text2):
    return None


if __name__ == "__main__":
    # Example usage
    file_path = "C:\\colin_films\\Dersou.Ouzala\\Dersou.Ouzala.mkv"
    extract_mkv_metadata(file_path, test=True)
    test_str = "Hello I'm COLIN. DROUINEAU 1253.MIDJ .mkv"
    text_formatter(test_str, test=True)
    significant_beginning(test_str, test=True)
