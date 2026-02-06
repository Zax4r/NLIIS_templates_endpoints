from pydantic import BaseModel, field_validator, Field
from datetime import datetime


class STextAdd(BaseModel):
    name: str
    text: str

    @field_validator("name")
    @classmethod
    def validate_filename(cls, v: str) -> str:
        if not (v.endswith(".doc") or v.endswith(".docs")):
            raise ValueError("Файл должен иметь расширение .doc или .docs")
        return v


class STextUpdate(STextAdd):
    date: datetime = datetime.now()
