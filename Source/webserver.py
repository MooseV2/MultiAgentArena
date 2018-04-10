import asyncio
import websockets
from threading import Thread
from queue import Queue
import json

class WebServer:
    def __init__(self, server=('localhost', 8765)):
        self.HOST, self.PORT = server
        self.send_queue = Queue()
        worker_loop = asyncio.new_event_loop()
        worker_thread = Thread(target=self.start_loop, args=(worker_loop,))
        worker_thread.start()
        self.recv = print

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.producer_handler, self.HOST, self.PORT)
        loop.run_until_complete(start_server)
        loop.run_forever()

    async def send_message(self, websocket):
        if not self.send_queue.empty():
            return str(self.send_queue.get())
        else:
            return None
        
    async def recv_message(self, message):
        message = json.loads(message)
        if message['cmd'] == 'connected':
            print('Client connected')
        else:
            print(message)
    async def producer_handler(self, websocket, path=''):
        while True:
            message = await self.send_message(websocket)
            if message: # Send outgoing messages first
                await websocket.send(message)
            else: # Start receiving incoming messages
                await websocket.send("REQ") # Tell client that we're ready to receive
                message = await websocket.recv()
                if message == 'DONE': # If the client is done sending
                    await asyncio.sleep(1) # Wait 1 second before asking again
                else:
                    await self.recv_message(message) # Parse message

    def send(self, data):
        print(f'Sending data [{data}]')
        self.send_queue.put(data) # Will be sent soon