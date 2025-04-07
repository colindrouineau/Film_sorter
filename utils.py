import chardet

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
