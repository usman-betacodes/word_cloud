from pydantic import BaseModel
from typing import List


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


class WordCloudOutput(BaseModel):
    """
    Pydantic model for the output of the word cloud.

    Attributes:
        word_cloud (List[WordStats]): A list containing word statistics.
    """
    word_cloud: List[WordStats]
