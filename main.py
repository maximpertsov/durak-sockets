from broadcaster import Broadcast
from starlette.applications import Starlette
from starlette.concurrency import run_until_first_complete
from starlette.routing import WebSocketRoute

broadcast = Broadcast("redis://localhost:6379")


async def chatroom_ws(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket}),
    )


async def chatroom_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="chatroom", message=message)


async def chatroom_ws_sender(websocket):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


routes = [
    WebSocketRoute("/ws/chat", chatroom_ws, name="chat"),
]


app = Starlette(
    routes=routes, on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect],
)
