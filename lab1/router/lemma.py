from database import SessionDep
from schemas.lemma import SLemmaAdd, SLemmaAddDb, SLemmaUpdate, SLemmaResponse
from schemas.text import STextAdd, STextUpdate, STextResponse
from fastapi import APIRouter, status, HTTPException, UploadFile, Request, Form
from repository import LemmaRepository, TextRepository
from processers.processing import DocReader
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter(prefix="/text/{text_id}/lemma", tags=["Леммы"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def get_all(
    session: SessionDep, 
    text_id: int, 
    request: Request
):
    current_text = await TextRepository.get_one(text_id, session)
    lemmas = await LemmaRepository.get_all(text_id, session)
    return templates.TemplateResponse(
        "lemma_index.html", 
        {
            "request": request, 
            "lemmas": lemmas, 
            "text": current_text,
            "text_id": text_id
        }
    )

@router.get("/filter", response_class=RedirectResponse)
async def add_one(
    session: SessionDep,
    text_id: int,
    request: Request,
    morph: str
):
    lemmas = await LemmaRepository.filter(text_id,morph,session)
    current_text = await TextRepository.get_one(text_id,session)
    return templates.TemplateResponse(
        "lemma_index.html", 
        {
            "request": request, 
            "lemmas": lemmas, 
            "text": current_text,
            "text_id": text_id
        }
    )

@router.post("/add", response_class=RedirectResponse)
async def add_one(
    session: SessionDep,
    text_id: int,
    word: str = Form(...),
    lemma: str = Form(...),
    morph: str = Form(...),
    role: str = Form(...),
):
    await LemmaRepository.add_one(
        SLemmaAddDb(
            lemma=lemma,
            morph=morph,
            role=role,
            word=word,
            text_id=text_id,
        ),
        session,
    )
    return RedirectResponse(
        f"/text/{text_id}/lemma/",
        status_code=status.HTTP_303_SEE_OTHER
    )

@router.post("/delete/{id}", response_class=RedirectResponse)
async def delete(
    id: int, 
    text_id: int, 
    session: SessionDep
):
    await LemmaRepository.delete_one(id, session)
    return RedirectResponse(
        f"/text/{text_id}/lemma/", 
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/update/{id}", response_class=RedirectResponse)
async def update(
    id: int,
    text_id: int, 
    session: SessionDep,
    lemma: str = Form(...),
    morph: str = Form(...),
    role: str = Form(...),
):
    new_lemma = SLemmaUpdate(lemma=lemma, morph=morph, role=role)
    lemma = await LemmaRepository.update_one(id, new_lemma, session)
    if not lemma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lemma with id {id} not found",
        )
    return RedirectResponse(
        f"/text/{text_id}/lemma/",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/{id}", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def get_one(
    id: int, 
    text_id: int, 
    session: SessionDep, 
    request: Request
):
    lemma = await LemmaRepository.get_one(id, session)
    if not lemma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lemma with id {id} not found",
        )
    return templates.TemplateResponse(
        "lemma_edit.html", 
        {
            "request": request, 
            "lemma": lemma, 
            "text_id": text_id
        }
    )
