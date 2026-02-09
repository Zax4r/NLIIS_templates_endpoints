from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaAddDb, SLemmaUpdate, SLemmaResponse
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile, Request, Depends
from repository import LemmaRepository, TextRepository
from processers.processing import DocReader
from dependencies import TextIdDep
from typing import List
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/lemma", tags=["Леммы"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_model=List[SLemmaResponse], status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep, text_id: TextIdDep):
    if not text_id:
        return []
    lemmas = await LemmaRepository.get_all(text_id, session)
    return lemmas


@router.delete(
    "/delete/{id}", response_model=SLemmaResponse | None, status_code=status.HTTP_200_OK
)
async def delete(id: int, session: SessionDep):
    await LemmaRepository.delete_one(id, session)
    return None


@router.put(
    "/update/{id}", response_model=SLemmaResponse, status_code=status.HTTP_202_ACCEPTED
)
async def update(id: int, new_lemma: SLemmaUpdate, session: SessionDep):
    lemma = await LemmaRepository.update_one(id, new_lemma, session)
    if not lemma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lemma with id {id} not found",
        )
    return lemma


@router.get("/{id}", response_model=SLemmaResponse, status_code=status.HTTP_200_OK)
async def get_one(id: int, session: SessionDep):
    lemma = await LemmaRepository.get_one(id, session)
    if not lemma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lemma with id {id} not found",
        )
    return lemma


@router.post("/", response_model=SLemmaAdd, status_code=status.HTTP_201_CREATED)
async def add_one(
    new_lemma: SLemmaAdd,
    session: SessionDep,
    text_id: TextIdDep,
):
    if not text_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File is not open, text_id = {text_id}",
        )
    lemma = await LemmaRepository.add_one(
        SLemmaAddDb(
            lemma=new_lemma.lemma,
            morph=new_lemma.morph,
            role=new_lemma.morph,
            word=new_lemma.word,
            text_id=text_id,
        ),
        session,
    )
    return lemma
