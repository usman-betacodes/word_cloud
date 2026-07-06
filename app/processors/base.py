from typing import List, Protocol, Set


class LanguageProcessor(Protocol):
  def extract_terms(self, text_or_tokens: str | List[str]) -> List[str]:
    ...
