import sys
from jinja2 import FileSystemLoader
from aiohttp import web, WSCloseCode, WSMsgType
from aiohttp_jinja2 import render_template
from src.api.TournamentStreamHelper import TournamentStreamHelper

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    sys.stderr = open('./assets/log_error.txt', 'w', encoding='utf-8')
    sys.stdout = open('./assets/log.txt', 'w', encoding='utf-8')

def main():
    app = web.Application()
    TSH = TournamentStreamHelper(app)

    async def root_handler(request):
        context = await TSH.index_context()
        response = render_template('index.html', request, context)
        return response

    aiohttp_jinja2.setup(app, loader=FileSystemLoader('./web/dist'))

    app.add_routes([web.get('/ws', TSH.websocket_handler)])
    app.add_routes([web.static('/assets', './web/dist/assets')])
    app.add_routes([web.get('/', root_handler)])

    web.run_app(app, host=TSH.host, port=TSH.port)
    return 0
