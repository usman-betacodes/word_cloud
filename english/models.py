from pydantic import BaseModel
from typing import Dict


class TextInput(BaseModel):
    text: str


class WordCloudOutput(BaseModel):
    word_cloud: Dict[str, int]