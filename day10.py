import requests
from aoclib import *

DAY = 10

try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)
inp = inp.strip().split('\n')


gd = Grid(inp)
start = None
for r in range(len(gd.grid)):
  if start:
    break
  for c in range(len(gd.grid[r])):
    if gd.grid[r][c] == 'S':
      start = [r,c]
      break

cur = start.copy()
nexts = []
path = []
if start[0]+1 < len(gd.grid) and gd.grid[start[0]+1][start[1]+0] in '|LJ':
  nexts.append([start[0]+1,start[1]])
if start[1]+1 < len(gd.grid[0]) and gd.grid[start[0]+0][start[1]+1] in '-7J':
  nexts.append([start[0],start[1]+1])
if start[0]-1 < 0 and gd.grid[start[0]+1][start[1]+0] in '|7F':
  nexts.append([start[0]-1,start[1]])
if start[1]-1 < 0 and gd.grid[start[0]+0][start[1]+1] in '-FL':
  nexts.append([start[0],start[1]-1])

cur = nexts[0]
path.append(start.copy())
while cur != start:
  curVal = gd.grid[cur[0]][cur[1]]
  delta = [cur[0]-path[-1][0],cur[1]-path[-1][1]]
  next = None
  match curVal:
    case '|':
      next = [cur[0]+delta[0],cur[1]+delta[1]]
    case '-':
      next = [cur[0]+delta[0],cur[1]+delta[1]]
    case 'L':
      if delta[0]:
        next = [cur[0],cur[1]+1]
      else:
        next = [cur[0]-1,cur[1]]
    case 'F':
      if delta[0]:
        next = [cur[0],cur[1]+1]
      else:
        next = [cur[0]+1,cur[1]]
    case '7':
      if delta[0]:
        next = [cur[0],cur[1]-1]
      else:
        next = [cur[0]+1,cur[1]]
    case 'J':
      if delta[0]:
        next = [cur[0],cur[1]-1]
      else:
        next = [cur[0]-1,cur[1]]
  path.append(cur.copy())
  cur = next.copy()
print(len(path))
print(len(path)//2)
cleanMap = [['.']*len(gd.grid[0]) for _ in range(len(gd.grid))]
for n in path:
  cleanMap[n[0]][n[1]] = gd.grid[n[0]][n[1]]

def pathfind(dest, start):




print('\n'.join([''.join(a) for a in cleanMap]))

