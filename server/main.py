import aiofiles
import aiofiles.os
import aiofiles.ospath
import tomllib

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from socketio import AsyncServer

from server import settings

program_context = {
    "name": "TournamentStreamHelper",
    "version": "?",
    "description": "",
    "authors": []
}

async def on_startup(app: FastAPI):
    async with aiofiles.open('pyproject.toml', mode='r', encoding='utf-8') as f:
        program_context = tomllib.loads(await f.read())["tool"]["poetry"]

async def on_shutdown(app: FastAPI):
    await settings.save()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup(app)
    yield
    await on_shutdown(app)

app = FastAPI(lifespan=lifespan)
app.socketio = AsyncServer(async_mode='asgi')
templates = Jinja2Templates(directory='./dist')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=program_context
    )

app.mount("/assets", StaticFiles(directory="./dist/assets"), name="assets")