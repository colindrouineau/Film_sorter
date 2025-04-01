from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def compute_similarity(list1, list2):
    # Join the lists into single strings
    str1 = " ".join(list1)
    str2 = " ".join(list2)

    print(str1, "\n", str2)

    # Compute the similarity ratio using Levenshtein Distance
    similarity_ratio = fuzz.ratio(str1, str2)

    return similarity_ratio


# Example usage
list1 = ["apple", "banana", "cherry"]
list2 = ["banana", "cherry", "date"]
similarity = compute_similarity(list1, list2)
print(f"Similarity Ratio: {similarity}")

# Example usage
list1 = ["apple", "banana", "cherry"]
list2 = ["cherry"]
similarity = compute_similarity(list1, list2)
print(f"Similarity Ratio: {similarity}")
