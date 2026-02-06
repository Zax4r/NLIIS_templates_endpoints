from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Lemma(Base):
    __tablename__ = "lemmas"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    text_id: Mapped[str] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    word: Mapped[str]
    lemma: Mapped[str]
    morph: Mapped[str]
    role: Mapped[str]
