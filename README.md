
# Roman Urdu Word Cloud API

A lightweight text analysis API that extracts word frequency statistics from Roman Urdu text for content analysis and word cloud visualization.

## Overview

This service analyzes Roman Urdu input (Latin script, e.g. `acha`, `pakistan`, `bohat`) and returns the most frequently occurring words after tokenization and stop-word removal. The API returns JSON frequencies only; clients can render word cloud images locally using the included `visualize.py` script or their own frontend.

## Features

- **Roman Urdu Processing**: Tokenizes Latin-script text with regex and filters common Roman Urdu stop words.
- **Lightweight**: No heavy NLP models — fast startup and low memory footprint.
- **Containerized**: Fully Dockerized for simple deployment.
- **Dynamic Configuration**: Host and port configurable via environment variables.

---

## Environment Configuration

Create a `.env` file in the root directory to configure the application runtime:

```env
HOST=0.0.0.0
PORT=8084

```

---

## Deployment (Production)

The recommended way to run this service is via Docker.

1. Ensure your `.env` file is created.
2. Build and start the service in the background:

```bash
docker compose up --build -d

```

3. Check the logs to verify the server has started:

```bash
docker logs word_cloud_formedia

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

3. Run the application:

```bash
python main.py

```

---

## API Endpoints

### Generate Word Frequencies

* **Endpoint**: `/word-frequency/`
* **Method**: POST
* **Query Parameter**: `max_words` (optional, default 10, limits the return payload)
* **Request Body**: JSON with a `text` field

### Health Check

* **Endpoint**: `/live`
* **Method**: GET

### Example Request

Using cURL:

```bash
curl -X POST "http://localhost:8084/word-frequency/?max_words=10" \
     -H "Content-Type: application/json" \
     -d '{"text": "ye naya model bohat tez hai aur aik acha system hai"}'

```

### Example Response

The API performs tokenization, stop-word removal, and frequency counting to return:

```json
{
  "frequencies": {
    "naya": 1,
    "model": 1,
    "bohat": 1,
    "tez": 1,
    "system": 1
  }
}
```
