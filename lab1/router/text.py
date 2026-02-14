from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaUpdate, SLemmaResponse, SLemmaAddDb
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile, Response, Request
from repository import LemmaRepository, TextRepository
from processers.processing import DocReader, Processer
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


router = APIRouter(prefix="/text", tags=["Тексты"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
@router.get("/all", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def get_all(session: SessionDep, request: Request):
    all_texts = await TextRepository.get_all(session)
    return templates.TemplateResponse(
        "text_index.html", {"request": request, "texts": all_texts}
    )


@router.post("/delete/{id}", response_class=HTMLResponse)
async def delete_one(id: int, session: SessionDep, response: Response):
    await TextRepository.delete_one(id, session)
    await LemmaRepository.delete_all(id, session)

    return RedirectResponse("/text/all", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/add", response_model=STextResponse, status_code=status.HTTP_201_CREATED)
async def add_text(new_text: UploadFile, session: SessionDep, response: Response):
    all_words = await DocReader.read_doc(new_text.filename, new_text.file)
    text_add = STextAdd(name=new_text.filename, text=all_words)
    text = await TextRepository.add_one(text_add, session)
    for lemma_dic in Processer.process(
        all_words, "mapping/dep_rules.json", "mapping/morph_rules.json"
    ):
        await LemmaRepository.add_one(
            SLemmaAddDb(**lemma_dic, text_id=text.id), session
        )

    return RedirectResponse("/text/all", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{id}", response_model=STextResponse, status_code=status.HTTP_200_OK)
async def get_text(id: int, session: SessionDep, response: Response, request: Request):
    text = await TextRepository.get_one(id, session)
    if text is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Text with id {id} not found"
        )

    return templates.TemplateResponse(
        "text_detail.html", {"request": request, "text": text}
    )
