import re
from collections import Counter
from nltk.corpus import stopwords
import numpy as np
from models import WordStats  # Assuming WordStats is defined elsewhere
from typing import Dict

# Load English stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text: str) -> list:
    """
    Cleans the text by removing special characters, lowercasing,
    and splitting into words while removing stopwords.
    """
    # Remove special characters and convert to lowercase
    cleaned = re.sub(r'[^\w\s]', '', text.lower())
    # Tokenize and remove stopwords
    words = [word for word in cleaned.split() if word not in stop_words]
    return words

def generate_word_frequency(text: str, max_words: int) -> Dict[str, WordStats]:
    """
    Generates a word frequency dictionary from the input text,
    returning only the top 'max_words' most frequent words along
    with their count, percentage, and percentile information.

    Args:
        text (str): The input text for generating word frequencies.
        max_words (int): The maximum number of words to return.

    Returns:
        Dict[str, WordStats]: A dictionary where keys are words
        and values are their corresponding statistics.
    """
    words = clean_text(text)
    total_words = len(words)
    word_freq = Counter(words)

    # Limit to top `max_words`
    limited_word_freq = dict(word_freq.most_common(max_words))

    # Prepare to calculate percentages and percentiles
    word_stats = {}
    frequencies = np.array(list(limited_word_freq.values()))
    sorted_indices = np.argsort(-frequencies)  # Indices of frequencies sorted in descending order

    # Font size parameters
    min_font_size = 10  # Minimum font size
    max_font_size = 100  # Maximum font size

    for rank, idx in enumerate(sorted_indices):
        word = list(limited_word_freq.keys())[idx]
        count = limited_word_freq[word]
        percentage = (count / total_words) * 100 if total_words > 0 else 0.0

        # Calculate percentile based on rank (rank is zero-indexed)
        percentile = (rank / (len(frequencies) - 1)) * 100 if len(frequencies) > 1 else 0

        # Calculate font size based on percentile
        font_size = min_font_size + (max_font_size - min_font_size) * (percentile / 100)

        word_stats[word] = WordStats(
            word=word,
            count=count,
            percentage=round(percentage, 2),
            percentile=round(percentile, 2)
        )

        # Print to visualize the output for each word
        print(f"Word: {word}, Count: {count}, Percentage: {round(percentage, 2)}%, "
              f"Percentile: {round(percentile, 2)}%, Font Size: {round(font_size, 2)}")

    return word_stats

# Example usage
text = "This is a simple example. This example demonstrates how to calculate word frequency, percentages, and percentiles."
result =generate_word_frequency(text, max_words=5)
print(result)
