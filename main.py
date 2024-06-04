import sys
import multiprocessing
import asyncio

from hypercorn.config import Config
from hypercorn.asyncio import serve
from socketio import ASGIApp
from loguru import logger

from server import settings, server

async def main():
    logger.add(
        "./logs/tsh_info.txt",
        format="[{time:YYYY-MM-DD HH:mm:ss}] - {level} - {file}:{function}:{line} | {message}",
        encoding="utf-8",
        level="INFO",
        rotation="20 MB"
    )

    logger.add(
        "./logs/tsh_error.txt",
        format="[{time:YYYY-MM-DD HH:mm:ss}] - {level} - {file}:{function}:{line} | {message}",
        encoding="utf-8",
        level="ERROR",
        rotation="20 MB"
    )

    logger.warning("Server is starting")

    await settings.load()

    config = Config()
    config.log.access_logger = logger.bind(name="access_logger")
    config.log.error_logger = logger.bind(name="error_logger")

    host = await settings.get("server.host")
    port = await settings.get("server.port")
    config.bind = [f"{host}:{port}"]

    await serve(
        app=ASGIApp(
            server.app.socketio,
            server.app
        ), 
        config=config, 
        mode='asgi'
    )
    return 0

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        sys.stderr = open('./logs/tsh_error.txt', 'w', encoding='utf-8')
        sys.stdout = open('./logs/tsh_info.txt', 'w', encoding='utf-8')

    ret = 0
    try:
        ret = asyncio.run(main())
    except asyncio.exceptions.CancelledError:
        pass
    except:
        logger.exception("Exiting application due to exception")
        sys.exit(1)
    finally:
        sys.exit(ret)