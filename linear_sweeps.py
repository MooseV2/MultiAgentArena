from itertools import permutations, product, combinations_with_replacement
import operator
from math import sqrt
from collections import deque
from random import randrange
import json
from statistics import stdev

def dist(start, end):
  sx, sy = start
  ex, ey = end
  return abs(ex - sx) + abs(ey - sy)


def get_best_order(players, regions):
    agentdist = lambda item: dist(item[0], item[1].pos)
    best_option = []
    best_option_cost = 1e5 # Some big number
    for order_a in permutations(range(5), 5):
        for order_b in product(range(2), repeat=5):
            option = list(zip([regions[a][b] for a,b in zip(order_a, order_b)], players))
            cost = sum(map(agentdist, option))
            if cost < best_option_cost: # New best option
                best_option = option
                best_option_cost = cost
    return best_option
                
w,h = 100,100

start_regions = [
  [(0,0)], # TL
  [(w-1,0)], # TR
  [(0,h-1)], # BL
  [(w-1,h-1)], # BR
  [((w-1)//2,(h-1)//2)], # C
]

regions = [
    [(90,90), (30,30)],
    [(40,40), (50,50)],
    [(2,2), (90,10)],
    [(10,90), (400,100)],
    [(4,4), (50,30)],
]


class Agent:
    _count = 0
    def __init__(self, x, y, goal=None):
        self.pos = (x,y)
        self.goal_q = []
        self.goal = goal
        self.id = Agent._count
        Agent._count += 1
        self.history = [self.pos]
        self.targets = [(randrange(0, 100), randrange(0, 100)) for _ in range(5)]
        self.steps_taken = -1
        self.happiness = []
    
    def get_targets(self):
        return [{
            "X": x,
            "Y": y
        } for x,y in self.targets]

    def add_goal(self, pos):
        self.goal_q.insert(0, pos)

    def move(self):
        self.targets = list(filter(lambda x: dist(self.pos, x) >= 10, self.targets))
        self.steps_taken = len(self.history)
        if len(self.targets) == 0:
            print(f"Agent {self.id} done in {self.steps_taken} steps.")
            return 1

        if self.goal == None:
            self.goal = self.goal_q.pop() if len(self.goal_q) > 0 else None
        if self.goal:
            self.pos = move_to_direct(*self.pos, *self.goal)
        
        if self.pos == self.goal:
            self.goal = None
        
        self.history.append(self.pos)
        self.happiness.append((5 - len(self.targets))/(len(self.history) + 1))
        return 0

    def __repr__(self):
        return f'A[{self.id}]({self.pos[0]},{self.pos[1]}) -> {self.goal}'



# print(get_best_order(players, regions))

def move_to(sx, sy, ex, ey):
    d_x = ex-sx
    d_y = ey-sy
    dist = sqrt(d_x**2 + d_y**2)
    if dist > 1:
        return (
            sx + d_x/dist,
            sy + d_y/dist,
        )
    else:
        return (ex, ey)

def move_to_direct(sx, sy, ex, ey):
    if sx < ex:
        sx += 1
    elif sx > ex:
        sx -= 1
    elif sy < ey:
        sy += 1
    elif sy > ey:
        sy -= 1
    return (sx, sy)

def zamboni_sweep(players):
    nplayers = len(players)
    start_regions = [
        [(10, y), (w-10, y)] for y in map(lambda x: h/nplayers * x + 10, range(nplayers))
    ]
    def add_remaining_goals(agent):
        remaining_goals = list(agent.targets)
        while remaining_goals:
            gdist = lambda goal: dist(agent.goal_q[0], goal)
            goal = min(remaining_goals, key=gdist)
            agent.add_goal(goal)
            remaining_goals.remove(goal)
    for order in get_best_order(players, start_regions):
        order[1].add_goal(order[0])
        order[1].add_goal((w-order[0][0], order[0][1]))
        add_remaining_goals(order[1])
    
    while True:
        if sum([agent.move() for agent in players]) == 5:
            break

def zamboni_sweep_comp(players):
    nplayers = len(players)
    start_regions = [
        [(10, y), (w-10, y)] for y in map(lambda x: h/nplayers * x + 10, range(nplayers))
    ]
    def add_remaining_goals(agent):
        remaining_goals = list(agent.targets)
        while remaining_goals:
            gdist = lambda goal: dist(agent.goal_q[0], goal)
            goal = min(remaining_goals, key=gdist)
            agent.add_goal(goal)
            remaining_goals.remove(goal)
    def get_distance(agent):
        goals = [agent.pos]
        goals.extend(agent.targets)
        distance = 0
        for i in range(len(goals)-1):
            distance += dist(goals[i], goals[i+1])
        return distance
        
    runners = zip([x.id for x in players], [get_distance(x) for x in players])
    runner = min(runners, key=operator.itemgetter(1))[0]
    for order in get_best_order(players, start_regions):
        order[1].add_goal(order[0])
        order[1].add_goal((w-order[0][0], order[0][1]))
        if order[1].id == runner: add_remaining_goals(order[1])
        # runner.append((order[1], get_distance(order[1])))
    
    # for agent in filter(lambda x: x.id != min(runner, key=operator.itemgetter(1))[0].id, players):
    #     print("Remove ", agent.id)
    #     del agent.goal_q[2:]
    #     print(len(agent.goal_q))
    
    while True:
        if sum([agent.move() for agent in players]) == 1:
            break


def sweep(fn, name):
    global itn
    Agent._count = 0
    players = [
        Agent(randrange(0,100), randrange(0,100)) for _ in range(5)
    ]
    data = []
    line = []
    targets = []
    for player in players:
        line.append({
            "X": player.pos[0],
            "Y": player.pos[1],
            "Targets": player.get_targets()
        })
    data.append(line)

    fn(players)

    for i in range(max([len(x.history) for x in players])):
        line = []
        for agent in players:
            k = i
            if k >= len(agent.history):
                k = len(agent.history)-1
            x = agent.history[k][0]
            y = agent.history[k][1]
            line.append({
                "X": x,
                "Y": y
            })
        data.append(line)

    if name:
        with open(f'{name}.txt', "w") as f:
            json.dump(data, f, indent=True)

    csv = ""
    steps = 0
    for agent in players:
        # # a= Scenario number (1,2 or 3)
        d_a = 2 # collaboration
        # # b. b= Iteration number
        d_b = itn
        # # c. c= Agent number
        d_c = agent.id
        # # d. d= Number of collected targets by the agent
        d_d = 5 - len(agent.targets)
        # # e. e= Number of steps taken by the agent at the end of iteration
        d_e = agent.steps_taken
        steps += d_e
        # # f. Agent happiness: f=d/(e+1)
        d_f = agent.happiness[-1]
        # d_f = d_d/(d_e+1)
        # # g. g= Maximum happiness in each iteration
        d_g = max(agent.happiness)
        # # h. h= Minimum happiness in each iteration
        d_h = min(agent.happiness)
        # # i. i= Average happiness in each iteration
        d_i = sum(agent.happiness) / len(agent.happiness)
        # # j. j= Standard deviation of happiness in each iteration 
        d_j = stdev(agent.happiness)
        # k. Agent competitiveness: k=(f-h)/(g-h)
        try:
            d_k = (d_f - d_h) / (d_g-d_h)
        except:
            d_k = -1
        csv += "\n" + ",".join([str(x) for x in [d_a, d_b, d_c, d_d, d_e, d_f, d_g, d_h, d_i, d_j, d_k]])

    if steps < (255*5):
        itn += 1
        with open(f'{name}.csv', 'a') as f:
            f.write(csv)

itn = 0
while itn < 25:
    sweep(zamboni_sweep_comp, "zamboni_comp")
    