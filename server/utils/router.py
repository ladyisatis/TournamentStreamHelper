import orjson
from functools import partial
from server import app

async def on_socketio_event(sid, data, func):
    parsed = orjson.loads(data)
    await func(**parsed, session_id=sid)

def method(*args, **kwargs):
    def wrapper(func):
        # Remove session id for APIRouter
        del kwargs["session_id"]

        # Remove Socketio Event ID
        id = kwargs.get("id", "")
        del kwargs["id"]

        # Remove Socketio extra params
        handler = kwargs.get("handler", None)
        del kwargs["handler"]
        namespace = kwargs.get("namespace", None)
        del kwargs["namespace"]

        # Call router.get() with async func
        router = args[0]
        router(*args[1:], **kwargs)(func)

        if id != "":
            app.socketio.on(
                id, 
                handler=handler, 
                namespace=namespace
            )(partial(
                on_socketio_event,
                func=func
            ))

    return wrapper