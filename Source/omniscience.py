from agent import Agent
class Omniscience:
  @classmethod
  def get_nearby(cls):
    for agent in Agent.getinstances():
      print(agent.id)