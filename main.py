from fastapi import FastAPI, HTTPException, Request,Query
from fastapi.responses import JSONResponse
from models import TextInput, WordFrequencyResponse
from utils import generate_word_frequency
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="Roman Urdu Word Cloud API", version="1.0")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTPException to return a structured error response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail},
    )

@app.post("/word-frequency/", response_model=WordFrequencyResponse)
async def create_roman_urdu_word_cloud(
    data: TextInput, 
    max_words: int = Query(10, gt=0, le=100, description="Maximum number of words to return (must be between 1 and 100)")
):
    """
    Generate word frequencies from Roman Urdu text after
    tokenization, normalization, and stop-word removal.
    
    The 'max_words' query parameter controls the maximum number of words returned.
    It must be greater than 0 and less than or equal to 100.
    """
    # Check for empty input text
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty")
    
    try:
        # Attempt to generate word frequency with the specified max_words
        word_freq = await generate_word_frequency(data.text, max_words=max_words)

        # Return the word frequencies in the response
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
    # Pull settings from the environment, use defaults if they don't exist
    port = int(os.getenv("PORT", 8084))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port)
