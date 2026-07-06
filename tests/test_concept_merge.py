import unittest

from app.core.concept_merge import merge_concepts


class TestConceptMerge(unittest.TestCase):
  def test_merges_cross_script_aliases(self):
    frequencies = {
      "pakistan": 3,
      "پاکستان": 2,
      "economy": 4,
      "معیشت": 1,
    }
    merged = merge_concepts(frequencies)
    self.assertEqual(merged["پاکستان"], 5)
    self.assertEqual(merged["معیشت"], 5)


if __name__ == "__main__":
  unittest.main()
