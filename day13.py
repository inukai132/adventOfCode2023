import requests
from aoclib import *

DAY = 13



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)
inpp = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

inp = inp.strip().split('\n\n')

chals = []
for l in inp:
  chals.append(l.split('\n'))

def strDiff(s1, s2):
  assert(len(s1)==len(s2))
  diffs = []
  for i in range(len(s1)):
    if s1[i] != s2[i]:
      diffs.append(i)
  return diffs

def testHor(c):
  possibles = []
  goods = []
  for i in range(len(c)-1):
    if c[i] == c[i+1]:
      possibles.append(i)
  for n in possibles:
    good = True
    for i in range(n):
      ri = 2*n-i+1
      if ri >= len(c):
        continue
      if c[ri] != c[i]:
        good = False
        break
    if good:
      goods.append(n+1)
  return goods

def graphDiff(c,n):
  diffs = []
  for i in range(n):
    ri = 2*(n-1)-i+1
    if ri >= len(c):
      continue
    diff = strDiff(c[ri],c[i])
    if diff:
      diffs += [(i,diff)]
  return diffs

def test2Hor(c):
  possibles = []
  for i in range(1,len(c)):
    diffs = graphDiff(c,i)
    if diffs and all([len(d[1]) == 1 for d in diffs]):
      possibles.append(i)
  for p in possibles:
    i,diffs = graphDiff(c, p)[0]
    s1 = c[i]
    _s1 = s1[:diffs[0]]+('#' if s1[diffs[0]]=='.'else '.')+s1[diffs[0]+1:]
    c_ = c[:i]+[_s1]+c[i+1:]
    newTest = testHor(c_)
    oldTest = testHor(c)
    for n in newTest:
      if n not in oldTest:
        return n
  return False

#test2Hor(['.###...###.#.#...', '.###...###.#.#...', '##....#..#..#.##.', '##..##.#######.#.', '#.##.####...#####', '..##.####...#####', '##..##.#######.#.'])


cols = []
rows = []
for c in chals:
  h = test2Hor(c)
  if h:
    cols.append(h)
    continue
  ct = [''.join([z[i] for z in c]) for i in range(len(c[0]))]
  v = test2Hor(ct)
  if v:
    rows.append(v)
    continue
  exit(-1)
print(100*sum(cols)+sum(rows))
