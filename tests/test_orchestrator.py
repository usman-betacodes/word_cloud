import unittest

from app.orchestrator import generate_word_frequency


class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
  async def test_roman_and_english_only(self):
    text = "Pakistan ki economy is improving but inflation bohat zyada hai."
    result = await generate_word_frequency(text, max_words=10)
    freqs = result["frequencies"]
    self.assertIn("economy", freqs)
    self.assertIn("bohat", freqs)

  async def test_merge_concepts_flag(self):
    text = "Pakistan ki economy is improving. پاکستان کی معیشت بہتر ہو رہی ہے."
    result = await generate_word_frequency(text, max_words=10, merge_concept_aliases=True)
    freqs = result["frequencies"]
    self.assertIn("پاکستان", freqs)
    self.assertIn("معیشت", freqs)

  async def test_empty_text_returns_empty(self):
    result = await generate_word_frequency("   ", max_words=10)
    self.assertEqual(result["frequencies"], {})


if __name__ == "__main__":
  unittest.main()
