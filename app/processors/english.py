from typing import List, Set

import nltk

from app.core.logging import frag_logger
from app.core.nltk_data import ensure_nltk
from app.processors.roman_urdu import ROMAN_STOP_WORDS

ensure_nltk()
ENGLISH_STOP_WORDS: Set[str] = {word.lower() for word in nltk.corpus.stopwords.words("english")}


class EnglishProcessor:
  def extract_terms(self, tokens: List[str]) -> List[str]:
    return [token for token in tokens if token not in ENGLISH_STOP_WORDS]
