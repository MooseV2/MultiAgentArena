import pyglet
from agent import Agent
from comms import Communications
from omniscience import Omniscience
from targets import Target
from gameobject import GameObject

pyglet.resource.path = ['./assets']
pyglet.resource.reindex()
arena_window = pyglet.window.Window(1000, 1000)
drawing_batch = pyglet.graphics.Batch()

@arena_window.event
def on_draw():
  arena_window.clear()  
  drawing_batch.draw()

def update(dt):
  for obj in Agent.getinstances():
    obj.update()

if __name__ == '__main__':
  print("Starting")
  comms_channel = Communications()
  k = []
  for i in range(5):
    print(f'Creating agent {i} at {(i*100+50,200)}')
    k.append(Agent(comms_channel, position=(i*100+50,200), batch=drawing_batch))
  j = Target(position=(600,200), batch=drawing_batch)
  
  pyglet.clock.schedule_interval(update, 1/120.0)
  pyglet.app.run()