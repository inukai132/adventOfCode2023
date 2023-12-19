import requests
from aoclib import *

DAY = 11



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)
inpp='''
#.#
..#
'''
inp = inp.strip().split('\n')

gd = Grid(inp)

SCALEFACTOR=999999
rowsToAdd = []
print('\n'.join([''.join(a) for a in gd.grid]))
for l in range(len(gd.grid)):
  if all(c=='.' for c in gd.grid[l]):
    rowsToAdd.append(l)

'''
rowsToAdd.sort(reverse=True)
for r in rowsToAdd:
  gd.grid.insert(r, gd.grid[r].copy())'''

colsToAdd = []
for l in range(len(gd.grid[0])-1, -1, -1):
  if all(gd.grid[r][l]=='.' for r in range(len(gd.grid))):
    colsToAdd.append(l)

print('\n'.join([''.join(a) for a in gd.grid]))

galaxies = []
for y in range(len(gd.grid)):
  for x in range(len(gd.grid[y])):
    if gd.grid[y][x] == '#':
      galaxies.append([len(galaxies),y+sum([SCALEFACTOR for r in rowsToAdd if r < y]),x+sum([SCALEFACTOR for c in colsToAdd if c < x])])

def dist(s,e):
  return abs(s[1]-e[1])+abs(s[2]-e[2])

import itertools
shortests = [[s, e ,999999999999999999999999999999] for s, e in itertools.combinations(range(len(galaxies)), 2)]
for s in shortests:
  s[2] = dist(galaxies[s[0]],galaxies[s[1]])

print(sum([m[2] for m in shortests]))
