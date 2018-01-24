# MultiAgentArena
Implementation of a multi-agent system with group pathfinding objectives.


# Rules

**Environment**: a 10 m x 10 m field

* Five agents (A,B,C,D,E) can move up and down and left and right, one centimeter in every step.
* For each agent, there are five target objects to collect. For example for agent A the target
objects are TA1 to TA5.
* Whenever a relevant object (for example TA3) is reachable by its related agent, the object is
considered as collected and will disappear from the field.
* All object are randomly scattered all over the field. Agents don’t know the location of none of
the objects.
* Agents have location sensor (x,y).
* Every agent has a Radar to sense objects or other agents. The Radar can sense the type (which
agent belongs to) and locate every object or agent in 10 centimeter radius. Whenever an agent
locates an object (or agent), it will receive the coordinates (x,y) of the object (or agent).
* An object (or agent) is reachable by an agent if it falls into its Radar range.
* Every agent has two communication channels: First is a public channel for broadcasting. In
broadcast mode, the message sent by an agent will be received by all other agents. Second, a
private channel to send private messages to a specific agent.
* In both channel, agents can send any type of message but a mandatory message will be sent in
broadcast mode by an agent that collected its all target object.
* Agents avoid colliding each other. They will never remain reachable by other agents.


# Implement the following scenarios: 

Scenario 1: Completion
----------------------

* The game will be over as soon as one of the agents collects all its objects.
* Only public communication channel is open for all agents. The private channels are closed.

Scenario 2: Collaboration
-------------------------

* The game is not over until all agents collect their own target objects.
* Both public and private channels are open. Example of a private communication: Agent A
encounters object TB1. It may or may not notify the object B the location of TB1. 

Scenario 3: Compassionate agents
--------------------------------

* The game will be over as soon as one of the agents collects all its objects.
* Both public and private channels are open. Example of a private communication: Agent A
encounters object TB1. It may or may not notify the object B the location of TB1.