import weakref
import pyglet
from math import hypot
from gameobject import GameObject
import json

class Agent(GameObject):
  def __init__(self, comms_channel, data_channel, position=(0,0)):
    self.x, self.y = position
    super().__init__()
    self.comms_channel = comms_channel
    self.comms_channel.add_client(self)
    self.data_channel = data_channel
    data = json.dumps({'cmd':'create', 'type': 'Agent', 'id': self.id, 'args':{'x': self.x, 'y': self.y}})
    self.data_channel.send(data)

  def update(self):
    data = json.dumps({'cmd':'move', 'id': self.id, 'args':{'x': self.x, 'y': self.y}})
    self.data_channel.send(data)
    nearby = self.get_nearby(GameObject)
    if nearby:
      print(nearby)
  
  def get_nearby(self, cls, r=10):
    def get_distance(x0, y0, x1, y1):
      return hypot(x1 - x0, y1 - y0)

    nearby = []
    for obj in cls.getinstances(exclude=self):
      if get_distance(self.x, self.y, obj.x, obj.y) < r:
        nearby.append([obj.x, obj.y, obj])
    return nearby
    
  def receive(self, message, sender_id):
    print(f'Agent [{self.id}]: Message from [{sender_id}]: \'{message}\'')
  
  def receive_broadcast(self, message, sender_id):
    print('Broadcast!!')
    self.receive(message, sender_id)

  def send(self, message, client_id):
    self.comms_channel.message_client(client_id, self.id, message)

  def send_broadcast(self, message):
    self.comms_channel.message_all(self.id, message)

  