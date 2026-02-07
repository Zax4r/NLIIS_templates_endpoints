from fastapi import FastAPI
from router import text
from contextlib import asynccontextmanager
from database import Base, engine



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(text.router)

