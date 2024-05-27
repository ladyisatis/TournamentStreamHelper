from socketio import AsyncServer, ASGIApp
from fastapi import FastAPI

class SocketIO(AsyncServer):
    def __init__(self, app: FastAPI, allowed_origins: union[str, list] = '*', **kwargs):
        super.__init__(async_mode="asgi", cors_allowed_origins=allowed_origins, **kwargs)
        app.mount("/ws", ASGIApp(socketio_server=self, socketio_path="socket.io"))

    def is_asyncio_based(self) -> bool:
        return True