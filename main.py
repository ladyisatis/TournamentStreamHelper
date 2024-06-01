import sys
import multiprocessing
import uvicorn
from socketio import ASGIApp
from server import app, config
from loguru import logger

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()

    try:
        logger.info("Server is starting")
        uvicorn.run(ASGIApp(app.socketio, app), host=config.host(), 
            port=config.port(), reload=config.reload())
        sys.exit(0)
    except:
        logger.exception("exiting application")
        sys.exit(1)