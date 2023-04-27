import logging
import asyncio
import json
import datetime
import random

from aiocoap import *

logging.basicConfig(level=logging.INFO)

def get_random():
    return random.randint(1, 3)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    low_limit = 60

    high_limit = 90

    data = {
            "id": "0001",
            "type": "start",
            "temp": 70.0,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "location": "Bloomington" 

    }

    payload = json.dumps(data).encode("utf-8")

    size = len(payload)

    sent_size = size

    last_temp = data["temp"]

    request = Message(code=POST, payload=payload, uri="coap://localhost:8000/data")

    response = await context.request(request).response
    
    print('Result: %s\n%r'%(response.code, response.payload))

    SIZE = 1024 * 1024

    while size < SIZE:

        r = get_random()

        if r == 1:
            data["temp"] -= .10

        if r == 2:
            data["temp"] += .10

        data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if abs(last_temp - data["temp"]) >= 1:
            last_temp = data["temp"]
            data["type"] = "fluctuation"

            data["temp"] = round(data["temp"], 2)

            if data["temp"] < low_limit or data["temp"] > high_limit:
                data["type"] = "warning"

            payload = json.dumps(data).encode("utf-8")

            request = Message(code=POST, payload=payload, uri="coap://localhost:8000/data")

            response = await context.request(request).response
    
            print('Result: %s\n%r'%(response.code, response.payload))

            sent_size += len(payload)

        payload = json.dumps(data).encode("utf-8")

        size += len(payload)
    
    print(size, sent_size)



if __name__ == "__main__":
    asyncio.run(main())