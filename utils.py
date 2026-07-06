import re
from collections import Counter
from typing import Dict, List
import logging


# =========================================================
# LOGGING  (rejected fragments -> file for later review)
# =========================================================
frag_logger = logging.getLogger("rejected_fragments")
frag_logger.setLevel(logging.INFO)
_handler = logging.FileHandler("rejected_fragments.log", encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s\t%(message)s"))
frag_logger.addHandler(_handler)
 

# =========================================================
# ROMAN URDU STOPWORDS
# =========================================================

ROMAN_STOP_WORDS = {
    
    "hai", "hain", "han", "tha", "thi", "the", "hoga", "hogi", "honge",
    "hon", "hoon", "hota", "hoti", "hote", "ho", "hua", "hui", "hue",
    "hona", "hone", "hokar", "hoke",

    "main", "mein", "hum", "tum", "aap", "ye", "yeh", "wo", "woh",
    "is", "us", "un", "unhein", "unhe", "inhen", "jis", "jise",
    "jiska", "jiski", "jiske", "kaun", "kon", "kaunsa", "kaunsi",
    "kis", "kisne", "kisko",

    "ko", "ka", "ki", "ke", "se", "par", "tak", "liye", "keliye",
    "keliye", "waste", "vaste", "taraf", "andar", "bahar", "upar",
    "neeche",

    "aur", "ya", "lekin", "magar", "balki", "kyunke", "kyunki",
    "chunanche", "agar", "to", "phir", "warna", "jab", "jabke",
    "isliye", "lehaza",

    "kya", "kyun", "kyu", "kab", "kahan", "kidhar", "kaise",

    "ji", "haan", "han", "nahi", "nahin", "na", "ne", "acha",
    "acha", "theek", "theekhai", "theekhai", "ok", "okay",
    "yar", "yaar", "bhai", "bhaii", "dekho", "suno", "matlab",
    "yani", "bas", "sirf", "zara", "chalo",

    "ab", "tab", "abhi", "kabhi", "hamesha", "aksar", "pehle",
    "baad", "kal", "aaj", "parson", "foran",

    "oh", "oho", "wah", "are", "achaacha", "theektheek",
    "kiabaat", "chalien", "chalen",

    "ao", "aao", "jao", "karo", "karlo", "dekhona", "sunona",
    "chalona",

    "hi", "bhi",

    "ek", "aik", "keh", "jo", "apne", "apni",
    "ga", "ge", "gi", "diya", "di", "liya",
    "saath", "doran", "khilaf", "mutabiq",
    "zariye", "zariyey", "ilawa", "bais", "wajah",


    "b", "c", "d", "ch", "p",
    "dar", "ani", "naib", "abad",
    "j", "a", "awam", "hal",
    "aman", "duniya", "media",
     "khabrain", "khabar"
}


# =========================================================
# ROMAN URDU EXTRACTION
# =========================================================
def extract_roman_words(text: str) -> List[str]:
    """
    Extracts valid Roman Urdu words from the text.
    """
    # 1. Lowercase for standardization
    text = text.lower()
    
    # 2. Extract only Latin alphabetical words (length 2 or more)
    # This automatically strips out numbers, punctuation
    raw_words = re.findall(r'\b[a-z]{2,}\b', text)
    
    # 3. Filter out the stop words and LOG the dropped ones
    valid_words = []
    for w in raw_words:
        if w in ROMAN_STOP_WORDS:
            # Log the dropped word
            frag_logger.info(f"dropped_stopword\t{w}")
        else:
            valid_words.append(w)
    
    return valid_words



# =========================================================
# FREQUENCY
# =========================================================
async def generate_word_frequency(text: str, max_words: int) -> Dict:
   
    # Get Roman Urdu words (using the new lightweight logic)
    roman_words = extract_roman_words(text)
    
    # Combine both lists
    all_words = roman_words
    
    if not all_words:
        return {"frequencies": {}}
        
    freq = Counter(all_words)
    return {"frequencies": dict(freq.most_common(max_words))}





