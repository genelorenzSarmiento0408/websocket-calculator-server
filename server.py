#!/usr/bin/env python

import asyncio
import websockets
from json import loads, dumps

async def reducer(websocket):
    async for message in websocket:
        loaded_message = loads(message)
        current_item = {
            "currentValue": loaded_message["currentValue"],
            "ok": True,
            "err": None
        }
        try:
            if loaded_message["type"] == "add":
                current_item["currentValue"] += loaded_message["value"]
            elif loaded_message["type"] == "minus":
                current_item["currentValue"] -= loaded_message["value"]
            else:
                current_item["ok"] = False
                current_item["err"] = "Invalid operation"
        except KeyError:
            current_item["ok"] = False
            current_item["err"] = "Wrong object sent"
        print(f"{current_item}")
        await websocket.send(dumps(current_item))

async def main():
    async with websockets.serve(reducer):
        await asyncio.Future()  # run forever

asyncio.run(main())
