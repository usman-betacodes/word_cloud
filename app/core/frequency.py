from collections import Counter
from typing import Dict, List


def merge_frequencies(term_lists: List[List[str]], max_words: int) -> Dict[str, int]:
  all_terms: List[str] = []
  for terms in term_lists:
    all_terms.extend(terms)

  if not all_terms:
    return {"frequencies": {}}

  freq = Counter(all_terms)
  return {"frequencies": dict(freq.most_common(max_words))}
