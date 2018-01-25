import weakref
from math import hypot
from gameobject import GameObject
import pyglet

class Target(GameObject):
  def __init__(self, position=(0,0), batch=None):  
    self.x, self.y = position
    self.init_drawing(batch)
    super().__init__()

  def init_drawing(self, batch):
    self.image = pyglet.resource.image('ball_5.png')
    self.image.anchor_x = self.image.width // 2
    self.image.anchor_y = self.image.height // 2
    self.sprite = pyglet.sprite.Sprite(img=self.image, x=self.x, y=self.y, batch=batch)
  
  def update(self):
    self.sprite.x = self.x
    self.sprite.y = self.y
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