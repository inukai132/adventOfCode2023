import requests
from aoclib import *

DAY = 16



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inpp = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''

inp = inp.strip().split('\n')

def step(x, y, d, used = {}):
  cx = x
  cy = y
  cd = d
  dirMap = {
    'u':(0,-1),
    'd':(0,1),
    'l':(-1,0),
    'r':(1,0)
  }
  while 0 <= cx < len(gd.grid[0]) and 0 <= cy < len(gd.grid):
    if (cx,cy) in used:
      if cd in used[(cx,cy)]:
        break
      else:
        used[(cx,cy)] += cd
    else:
      used[(cx, cy)] = cd

    spot = gd.grid[cy][cx]
    match spot:
      case '.':
        pass
      case '-':
        if cd in 'ud':
          step(cx-1,cy,'l',used)
          step(cx+1,cy,'r',used)
          return used
      case '|':
        if cd in 'lr':
          step(cx,cy-1,'u',used)
          step(cx,cy+1,'d',used)
          return used
      case '\\':
        match cd:
          case 'u':
            cd = 'l'
          case 'd':
            cd = 'r'
          case 'r':
            cd = 'd'
          case 'l':
            cd = 'u'
          case _:
            exit(-1)
      case '/':
        match cd:
          case 'u':
            cd = 'r'
          case 'd':
            cd = 'l'
          case 'r':
            cd = 'u'
          case 'l':
            cd = 'd'
          case _:
            exit(-1)
      case _:
        exit(-1)
    cx = dirMap[cd][0]+cx
    cy = dirMap[cd][1]+cy
  return used







gd = Grid(inp)
max = -1
for r in range(len(gd.grid)):
  for c in range(len(gd.grid[r])):
    dirs = ''
    if r == 0:
      dirs += 'd'
    if c == 0:
      dirs += 'r'
    if r == len(gd.grid)-1:
      dirs += 'u'
    if c == len(gd.grid[r])-1:
      dirs += 'l'
    for d in dirs:
      used = {}
      print(f"({c},{r},{d})")
      count = len(step(c,r,d,used))
      if count > max:
        max = count
        print(max)
print(max)
exit(0)
