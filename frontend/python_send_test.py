import asyncio
import websockets
from threading import Thread
from queue import Queue
class WebServer:
    def __init__(self, server=('localhost', 8765)):
        self.HOST, self.PORT = server
        self.data = Queue()
        worker_loop = asyncio.new_event_loop()
        self.worker_thread = Thread(target=self.start_loop, args=(worker_loop,))
        self.worker_thread.start()

    async def forward_messages(self, websocket, path):
        while True:
            while not self.data.empty():
                message = self.data.get()
                await websocket.send(str(message))
                # exception may be thrown here
                

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websockets.serve(self.forward_messages, self.HOST, self.PORT))
        loop.run_forever()
    
    def send(self, data):
        self.data.put(data) # Will be sent soon


from time import sleep
a = WebServer()

while True:
    sleep(1)
    print("zzz")
    a.send("Hello!")