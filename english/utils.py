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


async def generate_word_frequency(text: str, max_words: int) -> dict:
    """
    Generate a word frequency dictionary from the input text,
    returning only the top 'max_words' most frequent words.
    """
    words = clean_text(text)  # Assuming this function cleans the text appropriately
    word_freq = Counter(words)  # Count the frequency of each word
    
    # Sort by frequency in descending order
    sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True))
    
    # Return only the top `max_words` entries
    limited_word_freq = dict(list(sorted_word_freq.items())[:max_words])
    
    return limited_word_freq
