import asyncio
import datetime
import json

import aiocoap
import aiocoap.resource as resource

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


        return aiocoap.Message(code=aiocoap.CREATED, payload=request.payload)

class BlockResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""
    def __init__(self):
        super().__init__()
        self.set_content(b"This is the resource's default content. It is padded "
                b"with numbers to be large enough to trigger blockwise "
                b"transfer.\n")

    def set_content(self, content):
        self.content = content
        while len(self.content) <= 1024:
            self.content = self.content + b"0123456789\n"

    async def render_get(self, request):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)



async def main():
    root = resource.Site()

    root.add_resource(['time'], TimeResource())
    root.add_resource(['data'], DataResource())
    root.add_resource(['block'], BlockResource())

    await aiocoap.Context.create_server_context(root, bind= ["localhost", 8000])

    await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())