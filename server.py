import asyncio
import datetime
import json

import aiocoap
import aiocoap.resource as resource

import requests

class TimeResource(resource.ObservableResource):
    
    def __init__(self):
        super().__init__()

        self.handle = None

    async def render_get(self, request):

        print("received get request for time")
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").encode('ascii')

        return aiocoap.Message(payload=payload) 


class DataResource(resource.Resource):
    
    def __init__(self):
        super().__init__()

        self.content = "content"

    async def render_post(self, request):

        data = json.loads(request.payload)

        print(data)

        response = requests.post("https://localhost:3000", json=data)

        print(response)


        return aiocoap.Message(code=aiocoap.CREATED, payload=request.payload)

async def main():
    root = resource.Site()

    root.add_resource(['time'], TimeResource())
    root.add_resource(['data'], DataResource())

    print(root)

    await aiocoap.Context.create_server_context(root, bind= ("localhost", 8000), transports=['udp6'])

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())