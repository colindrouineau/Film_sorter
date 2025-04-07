import utils as u

PUNCTUATION = [
    " ",
    "'",
    "&",
    "~",
    "#",
    "{",
    "(",
    "[",
    "-",
    "|",
    "`",
    "_",
    ")",
    "°",
    "]",
    "=",
    "+",
    "}",
    "<",
    ">",
    ",",
    "?",
    ";",
    ".",
    ":",
    "!",
    "§",
]


STOP_WORDS_ENGLISH = u.list_from_txt("stop_words_english.txt")
STOP_WORDS_FRENCH = u.list_from_txt("stop_words_french.txt")


if __name__ == "__main__":
    print(STOP_WORDS_FRENCH)
