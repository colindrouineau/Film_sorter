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
            splitting.append(word)
        else:
            word += c
    return splitting


def text_formatter(text):
    punc_sep = punctuation_split(text)
    extension = punc_sep.pop()
    formatted_text = " ".join(punc_sep)
    return formatted_text


if __name__ == "__main__":
    # Example usage
    file_path = "C:\\colin_films\\Dersou.Ouzala\\Dersou.Ouzala.mkv"
    extract_mkv_metadata(file_path, test=True)
