import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from socketio import AsyncServer
from server import config

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    sys.stderr = open('./assets/log_error.txt', 'w', encoding='utf-8')
    sys.stdout = open('./assets/log.txt', 'w', encoding='utf-8')

app = FastAPI()
app.socketio = AsyncServer(async_mode='asgi')
templates = Jinja2Templates(directory='./dist')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "name": config.program_name(),
            "version": config.program_version()
        }
    )

app.mount("/assets", StaticFiles(directory="./dist/assets"), name="assets")