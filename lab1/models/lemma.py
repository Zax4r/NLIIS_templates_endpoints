from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import List


class Lemma(Base):
    __tablename__ = "lemmas"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    text_id: Mapped[str] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    word: Mapped[str]
    lemma: Mapped[str]
    morph: Mapped[str]
    role: Mapped[str]

    __table_args__ = (
        UniqueConstraint('text_id', 'lemma', 'morph', 'role', name='unique_text_lemma_morph_role'),
    )