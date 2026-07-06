from typing import List, Set, Tuple

import nltk

from app.core.logging import frag_logger
from app.core.nltk_data import ensure_nltk
from app.processors.english import ENGLISH_STOP_WORDS
from app.processors.roman_urdu import ROMAN_STOP_WORDS

_english_vocab: Set[str] | None = None


def _get_english_vocab() -> Set[str]:
  global _english_vocab
  ensure_nltk()
  if _english_vocab is None:
    _english_vocab = {word.lower() for word in nltk.corpus.words.words()}
  return _english_vocab


def _looks_english(token: str, english_vocab: Set[str]) -> bool:
  if token in english_vocab:
    return True

  if len(token) > 5 and token.endswith("ing"):
    stem = token[:-3]
    if stem in english_vocab or f"{stem}e" in english_vocab:
      return True

  if len(token) > 4 and token.endswith("ed"):
    stem = token[:-2]
    if stem in english_vocab or f"{stem}e" in english_vocab:
      return True

  if token.endswith(("tion", "ness", "ment", "able", "ible")):
    return True

  return False


def classify_latin_tokens(tokens: List[str]) -> Tuple[List[str], List[str]]:
  english_vocab = _get_english_vocab()
  english_tokens: List[str] = []
  roman_tokens: List[str] = []

  for token in tokens:
    if token in ROMAN_STOP_WORDS:
      frag_logger.info(f"dropped_stopword\troman\t{token}")
      continue
    if token in ENGLISH_STOP_WORDS:
      frag_logger.info(f"dropped_stopword\tenglish\t{token}")
      continue
    if _looks_english(token, english_vocab):
      english_tokens.append(token)
    else:
      roman_tokens.append(token)

  return english_tokens, roman_tokens
