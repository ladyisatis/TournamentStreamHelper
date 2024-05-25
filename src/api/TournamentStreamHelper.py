from aiohttp import web
import weakref
import os
import json
import asyncio

class TournamentStreamHelper:
    def __init__(self, app):
        self.app = app
        self.programState = {}
        self.version = '?'
        self.host = '0.0.0.0'
        self.port = '3000'

        self.tasks = web.AppKey('tasks', set)
        app[self.tasks] = set()

        self.websockets = web.AppKey('websockets', set)
        app[self.websockets] = set()
        app.on_shutdown.append(self.on_shutdown)
        
        if not os.path.exists('./user_data/games'):
            os.makedirs('./user_data/games')

    async def on_shutdown(self, app):
        for ws in app[self.websockets]:
            await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')

        for task in app[self.tasks]:
            task.cancel()

    async def add_task(self, task):
        t = asyncio.create_task(task)
        self.tasks.add(t)
        t.add_done_callback(self.tasks.discard)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        request.app[self.websockets].add(ws)
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await add_task(self.process(ws, msg.data))
                elif message.type == WSMsgType.CLOSE:
                    break
                elif message.type == WSMsgType.ERROR:
                    print(ws.exception())
                    break
        finally:
            request.app[websockets].discard(ws)

        return ws

    async def websocket_broadcast(self, msg):
        async for ws in self.app[self.websockets]:
            await ws.send_str(msg)

    async def index_context(self):
        try:
            async with aiofiles.open('./assets/versions.json', encoding='utf-8', mode='r') as f:
                version = json.loads(await f.readall()).get('program', '?')
        except:
            version = '?'

        return {'name': 'TournamentStreamHelper', 'version': version}

    async def process(self, ws, data):
        print(data)
