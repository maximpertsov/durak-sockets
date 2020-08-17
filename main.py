import json
from os import environ

import requests
from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.middleware.cors import CORSMiddleware

from lib.durak import attack, collect, defend, yield_attack

broadcast = Broadcast(environ.get("REDISCLOUD_URL", "redis://localhost:6379"))
app = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])

origins = [
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
            channel=channel, message=await transform_and_persist(message)
        )


async def channel_ws_sender(websocket: WebSocket, channel: str):
    async with broadcast.subscribe(channel=channel) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


async def transform_and_persist(message):
    data = json.loads(message)

    # transform
    if data["type"] == "attacked":
        data["to_state"] = attack(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
    if data["type"] == "defended":
        data["to_state"] = defend(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
    if data["type"] == "yielded_attack":
        data["to_state"] = yield_attack(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
    if data["type"] == "collected":
        data["to_state"] = collect(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )

    # persist
    url = "http://localhost:8000/api/game/{game}/events".format(**data)
    persist_data = {**data}
    persist_data.update(
        payload=json.dumps(data["payload"]),
        to_state=json.dumps(data.get("to_state", {})),
    )
    # TODO: make this async with request_threads?
    requests.post(url, persist_data)

    return json.dumps(data)
