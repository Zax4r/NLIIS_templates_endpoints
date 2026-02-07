from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaUpdate, SLemmaResponse
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile
from repository import LemmaRepository, TextRepository
from processing import DocReader


router = APIRouter(prefix="/text", tags=["Тексты"])


@router.get("/{id}", response_model=STextResponse, status_code=status.HTTP_200_OK)
async def get_text(id: int, session: SessionDep):
    text = await TextRepository.get_one(id, session)
    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with id {id} not found"
        )
    return text

@router.post('/add',response_model=STextResponse, status_code=status.HTTP_201_CREATED)
async def add_text(new_text: UploadFile, session: SessionDep):
    all_words = await DocReader.read_doc(new_text.file)
    text_add = STextAdd(name=new_text.filename, text=all_words)
    text = await TextRepository.add_one(text_add, session)
    return text
    

