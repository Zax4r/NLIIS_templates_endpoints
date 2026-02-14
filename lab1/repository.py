from database import SessionDep
from models.text import Text
from models.lemma import Lemma
from sqlalchemy import select, delete
from schemas.lemma import SLemmaAddDb, SLemmaUpdate
from schemas.text import STextAdd, STextUpdate
import sqlalchemy


class TextRepository:

    @classmethod
    async def get_all(cls, session: SessionDep):
        query = select(Text)
        query_result = await session.execute(query)
        texts = query_result.scalars().all()
        return texts

    @classmethod
    async def get_one(cls, id: int, session: SessionDep):
        text_query = select(Text).where(Text.id == id)
        text_result = await session.execute(text_query)
        text = text_result.scalar_one_or_none()
        return text

    @classmethod
    async def add_one(cls, data: STextAdd, session: SessionDep):
        text_dict = data.model_dump()
        text = Text(**text_dict)
        session.add(text)
        await session.commit()
        await session.refresh(text)
        return text

    @classmethod
    async def delete_one(cls, id: int, session: SessionDep):
        text = await session.get(Text, id)
        if text:
            await session.delete(text)
            await session.commit()
        else:
            raise ValueError(f"Text with id {id} not found")

    @classmethod
    async def update_text(cls, id: int, data: STextUpdate, session: SessionDep):
        data_dict = data.model_dump()
        text = await session.get(Text, id)
        if text:
            text.name = data_dict.get("name")
            text.text = data_dict.get("text")
        await session.commit()
        return text


class LemmaRepository:

    @classmethod
    async def get_one(cls, id: int, session: SessionDep):
        lemma_query = select(Lemma).where(Lemma.id == id)
        lemma_result = await session.execute(lemma_query)
        lemma = lemma_result.scalar_one_or_none()
        return lemma

    @classmethod
    async def get_all(cls, text_id: int, session: SessionDep):
        lemma_query = (
            select(Lemma).where(Lemma.text_id == text_id).order_by(Lemma.word.asc())
        )
        lemma_result = await session.execute(lemma_query)
        lemma = lemma_result.scalars().all()
        return lemma

    @classmethod
    async def add_one(cls, data: SLemmaAddDb, session: SessionDep):
        data_dict = data.model_dump()

        existing_lemma_query = select(Lemma).where(
            Lemma.text_id == data_dict["text_id"],
            Lemma.lemma == data_dict["lemma"],
            Lemma.morph == data_dict["morph"],
            Lemma.role == data_dict["role"]
        )
        existing_lemma_result = await session.execute(existing_lemma_query)
        existing_lemma = existing_lemma_result.scalar_one_or_none()
        
        if existing_lemma:
            return existing_lemma
        
        lemma = Lemma(**data_dict)
        session.add(lemma)
        await session.commit()
        await session.refresh(lemma)
        return lemma


    @classmethod
    async def delete_one(cls, id: int, session: SessionDep):
        lemma = await session.get(Lemma, id)
        if lemma:
            await session.delete(lemma)
            await session.commit()
        else:
            raise ValueError(f"Text with id {id} not found")

    @classmethod
    async def delete_all(cls, text_id: int, session: SessionDep):
        stmt = delete(Lemma).where(Lemma.text_id == text_id)
        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def update_one(cls, id: int, data: SLemmaUpdate, session: SessionDep):
        data_dict = data.model_dump()
        lemma = await session.get(Lemma, id)
        if lemma:
            lemma.lemma = data_dict.get("lemma")
            lemma.morph = data_dict.get("morph")
            lemma.role = data_dict.get("role")
        await session.commit()
        return lemma

    @classmethod
    async def filter(cls, text_id: int, morph: str, session: SessionDep):
        lemma_query = (
            select(Lemma)
            .where(Lemma.text_id == text_id)
            .where(Lemma.morph == morph)
            .order_by(Lemma.word.asc())
        )
        lemma_result = await session.execute(lemma_query)
        lemma = lemma_result.scalars().all()
        return lemma

    @classmethod
    async def search(cls, text_id:int, word: str, session: SessionDep):
        lemma_query = (
            select(Lemma)
            .where(Lemma.text_id == text_id)
            .where(Lemma.word.like(word))
            .order_by(Lemma.word.asc())
        )
        lemma_result = await session.execute(lemma_query)
        lemma = lemma_result.scalars().all()
        return lemma