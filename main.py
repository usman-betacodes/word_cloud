from fastapi import FastAPI, HTTPException, Request,Query
from fastapi.responses import JSONResponse
from models import TextInput, WordFrequencyResponse
from utils import *
import uvicorn
from typing import List

# Initialize FastAPI app
app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTPException to return a structured error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail},
    )

@app.post("/word-cloud/", response_model=WordFrequencyResponse)
async def create_english_word_cloud(
    data: TextInput, 
    max_words: int = Query(10, gt=0, le=100, description="Maximum number of words to return (must be between 1 and 100)")
):
    """
    Generate an English word cloud from the input text, remove stopwords,
    and return the words sorted by frequency in a dictionary.
    
    The 'max_words' query parameter controls the maximum number of words returned.
    It must be greater than 0 and less than or equal to 100.
    """
    # Check for empty input text
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty")
    
    try:
        # Attempt to generate word frequency with the specified max_words
        word_freq = await generate_word_frequency(data.text, max_words=max_words)

        # Return success with an empty word cloud if no valid words are found
        return word_freq
    
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/live")
async def live_status():
    """
    Endpoint to check if the service is live.
    Returns True if the service is running.
    """
    return {"live": True}

# Add the following block to run the app as a script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
