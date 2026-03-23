from pydantic import BaseModel
from typing import List

class SourceItem(BaseModel):
    section_number: str
    section_title:  str
    page_number:    int

class AskRequest(BaseModel):
    question: str
    top_k: int = 4
    threshold: float = 0.5

class AskResponse(BaseModel):
    question: str
    answer:   str
    sources:  List[SourceItem]