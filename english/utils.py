import re
from collections import Counter
from nltk.corpus import stopwords

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

def generate_word_frequency(text: str) -> dict:
    """
    Generate a word frequency dictionary from the input text.
    """
    words = clean_text(text)
    word_freq = Counter(words)
    # Sort by frequency in descending order
    sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
    return sorted_word_freq
