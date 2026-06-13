import re
from collections import Counter
from typing import Dict, List
import logging
import stanza


# =========================================================
# LOGGING  (rejected fragments -> file for later review)
# =========================================================
frag_logger = logging.getLogger("rejected_fragments")
frag_logger.setLevel(logging.INFO)
_handler = logging.FileHandler("rejected_fragments.log", encoding="utf-8")
_handler.setFormatter(logging.Formatter("%(asctime)s\t%(message)s"))
frag_logger.addHandler(_handler)
 
# =========================================================
# STANZA INIT  (once at import)
# =========================================================
stanza.download("ur", processors="tokenize,pos,ner", verbose=False)
 
ur_nlp = stanza.Pipeline(
    "ur",
    processors="tokenize,pos,ner",
    use_gpu=False,
    verbose=False,
)

# =========================================================
# STOPWORDS  (function words - safe to hardcode, closed set)
# =========================================================
stop_words = {
    "ہے", "کی", "کا", "میں", "سے", "اور", "ایک", "پر", "کو", "کے", "ہیں",
    "تو", "کہ", "نے", "یہ", "وہ", "تھا", "تھی", "تھے", "کر", "رہا", "رہی",
    "گیا", "گئی", "دی", "لیا", "ہو", "جا", "نہ", "نہیں", "تک", "بھی", "ہی",
    "جو", "اس", "ان", "اپنے", "اپنی", "گا", "گے", "گی", "دیا", "لیے", "ساتھ",
    "بعد", "دوران", "خلاف", "مطابق", "ذریعے", "علاوہ", "باعث", "وجہ",
}

# =========================================================
# NORMALIZATION
# =========================================================
def normalize_urdu(text: str) -> str:
    """Clean invisible chars, unify letter forms, fix spacing."""
    if not text:
        return ""
 
    # Invisible / zero-width characters
    text = text.replace("\u200c", " ").replace("\u200b", " ")
    text = text.replace("\u200d", "").replace("\ufeff", "")
 
    # Unify Arabic vs Urdu letter forms (same word, different codepoint)
    text = text.replace("\u064a", "\u06cc")  # Arabic ya  -> Urdu ya
    text = text.replace("\u0643", "\u06a9")  # Arabic kaf -> Urdu kaf
    text = text.replace("\u0629", "\u06c1")  # ta marbuta -> Urdu ha
 
    # Strip Arabic diacritics / harakat
    text = re.sub(r"[\u064b-\u0652\u0670]", "", text)
 
    # Space out punctuation so it never glues to words
    text = re.sub(r"([۔،؛:!؟()\"'])", r" \1 ", text)
 
    text = re.sub(r"\s+", " ", text)
    return text.strip()
 
 
def clean_token(token: str) -> str:
    """Keep Urdu letters and spaces only."""
    token = re.sub(r"[^\u0600-\u06FF\s]", "", token)
    return re.sub(r"\s+", " ", token).strip()
 
 
# =========================================================
# GENERAL VALIDITY RULE
# (replaces the hand-maintained garbage list - works on
#  unseen splinters because it judges shape, not identity)
# =========================================================
def is_valid_word(word: str) -> bool:
    """
    A token is kept only if it plausibly looks like a real Urdu word.
    No hardcoded bad-word list - this generalizes to open-domain news.
    """
    if not word:
        return False
 
    # Single-char tokens are almost always tokenizer splinters.
    if len(word) < 2:
        return False
 
    # Absurdly long = merged OCR garbage.
    if len(word) > 30:
        return False
 
    # Pure function words.
    if word in stop_words:
        return False
 
    # Must contain at least 2 distinct Urdu letters (filters "ٹٹ" etc.)
    letters = [c for c in word if "\u0600" <= c <= "\u06FF"]
    if len(set(letters)) < 2:
        return False
 
    return True
 
 
# =========================================================
# EXTRACTION
# =========================================================
# Minimal regex - only the highest-frequency Urdu news constructs.
# NER handles everything else.
NEWS_PHRASE_PATTERNS = [
    r"([\u0600-\u06FF]+\s+کورٹ)",     # X کورٹ
    r"([\u0600-\u06FF]+\s+تھانے)",    # X تھانے
    r"([\u0600-\u06FF]+\s+یونیورسٹی)",
    r"([\u0600-\u06FF]+\s+ہسپتال)",
]
 
 
def extract_words(text: str) -> List[str]:
    """
    Extract nouns + named entities from open-domain Urdu text.
 
    Order matters: multi-word phrases first (NER + regex), recording
    which single tokens they consume, so the noun pass does not
    double-count a token already inside a phrase.
    """
    if not text.strip():
        return []
 
    text = normalize_urdu(text)
    doc = ur_nlp(text)
 
    extracted: List[str] = []
    consumed: set = set()
 
    # ---- 1. NAMED ENTITIES (generalizes across all news) ----
    for ent in getattr(doc, "ents", []):
        phrase = clean_token(ent.text)
        if is_valid_word(phrase):
            extracted.append(phrase)
            consumed.update(phrase.split())
 
    # ---- 2. MINIMAL NEWS REGEX (a few common constructs only) ----
    for pattern in NEWS_PHRASE_PATTERNS:
        for match in re.findall(pattern, text):
            phrase = clean_token(match)
            if is_valid_word(phrase):
                extracted.append(phrase)
                consumed.update(phrase.split())
 
    # ---- 3. SINGLE NOUNS / PROPER NOUNS ----
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.upos not in ("NOUN", "PROPN"):
                continue
            token = clean_token(word.text)
            if token in consumed:
                continue
            if is_valid_word(token):
                extracted.append(token)
            elif 0 < len(token) < 2:
                # Log dropped single-char splinters for later review.
                frag_logger.info(f"dropped_fragment\t{token}\t{word.upos}")
 
    return extracted
 
 
# =========================================================
# FREQUENCY
# =========================================================
async def generate_word_frequency(text: str, max_words: int) -> Dict:
    words = extract_words(text)
    if not words:
        return {"frequencies": {}}
    freq = Counter(words)
    return {"frequencies": dict(freq.most_common(max_words))}
 

    # Prepare to calculate percentages and percentiles
    # word_stats = []

    
    # # Calculate total unique words for percentile calculation
    # total_unique_words = len(limited_word_freq)

    # # Sort words by frequency in descending order
    # sorted_word_freq = sorted(limited_word_freq.items(), key=lambda item: item[1], reverse=True)

    # for rank, (word, count) in enumerate(sorted_word_freq, start=1):
    #     # Calculate percentage of the total words
    #     percentage = (count / total_words) * 100 if total_words > 0 else 0.0
        
    #     # Calculate percentile based on rank and total unique words
    #     percentile = (rank / total_unique_words) * 100

    #     # Append word statistics as a dictionary to the list
    #     word_stats.append({
    #         "word": word,
    #         "count": count,
    #         "percentage": round(percentage, 2),
    #         "percentile": round(percentile, 2)
    #     })
    # # print(word_stats)
    # return word_stats


