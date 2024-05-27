import sys
import multiprocessing
import uvicorn
from server import config
from loguru import logger

if __name__ == '__main__':
    # Pyinstaller fix
    multiprocessing.freeze_support()

    try:
        uvicorn.run("server:app", host=config.host(), 
            port=config.port(), reload=config.reload())
        sys.exit(0)
    except:
        logger.exception("exiting application")
        sys.exit(1)