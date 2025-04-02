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

"""
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
"""
def levenshtein_costless_deletions(s1, s2):
    # Create a matrix to store the distances
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    # Initialize the first row and column
    for j in range(1, len_s2 + 1):
        dp[0][j] = j  # Only insertions are allowed

    # Fill the matrix
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Characters match, no new operation needed
            else:
                dp[i][j] = min(dp[i - 1][j - 1] + 1,  # Substitution
                                dp[i][j - 1] + 1,     # Insertion
                                dp[i - 1][j])         # Deletion (costless)

    return dp[len_s1][len_s2]

# Example usage
s1 = "kitten"
s2 = "sitting"
distance = levenshtein_costless_deletions(s1, s2)
print(f"Modified Levenshtein Distance (costless deletions): {distance}")
