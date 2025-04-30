import chardet
from CONFIG import *

## No longer useful because the stop word list is directly written as a str.
# def list_from_txt(file_path):
#     # Detect the encoding of the file
#     with open(file_path, "rb") as file:
#         raw_data = file.read()
#         result = chardet.detect(raw_data)
#         encoding = result["encoding"]
#
#     # Read the file with the detected encoding
#     with open(file_path, "r", encoding=encoding) as file:
#         content = file.read()
#
#     content = content.split("\n")
#     return content

def punctuation_split(text):
    splitting = []
    word = ""
    text = str(text)
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


def get_extension(file_name):
    return str(file_name).split(".")[-1]