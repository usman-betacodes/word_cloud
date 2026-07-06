import unittest

from app.core.roman_normalize import normalize_roman


class TestRomanNormalize(unittest.TestCase):
  def test_collapses_spelling_variants(self):
    self.assertEqual(normalize_roman("achha"), "acha")
    self.assertEqual(normalize_roman("accha"), "acha")
    self.assertEqual(normalize_roman("bohot"), "bohat")
    self.assertEqual(normalize_roman("tezz"), "tez")

  def test_merges_counts_via_processor(self):
    from app.processors.roman_urdu import RomanUrduProcessor

    processor = RomanUrduProcessor()
    terms = processor.extract_terms(["achha", "accha", "acha"])
    self.assertEqual(terms, ["acha", "acha", "acha"])


if __name__ == "__main__":
  unittest.main()
