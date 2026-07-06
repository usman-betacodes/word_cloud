import unittest

from app.core.latin_router import classify_latin_tokens
from app.core.segmentation import segment_text


class TestSegmentation(unittest.TestCase):
  def test_mixed_script_segmentation(self):
    text = "پاکستان ki economy بہتر ہو رہی ہے"
    urdu_text, latin_tokens = segment_text(text)
    self.assertIn("پاکستان", urdu_text)
    self.assertIn("بہتر", urdu_text)
    self.assertIn("ki", latin_tokens)
    self.assertIn("economy", latin_tokens)


class TestLatinRouter(unittest.TestCase):
  def test_routes_english_and_roman(self):
    tokens = ["pakistan", "ki", "economy", "is", "improving", "bohat", "zyada", "hai"]
    english, roman = classify_latin_tokens(tokens)
    self.assertIn("economy", english)
    self.assertIn("improving", english)
    self.assertIn("bohat", roman)
    self.assertIn("zyada", roman)
    self.assertIn("pakistan", roman)
    self.assertNotIn("ki", english + roman)
    self.assertNotIn("hai", english + roman)


if __name__ == "__main__":
  unittest.main()
