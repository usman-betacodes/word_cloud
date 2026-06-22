
# Word Cloud 

An advanced text analysis API for generating word clouds with detailed word statistics.

## Overview

Nimar Word Cloud AI is a powerful API that analyzes text input and extracts rich word frequency statistics. The system processes text to identify word frequencies, making it ideal for text analysis, content summarization, and data visualization. 

## Features

- **Nouns & Proper Nouns Only**: Text analysis and word frequency calculation restricted to meaningful grammatical targets.
- **Native Urdu Support**: Processes Urdu text accurately using the Stanford Stanza NLP Model.
- **Containerized**: Fully Dockerized with pre-cached NLP models for instant deployment and startup.
- **Dynamic Configuration**: No hardcoded values; fully configurable via environment variables.

---

## Environment Configuration

Create a `.env` file in the root directory to configure the application runtime:

```env
HOST=0.0.0.0
PORT=8082

```

---

## Deployment (Production)

The recommended way to run this service is via Docker. The Docker image pre-downloads the ~200MB Stanza Urdu language models during the build phase, meaning the container starts instantly without wasting bandwidth or delaying requests.

1. Ensure your `.env` file is created.
2. Build and start the service in the background:

```bash
docker compose up --build -d

```

3. Check the logs to verify the server has started:

```bash
docker logs nimar_word_cloud_service

```

---

## Local Development Setup

If you need to run the application directly on your host machine for development:

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

2. Install the required dependencies:

```bash
pip install -r requirements.txt

```

3. Run the application (it will automatically download the Stanza models on the first run if they are not cached):

```bash
python main.py

```

---

## API Endpoints

### Generate Word Frequencies

* **Endpoint**: `/word-cloud/`
* **Method**: POST
* **Query Parameter**: `max_words` (optional, default 10, limits the return payload)
* **Request Body**: JSON with a `text` field

### Example Request

Using cURL:

```bash
curl -X POST "http://localhost:8082/word-cloud/?max_words=10" \
     -H "Content-Type: application/json" \
     -d '{"text": "علی ایک اچھا لڑکا ہے۔ اسکول جاتا ہے۔ کتاب پڑھتا ہے۔ علی نے کتاب خریدی۔"}'

```

### Example Response

The API performs tokenization, UPOS filtering (NOUN, PROPN), stopword removal, and frequency counting to return:

```json
{
  "frequencies": {
    "علی": 2,
    "کتاب": 2,
    "لڑکا": 1,
    "اسکول": 1
  }
}
