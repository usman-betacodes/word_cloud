import re
from collections import Counter
from nltk.corpus import stopwords
from models import WordStats  # Assuming WordStats is defined elsewhere
from typing import List, Dict

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

async def generate_word_frequency(text: str, max_words: int) -> List[Dict[str, float]]:
    """
    Generates a word frequency list from the input text,
    returning only the top 'max_words' most frequent words along
    with their count, percentage, and percentile information.

    Args:
        text (str): The input text for generating word frequencies.
        max_words (int): The maximum number of words to return.

    Returns:
        List[Dict[str, float]]: A list of dictionaries where each dictionary
        contains word statistics.
    """
    words = clean_text(text)
    total_words = len(words)
    word_freq = Counter(words)

    # Limit to top `max_words`
    limited_word_freq = dict(word_freq.most_common(max_words))

    # Prepare to calculate percentages and percentiles
    word_stats = []
    frequencies = list(limited_word_freq.values())
    
    # Calculate total unique words for percentile calculation
    total_unique_words = len(limited_word_freq)

    # Sort words by frequency in descending order
    sorted_word_freq = sorted(limited_word_freq.items(), key=lambda item: item[1], reverse=True)

    for rank, (word, count) in enumerate(sorted_word_freq, start=1):
        # Calculate percentage of the total words
        percentage = (count / total_words) * 100 if total_words > 0 else 0.0
        
        # Calculate percentile based on rank and total unique words
        percentile = (rank / total_unique_words) * 100

        # Append word statistics as a dictionary to the list
        word_stats.append({
            "word": word,
            "count": count,
            "percentage": round(percentage, 2),
            "percentile": round(percentile, 2)
        })
    
    return word_stats


