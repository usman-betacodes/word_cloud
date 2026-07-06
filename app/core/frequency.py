from collections import Counter
from typing import Dict, List

from app.core.concept_merge import merge_concepts


def merge_frequencies(
  term_lists: List[List[str]],
  max_words: int,
  merge_concept_aliases: bool = False,
) -> Dict[str, int]:
  all_terms: List[str] = []
  for terms in term_lists:
    all_terms.extend(terms)

  if not all_terms:
    return {"frequencies": {}}

  freq = Counter(all_terms)
  frequencies = dict(freq.most_common(max_words if not merge_concept_aliases else None))

  if merge_concept_aliases:
    frequencies = merge_concepts(frequencies)
    frequencies = dict(Counter(frequencies).most_common(max_words))

  return {"frequencies": frequencies}
