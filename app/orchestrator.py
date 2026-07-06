import asyncio
import logging
import time
from typing import Dict, List

from app.core.frequency import merge_frequencies
from app.core.latin_router import classify_latin_tokens
from app.core.segmentation import segment_text
from app.processors.english import EnglishProcessor
from app.processors.roman_urdu import RomanUrduProcessor
from app.processors.urdu import UrduProcessor

logger = logging.getLogger("word_frequency")
_urdu_processor = UrduProcessor()
_english_processor = EnglishProcessor()
_roman_processor = RomanUrduProcessor()


async def _run_processor(processor, payload: str | List[str]):
  if not payload:
    return []
  return await asyncio.to_thread(processor.extract_terms, payload)


async def generate_word_frequency(
  text: str,
  max_words: int,
  merge_concept_aliases: bool = False,
) -> Dict:
  started = time.perf_counter()
  urdu_text, latin_tokens = segment_text(text)
  english_tokens, roman_tokens = classify_latin_tokens(latin_tokens)

  urdu_terms, english_terms, roman_terms = await asyncio.gather(
    _run_processor(_urdu_processor, urdu_text),
    _run_processor(_english_processor, english_tokens),
    _run_processor(_roman_processor, roman_tokens),
  )

  result = merge_frequencies(
    [urdu_terms, english_terms, roman_terms],
    max_words,
    merge_concept_aliases=merge_concept_aliases,
  )

  elapsed_ms = (time.perf_counter() - started) * 1000
  logger.info(
    "processed request urdu=%s english=%s roman=%s unique=%s elapsed_ms=%.2f",
    len(urdu_terms),
    len(english_terms),
    len(roman_terms),
    len(result["frequencies"]),
    elapsed_ms,
  )
  return result
