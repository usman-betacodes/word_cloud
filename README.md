
# Multilingual Word Frequency API

A word frequency API for mixed **Urdu**, **Roman Urdu**, and **English** media text.

## Overview

Send a single text payload and the service automatically segments Urdu script, routes Latin tokens to English or Roman Urdu processors, and returns one combined frequency dictionary.

## Features

- **Urdu script**: Stanza NLP (nouns, proper nouns, named entities)
- **Roman Urdu**: Regex tokenization + Roman stop words
- **English**: NLTK vocabulary routing + English stop words
- **Mixed text**: One request, one merged response

---

## Environment Configuration

```env
HOST=0.0.0.0
PORT=8084
```

---

## Deployment

```bash
docker compose up --build -d
docker logs word_cloud_formedia
```

---

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

---

## API

### `POST /word-frequency/`

**Query parameters:**

- `max_words` (default 10, max 100)
- `merge_concepts` (default false) — merge cross-language aliases (e.g. `pakistan` + `پاکستان`)

**Body:**

```json
{ "text": "Pakistan ki economy is improving but inflation bohat zyada hai." }
```

**Limits:** `MAX_INPUT_CHARS` env var (default 50000).

**Phase 2 features:**

- Roman Urdu spelling normalization (`achha` → `acha`)
- English lemmatization (`improving` → `improve`)
- Optional cross-script concept merging via `merge_concepts=true`
- Per-request processor logging

**Example:**

```bash
curl -X POST "http://localhost:8084/word-frequency/?max_words=10" \
  -H "Content-Type: application/json" \
  -d '{"text": "Pakistan ki economy is improving but inflation bohat zyada hai."}'
```

**Response:**

```json
{
  "frequencies": {
    "economy": 1,
    "improving": 1,
    "inflation": 1,
    "pakistan": 1,
    "bohat": 1,
    "zyada": 1
  }
}
```

### `GET /live`

Health check endpoint.

---

## Project Structure

```text
app/
  orchestrator.py       # coordinates all processors
  core/                 # segmentation, routing, frequency merge
  processors/           # urdu, roman_urdu, english
main.py                 # FastAPI entrypoint
tests/                  # unit tests
```

---

## Tests

```bash
python -m unittest discover -s tests -v
```
