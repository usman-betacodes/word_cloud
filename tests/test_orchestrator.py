import unittest

from app.orchestrator import generate_word_frequency


class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
  async def test_roman_and_english_only(self):
    text = "Pakistan ki economy is improving but inflation bohat zyada hai."
    result = await generate_word_frequency(text, max_words=10)
    freqs = result["frequencies"]
    self.assertIn("economy", freqs)
    self.assertIn("bohat", freqs)

  async def test_empty_text_returns_empty(self):
    result = await generate_word_frequency("   ", max_words=10)
    self.assertEqual(result["frequencies"], {})


if __name__ == "__main__":
  unittest.main()
