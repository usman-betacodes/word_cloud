import nltk

_nltk_ready = False


def ensure_nltk() -> None:
  global _nltk_ready
  if _nltk_ready:
    return
  for resource in ("stopwords", "words"):
    try:
      nltk.data.find(f"corpora/{resource}")
    except LookupError:
      nltk.download(resource, quiet=True)
  _nltk_ready = True
