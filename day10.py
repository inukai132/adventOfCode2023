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

inpp='''..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........'''

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

def pathfind(start):
  visited = set()
  queue = set()
  visited.add(start)
  queue.add(start)
  while queue:
    m = queue.pop()
    for dy in (1,0,-1):
      for dx in (1,0,-1):
        if dy != 0 and dx != 0:
          continue
        if m[0]+dy < 0 or m[0]+dy >= len(bigMap):
          continue
        if m[1]+dx < 0 or m[1]+dx >= len(bigMap[0]):
          continue
        neighbor = (m[0]+dy,m[1]+dx)
        if bigMap[neighbor[0]][neighbor[1]] == 'O':
          return True
        if bigMap[neighbor[0]][neighbor[1]] == 'I':
          return False
        if bigMap[neighbor[0]][neighbor[1]] == '.':
          if neighbor not in visited:
            queue.add(neighbor)
          visited.add(neighbor)
          if neighbor in outsides:
            return True
  return False

cleanMap = [['.']*len(gd.grid[0]) for _ in range(len(gd.grid))]
for n in path:
  cleanMap[n[0]][n[1]] = gd.grid[n[0]][n[1]]

bigMap = [['.']*len(gd.grid[0])*2 for _ in range(len(gd.grid)*2)]
for n in path:
  bigMap[n[0]*2][n[1]*2] = gd.grid[n[0]][n[1]]
  if gd.grid[n[0]][n[1]] in 'FL-':
    bigMap[n[0] * 2][n[1] * 2 + 1] = '-'
  if gd.grid[n[0]][n[1]] in '7J-' and n[1] * 2 - 1 >= 0:
    bigMap[n[0] * 2][n[1] * 2 - 1] = '-'
  if gd.grid[n[0]][n[1]] in 'F7|':
    bigMap[n[0] * 2 + 1][n[1] * 2] = '|'
  if gd.grid[n[0]][n[1]] in 'LJ|' and n[0] * 2 - 1 >= 0:
    bigMap[n[0] * 2 - 1][n[1] * 2] = '|'

print('\n'.join([''.join(a) for a in bigMap]))

ins = 0
outsides = [(0,0)]
for y in range(len(bigMap)):
  for x in range(len(bigMap[y])):
    if bigMap[y][x] is not '.':
      continue
    elif pathfind((y,x)):
      bigMap[y][x] = 'O'
      outsides.append((y,x))
    else:
      ins += 1
      bigMap[y][x] = 'I'
  print('\n'.join([''.join(a) for a in bigMap]))
  print()

print('\n'.join([''.join(a) for a in bigMap]))
print(ins)

smolMap = [['.']*len(gd.grid[0]) for _ in range(len(gd.grid))]

for y in range(0, len(bigMap), 2):
  for x in range(0, len(bigMap), 2):
    square = bigMap[y][x:x+2]+bigMap[y+1][x:x+2]
    smolMap[y//2][x//2] = square[0]

print('\n'.join([''.join(a) for a in smolMap]))
print(('\n'.join([''.join(a) for a in smolMap])).count('I'))
