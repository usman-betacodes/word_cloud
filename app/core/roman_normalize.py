import re

ROMAN_VARIANTS = {
  "accha": "acha",
  "achha": "acha",
  "acchha": "acha",
  "achaaa": "acha",
  "bohot": "bohat",
  "boht": "bohat",
  "zyada": "zyada",
  "zyadaa": "zyada",
  "zyadaah": "zyada",
  "tez": "tez",
  "tezz": "tez",
  "pakistan": "pakistan",
  "paakistan": "pakistan",
}


def normalize_roman(token: str) -> str:
  token = token.lower()
  token = re.sub(r"(.)\1+", r"\1", token)
  return ROMAN_VARIANTS.get(token, token)
