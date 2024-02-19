from src.presentation.socketio.di import DishkaAsyncNamespace, inject


class Namespace(DishkaAsyncNamespace):
    @inject
    async def on_connect(self, sid, environ, ):
        await self.enter_room(sid)
