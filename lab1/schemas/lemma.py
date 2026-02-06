from pydantic import BaseModel, Field


class SLemmaAdd(BaseModel):
    text_id: int = Field(..., ge=1)
    word: str
    lemma: str
    morph: str
    role: str


class SLemmaUpdate(BaseModel):
    lemma: str
    morph: str
    role: str
