# Nimar Word Cloud AI

An advanced text analysis API for generating word clouds with detailed word statistics.

## Overview

Nimar Word Cloud AI is a powerful API that analyzes text input and generates rich word cloud visualizations with comprehensive word statistics. The system processes text to identify word frequencies, percentages, and percentile ranks, making it ideal for text analysis, content summarization, and data visualization.

## Features

- Text analysis and word cloud generation
- Comprehensive word statistics (frequency, percentage, percentile)
- RESTful API for easy integration
- Support for English text processing
- Clean, minimalist design for visualizations
- Customizable word cloud parameters

## Installation

### Prerequisites

- Python 3.8+
- FastAPI
- WordCloud
- NLTK
- Pandas
- Matplotlib

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

To start the Word Cloud API server, navigate to the English folder and run the main.py file:

```bash
cd english
python main.py
```

By default, this will start a FastAPI server on `http://localhost:8000`.

### API Endpoints

#### Generate Word Cloud

- **Endpoint**: `/generate-wordcloud`
- **Method**: POST
- **Request Body**: JSON with text field
- **Response**: JSON with word cloud image (Base64 encoded) and word statistics

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
curl -X POST "http://localhost:8000/generate-wordcloud" \
     -H "Content-Type: application/json" \
     -d '{"text": "This is a sample text for word cloud generation. The more frequent words will appear larger in the word cloud visualization. Word clouds are useful for visualizing the most important words in a document or corpus."}'
```

Using Python requests:
```python
import requests
import json

url = "http://localhost:8000/generate-wordcloud"
payload = {
    "text": "This is a sample text for word cloud generation. The more frequent words will appear larger in the word cloud visualization. Word clouds are useful for visualizing the most important words in a document or corpus."
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(payload), headers=headers)
result = response.json()

# Access the word cloud image
word_cloud_image = result["word_cloud_image"]

# Access word statistics
word_stats = result["word_stats"]
```

## Text Processing

The API performs several text processing steps:

1. **Tokenization**: Splits text into individual words
2. **Stopword Removal**: Removes common words that don't add significant meaning
3. **Frequency Analysis**: Counts word occurrences and calculates statistics
4. **Visualization**: Generates the word cloud with word sizes proportional to frequency

## API Response

The API returns a JSON response with:

1. **Word Cloud Image**: Base64-encoded PNG image
2. **Word Statistics**: List of words with their counts, percentages, and percentiles
3. **Word Count**: Total number of words analyzed

Example response structure:
```json
{
  "word_cloud_image": "base64-encoded-image-data",
  "word_stats": [
    {
      "word": "cloud",
      "count": 3,
      "percentage": 7.5,
      "percentile": 95.2
    },
    {
      "word": "words",
      "count": 2,
      "percentage": 5.0,
      "percentile": 85.7
    },
    ...
  ],
  "word_count": 40
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
