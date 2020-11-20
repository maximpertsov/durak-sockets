from os import environ

from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.middleware.cors import CORSMiddleware
from lib import durak

broadcast = Broadcast(environ.get("REDISCLOUD_URL", "redis://localhost:6379"))
app = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])

origins = [
    "http://localhost:3002",
    "http://localhost:3003",
    "https://xchi.online",
    "https://xdurak.xyz",
    "https://maximpertsov.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def status():
    return {"status": "ok"}


@app.websocket("/ws/{channel}")
async def channel_ws(websocket: WebSocket, channel: str):
    await websocket.accept()
    await run_until_first_complete(
        (channel_ws_receiver, {"websocket": websocket, "channel": channel}),
        (channel_ws_sender, {"websocket": websocket, "channel": channel}),
    )


async def channel_ws_receiver(websocket: WebSocket, channel: str):
    async for message in websocket.iter_text():
        await broadcast.publish(
            channel=channel, message=await handle_message(channel, message)
        )


async def channel_ws_sender(websocket: WebSocket, channel: str):
    async with broadcast.subscribe(channel=channel) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


async def handle_message(channel: str, message):
    if channel == "durak":
        return await durak.handle_message(message)

    return message
