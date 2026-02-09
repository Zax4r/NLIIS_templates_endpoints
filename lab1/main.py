from fastapi import FastAPI, status
from router import text, lemma
from contextlib import asynccontextmanager
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(text.router)
app.include_router(lemma.router)


@app.get("/")
async def index():
    return RedirectResponse("/text", status_code=status.HTTP_308_PERMANENT_REDIRECT)
