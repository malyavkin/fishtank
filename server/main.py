from aiohttp import web
import asyncio

state = {
    "count": 0
}

async def serve(loop):
    async def handler(request):
        return web.Response(text=str(state['count']))

    await loop.create_server(
        web.Server(handler), 
        "127.0.0.1", 8080)
    
    await asyncio.sleep(100*3600)

async def misc():
    while True:
        await asyncio.sleep(0.1)
        state['count'] += 1


ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(serve(ioloop)),
    ioloop.create_task(misc())
]
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()