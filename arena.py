import pyglet
from agent import Agent
from comms import Communications
from targets import Target
from gameobject import GameObject
from webserver import WebServer
from time import sleep
pyglet.resource.path = ['./assets']
pyglet.resource.reindex()
arena_window = pyglet.window.Window(1000, 1000)
drawing_batch = pyglet.graphics.Batch()

def draw_gridlines(size, batch, spacing):
  width, height = size
  b = 200 # brightness
  for x in range(0, width, spacing):
    batch.add(2, pyglet.gl.GL_LINES, None, 
      ("v2f", (x, 0, x, width)),
      ("c3B", (b, b, b, b, b, b))
    )
  for y in range(0, height, spacing):
    batch.add(2, pyglet.gl.GL_LINES, None, 
      ("v2f", (0, y, height, y)),
      ("c3B", (b, b, b, b, b, b))
    )

draw_gridlines((arena_window.width, arena_window.height), drawing_batch, 10)

@arena_window.event
def on_draw():
  arena_window.clear()
  drawing_batch.draw()

def update(dt):
  for obj in Agent.getinstances():
    obj.update()

if __name__ == '__main__':
  print("Starting")
  sleep(3)
  data_channel = WebServer()
  comms_channel = Communications()
  k = []
  for i in range(5):
    data_channel.send(f'Creating agent {i} at {(i*100+50,200)}')
    k.append(Agent(comms_channel, position=(i*100+50,200), batch=drawing_batch))
  j = Target(position=(600,200), batch=drawing_batch)
  
  pyglet.clock.schedule_interval(update, 1/10.0)
  pyglet.app.run()