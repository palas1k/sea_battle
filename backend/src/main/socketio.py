import socketio
from fastapi import FastAPI
from socketio import AsyncServer


def setup_socketio(api_prefix: str, fastapi: FastAPI) -> AsyncServer:
    server = socketio.AsyncServer(cors_allowed_origins="*", cors_credentials=True, engineio_logger=False, )

    app = socketio.ASGIApp(server)

    fastapi.mount(api_prefix, app, name="Socket IO")
    return server
