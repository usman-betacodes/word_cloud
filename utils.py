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
# NORMALIZATION
# =========================================================
def normalize_urdu(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\u200c", " ").replace("\u200b", " ")
    text = text.replace("\u200d", "").replace("\ufeff", "")

    # Arabic -> Urdu variants
    text = text.replace("\u064a", "\u06cc")  # ي -> ی
    text = text.replace("\u0643", "\u06a9")  # ك -> ک
    text = text.replace("\u0629", "\u06c1")  # ة -> ہ

    # Remove diacritics
    text = re.sub(r"[\u064b-\u0652\u0670]", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_token(token: str) -> str:
    token = re.sub(r"[^\u0600-\u06FF\s]", "", token)
    return normalize_urdu(token)

# =========================================================
# STOPWORDS  (function words - safe to hardcode, closed set)
# =========================================================
STOP_WORDS = {
    "ہے", "ہیں", "ہےں", "تھا", "تھی", "تھے", "ہوگا", "ہوگی", "ہوں",
    "ہوتا", "ہوتی", "ہوتے", "ہو", "ہوا", "ہوئی", "ہوئے", "ہونا",
    "ہونے", "ہوکر", "ہوکے",

    "میں", "ہم", "تم", "آپ", "یہ", "وہ", "اس", "اُس", "ان", "انہیں",
    "جس", "جسے", "جسکا", "جسکی", "جسکے", "کون", "کونسا", "کونسی",
    "کس", "کس نے", "کس کو",

    "کو", "کا", "کی", "کے", "سے", "پر", "تک", "لیے", "کےلیے",
    "کیلئے", "واسطے", "طرف", "اندر", "باہر", "اوپر", "نیچے",

    "اور", "یا", "لیکن", "مگر", "بلکہ", "کیونکہ", "چونکہ", "اگر",
    "تو", "پھر", "ورنہ", "جب", "جبکہ", "اس لیے", "لہٰذا",

    "کیا", "کیوں", "کب", "کہاں", "کدھر", "کیسے",

    "جی", "ہاں", "نہیں", "نا", "نہ", "اچھا", "ٹھیک", "ٹھیک ہے",
    "اوکے", "یار", "بھئی", "دیکھو", "سنو", "مطلب", "یعنی", "بس",
    "صرف", "ذرا", "چلو",

    "اب", "تب", "ابھی", "کبھی", "ہمیشہ", "اکثر", "پہلے", "بعد",
    "کل", "آج", "پرسوں", "فوراً",

    "اوہ", "اوہو", "واہ", "ارے", "اچھا اچھا", "ٹھیک ٹھاک",
    "کیا بات ہے", "چلیں",

    "آؤ", "جاؤ", "کرو", "کرلو", "دیکھو نا", "سنو نا", "چلو نا",

    "ہی", "بھی",

    # Existing words
    "ایک", "کہ", "نے", "جو", "اپنے", "اپنی",
    "گا", "گے", "گی", "دیا", "دی", "لیا",
    "ساتھ", "دوران", "خلاف", "مطابق", "ذریعے",
    "علاوہ", "باعث", "وجہ",

    # Additional words provided
    "ہی،", "بی", "سی", "ڈی", "چی", "پی", "دار", "آنی",
    "نائب", "آباد", "جے", "ای", "عوام", "حل",
    "امن", "دنیا", "میڈیا", "رپورٹ", "خبریں"
}
# Normalize all stop words once
stop_words = {normalize_urdu(word) for word in STOP_WORDS}


 
 
# =========================================================
# GENERAL VALIDITY RULE
# (replaces the hand-maintained garbage list - works on
#  unseen splinters because it judges shape, not identity)
# =========================================================
def is_valid_word(word: str) -> bool:

    word = normalize_urdu(word)

    if not word:
        return False

    if len(word) < 2:
        return False

    if len(word) > 30:
        return False

    if word in stop_words:
        return False

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

    # ---- 1. NAMED ENTITIES ----
    for ent in getattr(doc, "ents", []):
        phrase = normalize_urdu(clean_token(ent.text))

        if is_valid_word(phrase):
            extracted.append(phrase)
            consumed.update(phrase.split())

    # ---- 2. NEWS REGEX PHRASES ----
    for pattern in NEWS_PHRASE_PATTERNS:
        for match in re.findall(pattern, text):

            phrase = normalize_urdu(clean_token(match))

            if is_valid_word(phrase):
                extracted.append(phrase)
                consumed.update(phrase.split())

    # ---- 3. SINGLE NOUNS / PROPER NOUNS ----
    for sentence in doc.sentences:
        for word in sentence.words:

            if word.upos not in ("NOUN", "PROPN"):
                continue

            token = normalize_urdu(clean_token(word.text))

            if token in consumed:
                continue

            # DEBUG (remove later)
            # print(f"TOKEN={repr(token)} | STOPWORD={token in stop_words}")

            if is_valid_word(token):
                extracted.append(token)

            elif 0 < len(token) < 2:
                frag_logger.info(
                    f"dropped_fragment\t{token}\t{word.upos}"
                )

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


