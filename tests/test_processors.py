import unittest

from app.core.frequency import merge_frequencies
from app.core.segmentation import segment_text
from app.core.latin_router import classify_latin_tokens
from app.processors.english import EnglishProcessor
from app.processors.roman_urdu import RomanUrduProcessor


class TestProcessors(unittest.TestCase):
  def test_english_processor(self):
    processor = EnglishProcessor()
    terms = processor.extract_terms(["economy", "the", "inflation"])
    self.assertEqual(terms, ["economy", "inflation"])

  def test_roman_processor(self):
    processor = RomanUrduProcessor()
    terms = processor.extract_terms(["bohat", "zyada", "hai"])
    self.assertEqual(terms, ["bohat", "zyada"])

  def test_merge_frequencies(self):
    result = merge_frequencies([["economy", "economy"], ["bohat"]], max_words=5)
    self.assertEqual(result["frequencies"]["economy"], 2)
    self.assertEqual(result["frequencies"]["bohat"], 1)


class TestMixedPipeline(unittest.TestCase):
  def test_mixed_latin_only_sentence(self):
    text = "Pakistan ki economy is improving but inflation bohat zyada hai."
    _, latin_tokens = segment_text(text)
    english, roman = classify_latin_tokens(latin_tokens)
    english_terms = EnglishProcessor().extract_terms(english)
    roman_terms = RomanUrduProcessor().extract_terms(roman)
    merged = merge_frequencies([english_terms, roman_terms], max_words=10)
    freqs = merged["frequencies"]
    self.assertIn("economy", freqs)
    self.assertIn("improving", freqs)
    self.assertIn("inflation", freqs)
    self.assertIn("bohat", freqs)
    self.assertIn("zyada", freqs)


if __name__ == "__main__":
  unittest.main()
