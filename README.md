# Nimar Word Cloud AI

An advanced text analysis API for generating word clouds with detailed word statistics.

## Overview

Nimar Word Cloud AI is a powerful API that analyzes text input and generates rich word cloud visualizations with comprehensive word statistics. The system processes text to identify word frequencies, percentages, and percentile ranks, making it ideal for text analysis, content summarization, and data visualization.

## Features

- Text analysis and word frequency calculation restricted to Nouns and Proper Nouns
- RESTful API for easy integration
- Native support for Urdu text processing using Stanza NLP Model
- Minimalist and reliable backend processing
- Customizable frequency limits via `max_words` parameter

## Installation

### Prerequisites

- Python 3.8+
- FastAPI
- Stanza
- PyTorch
- Uvicorn

### Setup

1. Clone the repository:
```bash
git clone https://github.com/AI-TEAM-R-D-Models/nimar-world-cloud-ai.git
cd nimar-world-cloud-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the API

To start the Word Cloud API server, run the `main.py` file:

```bash
python main.py
```

By default, this will start a FastAPI server on `http://0.0.0.0:8082`.

### API Endpoints

#### Generate Word Cloud

- **Endpoint**: `/word-cloud/`
- **Method**: POST
- **Query Parameter**: `max_words` (optional, default 10, limits the return payload)
- **Request Body**: JSON with a `text` field
- **Response**: JSON with the top identified words and their frequencies

#### API Models

The API uses Pydantic models for request and response validation:

```python
class TextInput(BaseModel):
    """
    Pydantic model for input text.
    Attributes:
        text (str): The input text from which to generate the word cloud.
    """
    text: str

class WordStats(BaseModel):
    """
    Pydantic model for word statistics.
    Attributes:
        word (str): The word itself.
        count (int): The frequency count of the word.
        percentage (float): The percentage representation of the word's frequency.
        percentile (float): The percentile rank of the word based on frequency.
    """
    word: str
    count: int
    percentage: float
    percentile: float
```

### Example Request

Using cURL:
```bash
curl -X POST "http://localhost:8082/word-cloud/?max_words=10" \
     -H "Content-Type: application/json" \
     -d '{"text": "علی ایک اچھا لڑکا ہے۔ اسکول جاتا ہے۔ کتاب پڑھتا ہے۔ علی نے کتاب خریدی۔"}'
```

Using Python requests:
```python
import requests
import json

url = "http://localhost:8082/word-cloud/?max_words=10"
payload = {
    "text": "علی ایک اچھا لڑکا ہے۔ اسکول جاتا ہے۔ کتاب پڑھتا ہے۔ علی نے کتاب خریدی۔"
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
result = response.json()

# Access the word cloud image
word_cloud_image = result["word_cloud_image"]

# Access word statistics
word_stats = result["word_stats"]
```

The API performs several text processing steps:

1. **Tokenization**: Splits text into individual words using the Stanza Urdu NLP pipeline.
2. **POS Tagging & Filtering**: Uses Stanza UPOS tags to strictly return nouns and proper nouns (`NOUN`, `PROPN`).
3. **Stopword & Symbol Removal**: Removes common Urdu stopwords and punctuation.
4. **Frequency Analysis**: Counts the top words occurrences and limits them based on the `max_words` parameter.

## API Response

The API returns a JSON response containing frequencies mapping:

Example response structure:
```json
{
  "frequencies": {
    "علی": 2,
    "کتاب": 2,
    "لڑکا": 1,
    "اسکول": 1
  }
}
```

## Deployment

The API can be deployed using various methods:

### Docker Deployment

```bash
docker build -t nimar-word-cloud-ai .
docker run -d -p 8000:8000 nimar-word-cloud-ai
```

### Cloud Deployment

The API can be deployed to cloud platforms like AWS, Google Cloud, or Azure using their respective container services.
