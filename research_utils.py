from fuzzywuzzy import fuzz
from utils import punctuation_split
from CONFIG import *


def significant_beginning(text, test=False):
    text = punctuation_split(text.lower())
    text.pop()  # On enlève l'extension
    # On enlève le "Disk disk_number"
    if text[0] == "Disk":
        text = text[2:]
    n_sig_words = 0
    i = 0
    last_recorded = 0
    while n_sig_words < 2 and i < len(text):
        if text[i] not in STOP_WORDS_ENGLISH and text[i] not in STOP_WORDS_FRENCH:
            n_sig_words += 1
            last_recorded = i + 1 if i < len(text) else len(text)
        i += 1
    sig_beg = " ".join(text[:last_recorded])
    if test:
        print(sig_beg)
    return sig_beg


# Computes the Levenshtein distance between 2 parts of 2 texts
# The parts are selected by stopping after 2 significant words.
def significant_str_distance(text1, text2, test=False):
    text1, text2 = significant_beginning(text1), significant_beginning(text2)
    # Compute the similarity ratio using Levenshtein Distance
    similarity_ratio = fuzz.ratio(text1, text2)

    if test:
        print(text1, "\n", text2)
        print(similarity_ratio)

    return similarity_ratio


if __name__ == "__main__":

    test_str = "Hello I'm COLIN. DROUINEAU 1253.MIDJ .mkv"
    significant_beginning(test_str, test=True)

    text1 = test_str
    text2 = "The worlds knows me as hello colin.mkv"
    text3 = "amazingdf.mkv"
    # significant_str_distance(text1, text2, test=True)
    # significant_str_distance(text1, text3, test=True)
    significant_str_distance(text3, text2, test=True)
