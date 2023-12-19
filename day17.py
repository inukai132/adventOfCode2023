import heapq

import requests
from aoclib import *
from heapq import *

DAY = 17



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

class AStarNode:
  def __init__(self, val, x, y, d, n):
    self.x = x
    self.y = y
    self.val = val
    self.g = 99999999
    self.h = 99999999
    self.f = 99999999
    self.d = d
    self.n = n
    self.parent = None
    self.id = x*200*200*200+y*200*200+(ord(d) if d else 0)*200+n

  def __eq__(self, other):
    return self.id == other.id

  def __repr__(self):
    return f"A* Node at ({self.x}, {self.y}) going {self.d} with {self.n} steps, {self.g=}, {self.f=}, {self.h=}"

  def __lt__(self, other):
    return self.f < other.f

  def __hash__(self):
    return self.id


inpp = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

inpp = '''111111111111
999999999991
999999999991
999999999991
999999999991'''

inp = inp.strip().split('\n')


def printPath(path, explored):
  #f = open('map.txt','w')
  lines = ''
  for y in range(len(gd.grid)):
    line = ''
    for x in range(len(gd.grid[y])):
      if (x, y) in [(p.x, p.y) for p in path]:
        line += '*'
      elif (x, y) in [(p.x, p.y) for p in explored]:
        line += '?'
      else:
        line += gd.grid[y][x]
    lines += line+'\n'
  print(lines)

def astar(st, ed):
  visited = set()
  toVisit = []
  start = AStarNode(gd.grid[st[1]][st[0]], st[0],st[1], '', 2)
  start.g = 0
  start.f = 0
  start.h = 0
  heapq.heappush(toVisit, start)
  printCounter = 0
  while toVisit:
    printCounter+=1
    cur = heapq.heappop(toVisit)
    # if printCounter % 1000 == 0:
    #   path = []
    #   c = cur
    #   while c:
    #     path.append(c)
    #     c = c.parent
    #   printPath(path, visited)
    visited.add(cur)
    if cur.x == ed[0] and cur.y == ed[1]:
      path = []
      c = cur
      while c:
        path.append(c)
        c = c.parent
      return path[::-1]
    posDirs = 'udlr'
    if cur.d == 'u':
      posDirs = posDirs.replace('d','')
    if cur.d == 'd':
      posDirs = posDirs.replace('u','')
    if cur.d == 'r':
      posDirs = posDirs.replace('l','')
    if cur.d == 'l':
      posDirs = posDirs.replace('r','')

    children = []
    for d in posDirs:
      dx,dy = dirMap[d]
      nx,ny = cur.x+dx,cur.y+dy
      if nx < 0 or ny < 0 or nx >= len(gd.grid[0]) or ny >= len(gd.grid):
        continue
      newLen = 2
      if cur.d in dirMap and (dx,dy) == dirMap[cur.d]:
        newLen = cur.n-1
      if newLen >= 0:
        children.append(AStarNode(gd.grid[ny][nx], nx,ny,d,newLen))
    for child in children:
      if child in visited:
        continue
      if child.g > cur.g + int(child.val):
        child.g = cur.g + int(child.val)
      else:
        continue
      child.h = dist(ed[0],ed[1],child.x,child.y)
      child.f = child.g + child.h
      child.parent = cur
      if child not in toVisit:
        heapq.heappush(toVisit, child)
  exit(-1)

def astar2(st, ed):
  visited = set()
  toVisit = []
  start = AStarNode(gd.grid[st[1]][st[0]], st[0],st[1], '', 0)
  start.g = 0
  start.f = 0
  start.h = 0
  heapq.heappush(toVisit, start)
  printCounter = 0
  while toVisit:
    printCounter+=1
    cur = heapq.heappop(toVisit)
    visited.add(cur)
    if printCounter % 0x1000 == 0:
      print(cur)
      print(f"{len(toVisit)=}")
      print(f"{len(visited)=}")
    if cur.x == ed[0] and cur.y == ed[1] and cur.n >= 3:
      path = []
      c = cur
      while c:
        path.append(c)
        c = c.parent
      return path[::-1]
    posDirs = 'udlr'
    if cur.n < 3:
      posDirs = cur.d if cur.d else 'rd'
    if cur.d == 'u':
      posDirs = posDirs.replace('d','')
    if cur.d == 'd':
      posDirs = posDirs.replace('u','')
    if cur.d == 'r':
      posDirs = posDirs.replace('l','')
    if cur.d == 'l':
      posDirs = posDirs.replace('r','')

    children = []
    for d in posDirs:
      dx,dy = dirMap[d]
      nx,ny = cur.x+dx,cur.y+dy
      if nx < 0 or ny < 0 or nx >= len(gd.grid[0]) or ny >= len(gd.grid):
        continue
      newLen = 0
      if cur.d in dirMap and (dx,dy) == dirMap[cur.d]:
        newLen = cur.n+1
      if newLen < 10:
        children.append(AStarNode(gd.grid[ny][nx], nx,ny,d,newLen))
    for child in children:
      if child in visited:
        continue
      if child.g > cur.g + int(child.val):
        child.g = cur.g + int(child.val)
      else:
        continue
      child.h = dist(ed[0],ed[1],child.x,child.y)
      child.f = child.g + child.h
      child.parent = cur
      if child not in toVisit:
        heapq.heappush(toVisit, child)
  exit(-1)

def dist(x0, y0, x1, y1):
  return (x0-x1+y0-y1)*2


from cProfile import Profile
from pstats import SortKey, Stats

gd = Grid(inp)

path = astar2([0,0],[len(gd.grid[0])-1, len(gd.grid)-1])
printPath(path,[])
print(len(path))
print(path[-1].g)
