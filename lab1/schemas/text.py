from pydantic import BaseModel, field_validator, Field
from datetime import datetime


class STextBase(BaseModel):
    name: str
    text: str

    @field_validator("name")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        if not (v.endswith(".doc") or v.endswith(".docx")):
            raise ValueError("Файл должен иметь расширение .doc или .docx")
        return v


class STextAdd(STextBase):
    pass


class STextUpdate(STextBase):
    date: datetime = datetime.now()


class STextResponse(STextBase):
    date: datetime
