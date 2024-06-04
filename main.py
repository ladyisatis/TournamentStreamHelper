import sys
import multiprocessing
import asyncio

from hypercorn.config import Config
from hypercorn.asyncio import serve
from socketio import ASGIApp
from loguru import logger

from server import app, settings

async def main():
    logger.info("Server is starting")

    try:
        await settings.load()
        combined_app = ASGIApp(
            app.socketio,
            app
        )
        
        config = Config()
        host = settings.get("server.host")
        port = settings.get("server.port")
        config.bind = [f"{host}:{port}"]

        await serve(combined_app, config)
        return 0
    except:
        logger.exception("Exiting application due to exception")
        return 1

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        sys.stderr = open('./logs/tsh_error.txt', 'w', encoding='utf-8')
        sys.stdout = open('./logs/tsh_info.txt', 'w', encoding='utf-8')

    sys.exit(asyncio.run(main()))