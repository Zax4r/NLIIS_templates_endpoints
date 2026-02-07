from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime


class Text(Base):
    __tablename__ = "texts"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    text: Mapped[str]
    date: Mapped[datetime] = mapped_column(
        init=False, default=datetime.now(), nullable=False
    )
