import weakref
from math import hypot
from gameobject import GameObject
import json

class Target(GameObject):
  def __init__(self, data_channel, position=(0,0), batch=None):  
    self.x, self.y = position
    super().__init__()
    data = json.dumps({'cmd':'create', 'type': 'Target', 'id': self.id, 'args':{'x': self.x, 'y': self.y}})
    data_channel.send(data)

  def update(self):
    nearby = self.get_nearby()
    if nearby:
      print(nearby)
  
  def get_nearby(self, r=10):
    def get_distance(x0, y0, x1, y1):
      return hypot(x1 - x0, y1 - y0)

    nearby = []
    for obj in Target.getinstances(exclude=self):
      if get_distance(self.x, self.y, obj.x, obj.y) < r:
        nearby.append([obj.x, obj.y, obj])
    return nearby