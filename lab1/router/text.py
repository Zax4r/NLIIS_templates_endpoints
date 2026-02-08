from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaUpdate, SLemmaResponse, SLemmaAddDb
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile, Response
from repository import LemmaRepository, TextRepository
from processers.processing import DocReader, Processer
from typing import List
router = APIRouter(prefix="/text", tags=["Тексты"])

@router.get('/all', response_model=List[STextResponse], status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep):
    all_texts = await TextRepository.get_all(session)
    return all_texts

@router.delete('/delete/{id}', response_model=STextResponse|None, status_code=status.HTTP_200_OK)
async def delete_one(id:int, session: SessionDep):
    await TextRepository.delete_one(id,session)
    await LemmaRepository.delete_all(id,session)
    return None

@router.put('/update/{id}', response_model=STextResponse, status_code=status.HTTP_200_OK)
async def update_one(id:int,new_text: STextUpdate, session: SessionDep):
    text = await TextRepository.update_text(id,new_text,session)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with id {id} not found"
        )
    return text

@router.get("/{id}", response_model=STextResponse, status_code=status.HTTP_200_OK)
async def get_text(id: int, session: SessionDep, response: Response):
    text = await TextRepository.get_one(id, session)
    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with id {id} not found"
        )

    response.set_cookie(key="current_text_id", value=str(text.id))
    return text


@router.post("/add", response_model=STextResponse, status_code=status.HTTP_201_CREATED)
async def add_text(new_text: UploadFile, session: SessionDep, response: Response):
    all_words = await DocReader.read_doc(new_text.filename,new_text.file)
    text_add = STextAdd(name=new_text.filename, text=all_words)
    text = await TextRepository.add_one(text_add, session)
    for lemma_dic in Processer.process(all_words, 'mapping/dep_rules.json', 'mapping/morph_rules.json'):
        await LemmaRepository.add_one(SLemmaAddDb(**lemma_dic,text_id=text.id), session)

    response.set_cookie(key="current_text_id",value=str(text.id))
    return text
