import nltk

_nltk_ready = False


def ensure_nltk() -> None:
  global _nltk_ready
  if _nltk_ready:
    return
  for resource in ("stopwords", "words", "wordnet", "omw-1.4"):
    try:
      if resource.startswith("omw"):
        nltk.data.find("corpora/omw-1.4")
      else:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
      nltk.download(resource, quiet=True)
  _nltk_ready = True
