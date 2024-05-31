import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from server import config, socketio

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    sys.stderr = open('./assets/log_error.txt', 'w', encoding='utf-8')
    sys.stdout = open('./assets/log.txt', 'w', encoding='utf-8')

app = FastAPI()
app.socketio = socketio.SocketIO(app=app)
templates = Jinja2Templates(directory='./dist')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "program_name": config.program_name(),
            "program_version": config.program_version()
        }
    )

app.mount("/assets", StaticFiles(directory="./dist/assets"), name="assets")