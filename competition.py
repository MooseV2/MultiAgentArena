import numpy as np
from math import hypot, inf
from pathfinding.core.node import Node

import json
import pandas as pd
import random
from random import shuffle

def start_positions(agents,scaler):

    starting_states = []
    for agent in agents:
        state = {"X":int(scaler*agent.x), "Y":int(scaler*agent.y),
                "Targets":[{"X":int(scaler*agent.targets[0][0]),"Y":int(scaler*agent.targets[0][1])},
                {"X":int(scaler*agent.targets[1][0]),"Y":int(scaler*agent.targets[1][1])},
                {"X":int(scaler*agent.targets[2][0]),"Y":int(scaler*agent.targets[2][1])},
                {"X":int(scaler*agent.targets[3][0]),"Y":int(scaler*agent.targets[3][1])},
                {"X":int(scaler*agent.targets[4][0]),"Y":int(scaler*agent.targets[4][1])},]}
        starting_states.append(state)
    return starting_states


def output_frontend(agents,scaler):

    agent_path = []
    for cnt,agent in enumerate(agents):
        state = {"X":int(scaler*agent.x),
                "Y":int(scaler*agent.y)}
        agent_path.append(state)
    return agent_path


def csv_writer(iteration,agent_no,agent):

    max_happ = max(agent.happiness_array)
    min_happ = min(agent.happiness_array)
    try:
        competitive =((agent.happiness-min_happ)/(max_happ-min_happ))
    except:
        competitive = -1

    data = {"A":1,
            "B":iteration,
            "C":agent_no,
            "D":agent.no_targets_collected,
            "E":agent.steps_taken,
            "F":agent.happiness,
            "G":max_happ,
            "H":min_happ,
            "I":np.mean(agent.happiness_array),
            "J":np.std(agent.happiness_array),
            "K":competitive}
    return data



class Agent():
    def __init__(self, target_type,targets,offset):
        self.x = random.randint(0,99)
        self.y = random.randint(0,99)
        self.offset = offset
        self.target_type = target_type
        self.no_targets_collected=0
        self.steps_taken=0
        self.happiness =0
        self.path =0
        self.targets = targets
        self.genrate_path()
        self.moves = [0,0]
        self.happiness_array = []



    def genrate_path(self):

        self.path =[Node(7+self.offset,7+self.offset),Node(7+self.offset,98+self.offset),Node(14+self.offset,98+self.offset),Node(14+self.offset,7+self.offset),
                    Node(21+self.offset,7+self.offset),Node(21+self.offset,98+self.offset),Node(28+self.offset,98+self.offset),Node(28+self.offset,7+self.offset),
                    Node(35+self.offset,7+self.offset),Node(35+self.offset,98+self.offset),Node(42+self.offset,98+self.offset),Node(42+self.offset,7+self.offset),
                    Node(49+self.offset,7+self.offset),Node(49+self.offset,98+self.offset),Node(56+self.offset,98+self.offset),Node(56+self.offset,7+self.offset),
                    Node(63+self.offset,7+self.offset),Node(63+self.offset,98+self.offset),Node(70+self.offset,98+self.offset),Node(70+self.offset,7+self.offset),
                    Node(77+self.offset,7+self.offset),Node(77+self.offset,98+self.offset),Node(84+self.offset,98+self.offset),Node(84+self.offset,7+self.offset),
                    Node(91+self.offset,7+self.offset),Node(91+self.offset,98+self.offset),Node(98+self.offset,98+self.offset),Node(98+self.offset,7+self.offset)]
        if random.random() < 0.9:
            shuffle(self.path)


    def prune_path(self,empty):
        self.path = [point for point in self.path if point not in empty]


    # def check_correctness(self):
    #     cnt = 0
    #     for step in self.path:
    #         for tar in self.targets:
    #             if step.x ==tar[0] and step.y == tar[1]:
    #                 cnt +=1
    #     if cnt == 5:
    #         print("All good")
    #     else:
    #         print("Problem with pathfinding path only contained ", cnt)


    def next_moves(self):
        try:
            movesX = self.path[0].x - self.x
            movesY = self.path[0].y - self.y
            self.path.pop(0)
            return [movesX,movesY]
        except:
            return[0,0]

    def check_targets(self, alltargets,r=10):
        for cnt,target in enumerate(self.targets):
            if hypot((target[0]-self.x),(target[1]-self.y))<=r:
                del self.targets[cnt]
                self.no_targets_collected +=1
                return False
            else:
                pass
        for target in alltargets:
            if hypot((target[0]-self.x),(target[1]-self.y))<r:
                return False
            else:
                pass
        return True

    def update(self):

        self.steps_taken +=1
        # self.prune_path(empty)
        self.happiness = (self.no_targets_collected/(self.steps_taken))
        self.happiness_array.append(self.happiness)

        if (self.moves[0] == 0 and self.moves[1]==0) :
            self.moves = self.next_moves()

        if self.moves[0] !=0:
            next_move = 1*np.sign(self.moves[0])
            self.moves[0] = self.moves[0] - next_move
            self.x += next_move

        elif self.moves[1] !=0:
            self.notleft = True
            next_move = 1*np.sign(self.moves[1])
            self.moves[1] = self.moves[1] - next_move
            self.y += next_move
        else:
            pass


def main():

    iterations = 25
    csv = []

    scaler = 1

    for iter_no in range(iterations):

        starting_states=[]
        path_taken = []
        no_targets = 5
        agents = []
        alltargets = []

        for i in range(5):
            targets = []
            for j in range(no_targets):
                targetpos = [random.randint(0,99),random.randint(0,99)]
                targets.append(targetpos)
                alltargets.append(targetpos)
            agents.append(Agent(i+1,targets,-i))

        starting_states.append(start_positions(agents,scaler))

        print("Paths found")
        flag =0
        while(agents[0].no_targets_collected < no_targets and
                agents[1].no_targets_collected < no_targets and
                agents[2].no_targets_collected < no_targets and
                agents[3].no_targets_collected < no_targets and
                agents[4].no_targets_collected < no_targets):

            for cnt,agent in enumerate(agents):
                agent.update()
                agent.check_targets(alltargets)
            if flag==0:
                flag+=1
            else:
                starting_states.append(output_frontend(agents,scaler))

        for cnt,agent in enumerate(agents):
            csv.append(csv_writer(iter_no,cnt,agent))

        filename = "scenario_1_%d.txt" %(iter_no+1)
        with open(filename,'w') as outfile:
            json.dump(starting_states,outfile,indent=2)

    data = pd.DataFrame(csv)
    data.set_index("A", inplace=True)
    data.to_csv("scenario_1.csv",header=None)

main()
