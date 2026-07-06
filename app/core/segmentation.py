import re
from typing import List, Tuple

URDU_SPAN_RE = re.compile(r"[\u0600-\u06FF]+(?:\s+[\u0600-\u06FF]+)*")
LATIN_TOKEN_RE = re.compile(r"\b[a-zA-Z]{2,}\b")


def segment_text(text: str) -> Tuple[str, List[str]]:
  urdu_spans = URDU_SPAN_RE.findall(text)
  urdu_text = " ".join(urdu_spans)
  latin_tokens = [token.lower() for token in LATIN_TOKEN_RE.findall(text)]
  return urdu_text, latin_tokens
