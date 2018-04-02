from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.core.node import Node
from pathfinding.finder.breadth_first import BreadthFirstFinder



matrix = [[0,5,0,1,0,0,0],
          [5,5,0,0,3,0,0],
          [5,5,0,3,0,0,0],
          [0,0,0,1,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0]]


test = Grid(matrix=matrix)
anode = test.node(0,0)
finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
path, runs = finder.find_path(anode,5,test)


print('operations:', runs, 'path length:', len(path))

# print(test.neighbors(anode))
# print(test.grid_str())
