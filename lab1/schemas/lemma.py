from pydantic import BaseModel, Field


class SLemmaBase(BaseModel):
    lemma: str
    morph: str
    role: str


class SLemmaAdd(SLemmaBase):
    word: str

class SLemmaAddDb(SLemmaAdd):
    text_id: int = Field(...,ge=1)

class SLemmaUpdate(SLemmaBase):
    pass

class SLemmaResponse(SLemmaBase):
    id: int
    word: str
