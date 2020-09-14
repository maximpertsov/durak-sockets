import json
from copy import deepcopy
from os import environ

import httpx
from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from fastapi.concurrency import run_until_first_complete
from fastapi.middleware.cors import CORSMiddleware

from lib.durak import (attack, attack_with_many, defend, give_up, pass_card,
                       pass_with_many, start_game, yield_attack)
from lib.durak.exceptions import IllegalAction

BASE_API_URL = environ.get("BASE_API_URL", "http://localhost:8000/api")
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
        return await handle_durak_message(message)

    return message


actions = {
    "started_game": start_game,
    "attacked": attack,
    "attacked_with_many": attack_with_many,
    "defended": defend,
    "gave_up": give_up,
    "passed": pass_card,
    "passed_with_many": pass_with_many,
    "yielded_attack": yield_attack,
}


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


async def handle_durak_message(message):
    data = json.loads(message)

    try:
        try:
            action = actions[data["type"]]
        except KeyError:
            raise IllegalAction
        data["to_state"] = action(
            from_state=data["from_state"], user=data["user"], payload=data["payload"]
        )
        await persist(data)
    except IllegalAction:
        data["to_state"] = deepcopy(data["from_state"])
        data["no_display"] = True

    del data["from_state"]
    return json.dumps(data, cls=MessageEncoder)


async def persist(data):
    async with httpx.AsyncClient() as client:
        await client.post(
            "{}/game/{}/events".format(BASE_API_URL, data["game"]),
            headers={"Content-Type": "application/json"},
            data=json.dumps(data, cls=MessageEncoder),
        )
