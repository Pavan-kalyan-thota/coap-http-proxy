import logging
import asyncio
import json
import datetime

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    data = {
            "id": "0001",
            "type": "fluctuation",
            "temp": "69",
            "time-stamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "location": "Bloomington" 

    }

    payload = json.dumps(data).encode("utf-8")

    #payload = b"The quick brown fox jumps over the lazy dog.\n" * 30
    request = Message(code=POST, payload=payload, uri="coap://localhost:8000/data")

    response = await context.request(request).response

    print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main())