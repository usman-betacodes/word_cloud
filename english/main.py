# main.py

from fastapi import FastAPI, HTTPException, Request,Query
from fastapi.responses import JSONResponse
from models import TextInput, WordCloudOutput
from utils import generate_word_frequency
import uvicorn

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

@app.post("/english-word-cloud/", response_model=WordCloudOutput)
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
    if not data.text:
        raise HTTPException(status_code=400, detail="Input text is empty")
    
    # Call the generate_word_frequency function with the specified max_words
    word_freq = await generate_word_frequency(data.text, max_words=max_words)

    if not word_freq:
        raise HTTPException(status_code=400, detail="No valid words in input text")
    
    return WordCloudOutput(word_cloud=word_freq)

@app.get("/live/")
async def live_status():
    """
    Endpoint to check if the service is live.
    Returns True if the service is running.
    """
    return {"live": True}

# Add the following block to run the app as a script
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
