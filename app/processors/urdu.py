import re
from typing import List, Optional

import stanza

from app.core.logging import frag_logger

_ur_nlp: Optional[stanza.Pipeline] = None

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

NEWS_PHRASE_PATTERNS = [
  r"([\u0600-\u06FF]+\s+کورٹ)",
  r"([\u0600-\u06FF]+\s+تھانے)",
  r"([\u0600-\u06FF]+\s+یونیورسٹی)",
  r"([\u0600-\u06FF]+\s+ہسپتال)",
]


def normalize_urdu(text: str) -> str:
  if not text:
    return ""

  text = text.replace("\u200c", " ").replace("\u200b", " ")
  text = text.replace("\u200d", "").replace("\ufeff", "")
  text = text.replace("\u064a", "\u06cc")
  text = text.replace("\u0643", "\u06a9")
  text = text.replace("\u0629", "\u06c1")
  text = re.sub(r"[\u064b-\u0652\u0670]", "", text)
  text = re.sub(r"\s+", " ", text)
  return text.strip()


def clean_token(token: str) -> str:
  token = re.sub(r"[^\u0600-\u06FF\s]", "", token)
  return normalize_urdu(token)


stop_words = {normalize_urdu(word) for word in STOP_WORDS}


def is_valid_word(word: str) -> bool:
  word = normalize_urdu(word)
  if not word or len(word) < 2 or len(word) > 30:
    return False
  if word in stop_words:
    return False
  letters = [c for c in word if "\u0600" <= c <= "\u06FF"]
  if len(set(letters)) < 2:
    return False
  return True


def _get_ur_nlp() -> stanza.Pipeline:
  global _ur_nlp
  if _ur_nlp is None:
    stanza.download("ur", processors="tokenize,pos,ner", verbose=False)
    _ur_nlp = stanza.Pipeline(
      "ur",
      processors="tokenize,pos,ner",
      use_gpu=False,
      verbose=False,
    )
  return _ur_nlp


def _extract_words(text: str) -> List[str]:
  if not text.strip():
    return []

  text = normalize_urdu(text)
  doc = _get_ur_nlp()(text)
  extracted: List[str] = []
  consumed: set = set()

  for ent in getattr(doc, "ents", []):
    phrase = normalize_urdu(clean_token(ent.text))
    if is_valid_word(phrase):
      extracted.append(phrase)
      consumed.update(phrase.split())

  for pattern in NEWS_PHRASE_PATTERNS:
    for match in re.findall(pattern, text):
      phrase = normalize_urdu(clean_token(match))
      if is_valid_word(phrase):
        extracted.append(phrase)
        consumed.update(phrase.split())

  for sentence in doc.sentences:
    for word in sentence.words:
      if word.upos not in ("NOUN", "PROPN"):
        continue
      token = normalize_urdu(clean_token(word.text))
      if token in consumed:
        continue
      if is_valid_word(token):
        extracted.append(token)
      elif 0 < len(token) < 2:
        frag_logger.info(f"dropped_fragment\t{token}\t{word.upos}")

  return extracted


class UrduProcessor:
  def extract_terms(self, text: str) -> List[str]:
    return _extract_words(text)
