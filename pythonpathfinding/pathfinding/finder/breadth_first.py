from .finder import Finder, TIME_LIMIT, MAX_RUNS
from pythonpathfinding.pathfinding.core.util import unique_val
from pythonpathfinding.pathfinding.core.diagonal_movement import DiagonalMovement
import math
import sys
sys.setrecursionlimit(100000)

class BreadthFirstFinder(Finder):
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        super(BreadthFirstFinder, self).__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs)
        if not diagonal_movement:
            self.diagonalMovement = DiagonalMovement.never

    def ids(self, start, bottype, grid, open_list):
        node = open_list.pop(0)
        node.closed = True


        for depth in range(0,100000):
            history = []
            history.append(start)
            path = self.dfs(start,depth,bottype,history,grid)
            # this would return the solution of what the actaul path is.
            #I am only using this as a termination condtions since if all 5 targets are collected no point in building path out further
            if self.targets_collected[bottype]==6 or len(unique_val(history)) == grid.height*grid.width:
                history = unique_val(history)
                print("Agent Done")
                return history

            self.targets_collected[bottype] = 0

            for node in history:
                node.opened = False



    def dfs(self,node,depth,bottype,history,grid):

        if depth == 0 and node.goal == bottype :
            # self.targets_collected[bottype]+=1
            history.append(node)
            return history

        elif depth == 0:
            history.append(node)
            return history

        else:
            neighbors = self.find_neighbors(grid,node)
            for neighbor in neighbors:
                if neighbor.closed or neighbor.opened:
                    continue
                if neighbor.goal == bottype :
                    self.targets_collected[bottype]+=1
                    if self.targets_collected[bottype] == 4:
                        if history[0].goal == bottype:
                            self.targets_collected[bottype]+=1
                # print("neighbor : ",neighbor.goal)
                history.append(neighbor)
                # print("history: ", history)
                neighbor.opened = True
                neighbor.parent = node
                path = self.dfs(neighbor,depth-1,bottype,history,grid)
                if path != None and self.targets_collected[bottype]==5:
                    return history

        # print(history)
        return None
