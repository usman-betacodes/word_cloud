from typing import List, Set

import nltk
from nltk.stem import WordNetLemmatizer

from app.core.nltk_data import ensure_nltk
from app.processors.roman_urdu import ROMAN_STOP_WORDS

ensure_nltk()
ENGLISH_STOP_WORDS: Set[str] = {word.lower() for word in nltk.corpus.stopwords.words("english")}
_lemmatizer = WordNetLemmatizer()


def _lemmatize(token: str) -> str:
  if len(token) > 5 and token.endswith("ing"):
    lemma = _lemmatizer.lemmatize(token, pos="v")
    if lemma != token:
      return lemma
  if len(token) > 4 and token.endswith("ed"):
    lemma = _lemmatizer.lemmatize(token, pos="v")
    if lemma != token:
      return lemma
  if token.endswith("ies") and len(token) > 4:
    return _lemmatizer.lemmatize(token, pos="n")
  return _lemmatizer.lemmatize(token, pos="n")


class EnglishProcessor:
  def extract_terms(self, tokens: List[str]) -> List[str]:
    terms: List[str] = []
    for token in tokens:
      if token in ENGLISH_STOP_WORDS:
        continue
      terms.append(_lemmatize(token))
    return terms
