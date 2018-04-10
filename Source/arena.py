import pyglet
from agent import Agent
from comms import Communications
from targets import Target
from gameobject import GameObject
from webserver import WebServer
from time import sleep
import json

def update():
  for obj in Agent.getinstances():
    obj.y += 5
    obj.update()

if __name__ == '__main__':
  print("Starting")
  sleep(3)
  data_channel = WebServer()
  comms_channel = Communications()
  for i in range(5):
    a = Agent(comms_channel, data_channel, position=(i*30+30, 200))
    t = Target(data_channel, position=(i*30+30, 300))  

  for _ in range(10):
    sleep(2)
    update()