import requests
from aoclib import *

DAY = 18

try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inpp = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

inp = inp.strip().split('\n')

class Line:
  def __init__(self, x, y, l, d):
    self.x0 = x
    self.y0 = y
    self.d = d
    match d:
      case 'r':
        self.x1 = x+l
        self.y1 = y
      case 'l':
        self.x0 = x-l
        self.x1 = x
        self.y1 = y
      case 'd':
        self.y1 = y+l
        self.x1 = x
      case 'u':
        self.y0 = y-l
        self.y1 = y
        self.x1 = x
  def pointIn(self, tx, ty):
    return self.x0 <= tx <= self.x1 and self.y0 <= ty <= self.y1

  def rowIn(self, ty):
    return self.y0 <= ty <= self.y1

  def colIn(self, tx):
    return self.x0 <= tx <= self.x1

  def __len__(self):
    return self.x1-self.x0+self.y1-self.y0

  def __repr__(self):
    return f"Line from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1}), len {len(self)}"

  def translate(self, dx, dy):
    self.x0 -= dx
    self.x1 -= dx
    self.y0 -= dy
    self.y1 -= dy

def islandCount(i):
  return (i^(i<<1)).bit_count()//2

from cProfile import Profile
from pstats import SortKey, Stats


lines = []
x,y  = 0,0
minW = 9999999999999
maxW = -9999999999999
minH = 9999999999999
maxH = -9999999999999
pt2 = 1
for l in inp:
  d,ln,c = l.split(' ')
  d = d.lower()
  ln=int(ln)
  c=c.strip('()#')
  if pt2:
    d = 'rdlu'[int(c[-1])]
    ln = int(c[:-1],16)
  lines.append(Line(x,y,ln,d))
  match d:
    case 'l':
      x -= ln
    case 'r':
      x += ln
    case 'u':
      y -= ln
    case 'd':
      y += ln
  if x < minW:
    minW = x
  if y < minH:
    minH = y
  if x > maxW:
    maxW = x
  if y > maxH:
    maxH = y
assert len(lines) == len(inp)
assert (x,y) == (0,0)
print(len(lines))
for l in lines:
  l.translate(minW,minH)
maxW -= minW
minW -= minW
maxH -= minH
minH -= minH

intLines = []
for y in range(maxH):
  if y%0x10000 == 0:
    print(f"{y} / {maxH}")
  subsetH = [l for l in lines if l.d in 'lr' and l.y0 == y]
  inside = False
  roundMask = 0
  for s in subsetH:
    m = (2**len(s)-1) << s.x0
    roundMask ^= m
  intLines.append(roundMask)

print(len([a for a in intLines if a]))
mask = 0
y = 0
count = 0
islands = 0
lastMaskBitCnt = 0
for y,roundMask in enumerate(intLines):
  if roundMask:
    offs = roundMask & mask
    mask ^= roundMask
    islands = islandCount(mask)
    lastMaskBitCnt = mask.bit_count() + islands
    count += lastMaskBitCnt + offs.bit_count()
  else:
    count += lastMaskBitCnt
  if y%0x10000 == 0:
    print(f"{y} / {maxH}")
print(count+mask.bit_count()+1)
