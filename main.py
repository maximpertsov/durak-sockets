import json
from copy import deepcopy
from os import environ

import requests
from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.middleware.cors import CORSMiddleware

from lib.durak import (attack, attack_with_many, collect, defend, pass_card,
                       yield_attack)

BASE_API_URL = environ.get("BASE_API_URL", "http://localhost:8000/api")
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


actions = {
    "attacked": attack,
    "attacked_with_many": attack_with_many,
    "defended": defend,
    "yielded_attack": yield_attack,
    "collected": collect,
    "passed": pass_card,
}


async def transform_and_persist(message):
    data = json.loads(message)

    # transform
    if data["type"] in actions:
        data["to_state"] = actions[data["type"]](
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
    else:
        data["to_state"] = deepcopy(data["from_state"])

    # persist
    url = "{}/game/{}/events".format(BASE_API_URL, data["game"])
    # TODO: make this async with request_threads?
    requests.post(url, json=data)

    return json.dumps(data)
