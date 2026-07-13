from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
from models import TextInput, WordFrequencyResponse
from app.orchestrator import generate_word_frequency
import uvicorn
import os
import logging

MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "50000"))

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Multilingual Word Frequency API", version="2.1")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"success": False, "detail": exc.detail},
  )


@app.post("/word-frequency/", response_model=WordFrequencyResponse)
async def create_multilingual_word_frequency(
  data: TextInput,
  max_words: int = Query(20, gt=0, le=100, description="Maximum number of words to return (must be between 1 and 100)"),
  merge_concepts: bool = Query(False, description="Merge cross-language aliases into canonical keys"),
):
  """
  Generate word frequencies from mixed Urdu, Roman Urdu, and English text.
  """
  if not data.text.strip():
    raise HTTPException(status_code=400, detail="Input text is empty")

  if len(data.text) > MAX_INPUT_CHARS:
    raise HTTPException(
      status_code=400,
      detail=f"Input text exceeds maximum length of {MAX_INPUT_CHARS} characters",
    )

  try:
    return await generate_word_frequency(
      data.text,
      max_words=max_words,
      merge_concept_aliases=merge_concepts,
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/live")
async def live_status():
  return {"live": True}


if __name__ == "__main__":
  port = int(os.getenv("PORT", 8084))
  host = os.getenv("HOST", "0.0.0.0")
  uvicorn.run(app, host=host, port=port)
