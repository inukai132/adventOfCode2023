import pprint

import requests
from aoclib import *

DAY = 14



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)


innp = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''
inp = inp.strip().split('\n')


def slide(gd, direct):
  match direct:
    case 'west':
      for ri in range(len(gd.grid)):
        r = [ x for x in gd.grid[ri]]
        slideRocksLeft(r)
        gd.grid[ri] = r
    case 'east':
      for ri in range(len(gd.grid)):
        r = [ x for x in gd.grid[ri]][::-1]
        slideRocksLeft(r)
        r = r[::-1]
        gd.grid[ri] = r
    case 'north':
      for ci in range(len(gd.grid)):
        r = [ x[ci] for x in gd.grid]
        slideRocksLeft(r)
        for i,rw in enumerate(gd.grid):
          rw[ci] = r[i]
    case 'south':
      for ci in range(len(gd.grid)):
        r = [ x[ci] for x in gd.grid][::-1]
        slideRocksLeft(r)
        r = r[::-1]
        for i,rw in enumerate(gd.grid):
          rw[ci] = r[i]
    case _:
      exit(-1)


def slideRocksLeft(r):
  rocks = r.count('O')
  lastRock = 0
  for _ in range(rocks):
    ri = r.index('O', lastRock)
    rn = ri
    for ri_ in range(ri - 1, -1, -1):
      if ri_ == 0 and r[ri_] == '.':
        rn = 0
        break

      if r[ri_] in 'O#':
        rn = ri_ + 1
        break
    lastRock = rn + 1
    if rn != ri:
      r[rn] = 'O'
      r[ri] = '.'


gd = Grid(inp)


def cycle(gd):
  slide(gd, 'north')
  slide(gd, 'west')
  slide(gd, 'south')
  slide(gd, 'east')

CYCLES=1000000000

cache = set()
for x in range(CYCLES):
  if x%100000 == 0:
    print(f"{x}/{CYCLES}")
  cycle(gd)
  strrep = ''.join([''.join(r) for r in gd.grid])
  if strrep in cache:
    break
  else:
    cache.add(strrep)

for i in range((CYCLES%x)+2):
  cycle(gd)
total = 0
for j,r in enumerate(gd.grid):
  total += r.count('O')*(len(gd.grid)-j)
print(i)
print(total)
