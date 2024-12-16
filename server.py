import socketio
import asyncio
from utils.buscarVentas import buscarVentas
server = socketio.AsyncServer(logger=True, async_mode = 'asgi')
app = socketio.ASGIApp(server)


class ServerNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.namespace = namespace

    async def on_connect(self, sid, environ):
        print('i connect')

    
    async def on_welcome(self, sid, data):
        print('Welcome user', data)

server.register_namespace(ServerNamespace('/'))
server.start_background_task(buscarVentas, server=server)      


async def run_server():
    import uvicorn
    await asyncio.sleep(2)
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
    

if __name__ == '__main__':
    asyncio.run(run_server())
    
    