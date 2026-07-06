import json
from collections import Counter
from pathlib import Path
from typing import Dict

_ALIASES_PATH = Path(__file__).resolve().parent.parent / "data" / "concept_aliases.json"
_alias_to_canonical: Dict[str, str] | None = None


def _load_alias_map() -> Dict[str, str]:
  global _alias_to_canonical
  if _alias_to_canonical is not None:
    return _alias_to_canonical

  with _ALIASES_PATH.open(encoding="utf-8") as handle:
    groups = json.load(handle)

  mapping: Dict[str, str] = {}
  for canonical, aliases in groups.items():
    mapping[canonical] = canonical
    for alias in aliases:
      mapping[alias] = canonical
      if alias.isascii():
        mapping[alias.lower()] = canonical

  _alias_to_canonical = mapping
  return mapping


def merge_concepts(frequencies: Dict[str, int]) -> Dict[str, int]:
  alias_map = _load_alias_map()
  merged: Counter = Counter()

  for word, count in frequencies.items():
    canonical = alias_map.get(word, word)
    merged[canonical] += count

  return dict(merged)
