from database import SessionDep
from schemas.lemma import SLemmaAdd,SLemmaAddDb, SLemmaUpdate, SLemmaResponse
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile, Request, Depends
from repository import LemmaRepository, TextRepository
from processing import DocReader
from typing import List

router = APIRouter(prefix="/lemma", tags=["Леммы"])

def get_text_id_from_cookie(request: Request):
    text_id_cookie = request.cookies.get("current_text_id")
    return int(text_id_cookie) if text_id_cookie else None

@router.get('/', response_model=List[SLemmaResponse], status_code=status.HTTP_200_OK)
async def get_all(session:SessionDep, text_id:int|None = Depends(get_text_id_from_cookie)):
    if not text_id:
        return []
    lemmas = await LemmaRepository.get_all(text_id, session)
    return lemmas
    
@router.post('/', response_model=SLemmaAdd, status_code=status.HTTP_201_CREATED)
async def add_one(new_lemma: SLemmaAdd, session:SessionDep, text_id:int|None = Depends(get_text_id_from_cookie)):
    if not text_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'File is not open, text_id = {text_id}')
    lemma = await LemmaRepository.add_one(SLemmaAddDb(lemma=new_lemma.lemma,
                                        morph=new_lemma.morph,
                                        role=new_lemma.morph,
                                        word=new_lemma.word,
                                        text_id=text_id),
                                        session)
    return lemma