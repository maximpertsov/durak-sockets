from os import environ

from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.middleware.cors import CORSMiddleware

broadcast = Broadcast(environ.get("REDISCLOUD_URL", "redis://localhost:6379"))
app = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])

origins = [
    "http://localhost:3000",
    "https://xchi.online",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def room_ws(websocket: WebSocket):
    await websocket.accept()
    await run_until_first_complete(
        (room_ws_receiver, {"websocket": websocket}),
        (room_ws_sender, {"websocket": websocket}),
    )


async def room_ws_receiver(websocket: WebSocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="room", message=message)


async def room_ws_sender(websocket: WebSocket):
    async with broadcast.subscribe(channel="room") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)
