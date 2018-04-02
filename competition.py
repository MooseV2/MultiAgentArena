import numpy as np
from math import hypot, inf
np.set_printoptions(threshold=np.inf)
from pythonpathfinding.pathfinding.core.grid import Grid
from pythonpathfinding.pathfinding.finder.breadth_first import BreadthFirstFinder
from pythonpathfinding.pathfinding.core.node import Node
from pythonpathfinding.pathfinding.core.diagonal_movement import DiagonalMovement
import json
import pandas as pd
import multiprocessing as mp
import cProfile

def start_positions(agents):

    starting_states = []

    for agent in agents:

        state = {"Agent":[{"X":int(agent.x), "Y":int(agent.y),
                "Targets":[{"X":int(agent.targets[0][0]),"Y":int(agent.targets[0][1])},
                {"X":int(agent.targets[1][0]),"Y":int(agent.targets[1][1])},
                {"X":int(agent.targets[2][0]),"Y":int(agent.targets[2][1])},
                {"X":int(agent.targets[3][0]),"Y":int(agent.targets[3][1])},
                {"X":int(agent.targets[4][0]),"Y":int(agent.targets[4][1])},]}]}
        starting_states.append(state)
    return starting_states


def output_frontend(agents):

    agent_path = []

    for cnt,agent in enumerate(agents):

        state = {"agent_no":cnt+1,
                "X":int(agent.x),
                "Y":int(agent.y)}
        agent_path.append(state)
    return agent_path


def csv_writer(iteration,agent_no,agent):

    max_happ = max(agent.happiness_array)
    min_happ = min(agent.happiness_array)

    try:
        competitive =((agent.happiness-min_happ)/(max_happ-min_happ))
    except:
        competitive = 1


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
    def __init__(self, position, target_type,targets):
        self.x, self.y = position
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
        matrix = np.zeros((10,10))
        for target in self.targets:
            matrix[target[0],target[1]] = self.target_type

        my_grid = Grid(matrix=matrix)
        agent = my_grid.node(self.x,self.y)
        finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(agent,self.target_type,my_grid)

        self.path = path

    def prune_path(self,empty):
        self.path = [point for point in self.path if point not in empty]


    def check_correctness(self):
        cnt = 0
        for step in self.path:
            for tar in self.targets:
                if step.x ==tar[0] and step.y == tar[1]:
                    cnt +=1
        if cnt == 5:
            print("All good")
        else:
            print("Problem with pathfinding path only contained ", cnt)

    # def check_distance(self):



    def next_moves(self):
        try:
            movesX = self.path[0].x - self.x
            movesY = self.path[0].y - self.y
            self.goal= self.path.pop(0)
            return [movesX,movesY]
        except:
            return[0,0]

    def check_empty(self, alltargets):
        # print("Current Postion: ",self.x,self.y)
        for cnt,target in enumerate(self.targets):
            # print("target Postion: ",target[0],target[1])
            if self.x == target[0] and self.y == target[1]:
                del self.targets[cnt]
                self.no_targets_collected +=1
                return False
            else:
                pass
        for target in alltargets:
            if self.x == target[0] and self.y == target[1]:
                return False
            else:
                pass
        return True



    def update(self,empty):

        self.steps_taken +=1
        self.prune_path(empty)

        self.happiness = (self.no_targets_collected/(self.steps_taken))

        self.happiness_array.append(self.happiness)


        if (self.moves[0] == 0 and self.moves[1]==0) :
            self.moves = self.next_moves()
            # print (moves)

        if self.moves[0] !=0:
            next_move = 1*np.sign(self.moves[0])
            self.moves[0] = self.moves[0] - next_move
            self.x += next_move
        elif self.moves[1] !=0:
            next_move = 1*np.sign(self.moves[1])
            self.moves[1] = self.moves[1] - next_move
            self.y += next_move
        else:
            # print("No more moves")
            pass


def main():

    iterations = 10
    csv = []
    for iter_no in range(iterations):

        path_taken = []

        no_targets = 5
        agents = []
        empty = set()
        alltargets = []



        all_targetss= []
        for i in range(5):
            targets = []
            for j in range(5):
                targetpos = np.random.randint(10,size=2)
                targets.append(targetpos)
                alltargets.append(targetpos)
            agentpos = np.random.randint(10,size=2)
            agents.append(Agent(agentpos,i+1,targets))
        filename = "CSV_files/start_pos%d.txt" %(iter_no+1)
        with open(filename,'w') as outfile:
            json.dump(start_positions(agents),outfile)

        print("Paths found")
        while(agents[0].no_targets_collected < no_targets and
                agents[1].no_targets_collected < no_targets and
                agents[2].no_targets_collected < no_targets and
                agents[3].no_targets_collected < no_targets and
                agents[4].no_targets_collected < no_targets):

            for cnt,agent in enumerate(agents):
                # agent.check_correctness()
                agent.update(empty)
                if agent.check_empty(alltargets):
                    empty.add((agent.x,agent.y))


            path_taken.append(output_frontend(agents))
        for cnt,agent in enumerate(agents):

            csv.append(csv_writer(iter_no+1,cnt+1,agent))

        filename = "CSV_files/path_taken%d.txt" %(iter_no+1)
        with open(filename,'w') as outfile:
            json.dump(path_taken,outfile)



    # print(json.dumps(csv, indent=2))
    data = pd.DataFrame(csv)
    data.to_csv("CSV_files/csv_1.csv")



main()
