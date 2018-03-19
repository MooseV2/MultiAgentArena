import random
from termcolor import colored
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from itertools import *

def draw_board():
  for y in range(h):
    for x in range(w):
      for player in players:
        if (x,y) in nopath:
          print(colored('1', 'cyan'), end='')
          break
        elif (player.has(x, y)):
          ch = 'S' if player.start == (x,y) else '•'
          print(colored(ch, player.col), end='')
          break
      else:
        print('0', end='')
    print()
  for index, player in enumerate(players):
    print(colored(f'Player {index}:\t{len(player.area)}', player.col))

w, h= 120, 30
spaces = [[0]*w]*h
nplayers = 5
colors = 'red, green, yellow, blue, magenta, cyan, white'.split(', ')
# random.seed(1)

class Player:
  def __init__(self, x, y, n, col):
    self.pos = x,y
    self.target = 0,0
    self.n = n
    self.col = col
    self.area = set()
    self.area.add((x,y))
    self.last = (self.pos[0], self.pos[1])
    self.start = (x,y)

  def has(self, x, y):
    if (x, y) in self.area:
      return True
    return False

def owned(x, y):
  for player in players:
    if (player.has(x, y)):
      return player
  else:
    return False

def okay(x, y):
  return 0 <= x < w and 0 <= y < h

def dist(start, end):
  sx, sy = start
  ex, ey = end
  return abs(ex - sx) + abs(ey - sy)

players = []
for i in range(nplayers):
  players.append(Player(random.randint(0, w), random.randint(0, h), i, colors[i]))

regions = [
  (0,0), # TL
  (w-1,0), # TR
  (0,h-1), # BL
  (w-1,h-1), # BR
  ((w-1)//2,(h-1)//2), # C
]
gdist = lambda player, region: dist(player.pos, regions[region])
_, region_map = min([(sum(map(gdist, players, combo)), combo) for combo in permutations(range(5), 5)])
for index, player in enumerate(players):
  player.target = regions[region_map[index]]
  player.area.add(player.target)


# for i, player in enumerate(players):
#   pregions = sorted([(dist(region, player.pos), region) for region in regions])
#   print(f'Player {i} {player.pos}: [{pregions}]')

# for y in range(h):
#   for x in range(w):
#     distances = []
#     for player in players:
#       distances.append((dist((x,y), (player.x, player.y)), player.nspace(), player))
#     distances = sorted(distances, key=lambda element: (element[0], element[1]))
#     distances[0][2].area.append((x,y))

def create_matrix(tplayer, end=None):
  board = []
  for y in range(h):
    row = []
    for x in range(w):
      if end==(x,y):
        row.append(0)
      else:
        for player in players:
          if (player.has(x, y)):
            if tplayer == player:
              row.append(0)
            else:
              row.append(1)
            break
        else:
          row.append(0)
    board.append(row)
  return board



all_spaces = set()
for y in range(h):
  for x in range(w):
    all_spaces.add((x,y))

def get_lowest_player(rchoice):
  # lowest = min([len(x.area) for x in players])
  # return random.choice(list(filter(lambda x: len(x.area) == lowest, players)))
  return sorted(players, key=lambda x: len(x.area))[rchoice]

total = 0
nopath = []
rchoice = 0
while all_spaces:
  player = get_lowest_player(rchoice)
  sorted_spaces = sorted(all_spaces, key=lambda x: dist(x, player.target))
  
  grid = Grid(matrix=create_matrix(player))
  start = grid.node(*player.last)
  for index, best_choice in enumerate(sorted_spaces):
    print(f'{index}/{len(sorted_spaces)}')
    end = grid.node(best_choice[0], best_choice[1])
    path, _ = AStarFinder(diagonal_movement=DiagonalMovement.never).find_path(start, end, grid)
    if path:
      break
  else:
    # nopath.append(sorted_spaces[0])
    print(f'No path found {len(nopath)}')
    best_choice = sorted_spaces[0]
    

  all_spaces.discard(best_choice)
  player.area.add(best_choice)
  player.last = best_choice


player_grids = [Grid(matrix=create_matrix(player)) for player in players]

def get_correct_player(x,y):
  for index, player in enumerate(players):
    grid = Grid(matrix=create_matrix(player, end=(x,y)))
    start = grid.node(*player.target)
    end = grid.node(x, y)
    path, ops = AStarFinder(diagonal_movement=DiagonalMovement.never).find_path(start, end, grid)
    if path:
      return player
    else:
      pass
      # print(ops)
      # print(path)
      # print(grid.grid_str(start=start, end=end, path=path))
      # print(grid.grid_str(start=start, end=None, path=path))
  else:
    print('Error! This shouldn\'t happen')
    return None

# for player in players:
#   start = grid.node(*player.target)
#   for space in player.area:
#     if space == player.pos:
#       continue
#     end = grid.node(*space)
#     path, ops = AStarFinder(diagonal_movement=DiagonalMovement.never).find_path(start, end, grid)
#     if not path:
#       # print(space)
#       # print(grid.grid_str(path=path, start=start, end=end))
#       nopath.append(space)
      


# Fix nopaths
for item in list(nopath):
  player = get_correct_player(*item)
  if player:
    player.area.add(item)
    nopath.remove(item)



draw_board()