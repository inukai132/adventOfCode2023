import requests
from aoclib import *

DAY = 5

try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inp = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

inp = inp.strip().split('\n')

seeds = []
seeds2 = []
maps = {}
curMap = None
for l in inp:
  if len(l) == 0:
    if curMap:
      maps[curMap[0][0]] = (curMap[0],curMap[1])
      curMap = None
    continue
  elif l.startswith('seeds'):
    seeds = [int(a) for a in l.split(': ')[-1].split(' ')]
    i=0
    while i < len(seeds):
      seeds2.append(range(seeds[i], seeds[i]+seeds[i+1],1))
      i += 2
  elif 'map' in l:
    mapFrom, mapTo = l.split('-to-')
    mapTo = mapTo.split(' ')[0]
    mappingTup = (mapFrom, mapTo)
    curMap = (mappingTup,[])
  else:
    ranges = [int(a) for a in l.split(' ')]
    toRange = range(ranges[0], ranges[0]+ranges[2]+1, 1)
    fromRange = range(ranges[1], ranges[1]+ranges[2]+1, 1)
    curMap[1].append((fromRange, toRange))

maps[curMap[0][0]] = (curMap[0], curMap[1])
curMap = None

lowLoc = 9999999999999999999999999999
startLoc = None
for i,s in enumerate(seeds):
  print(i)
  curAbs = 'seed'
  while curAbs != 'location':
    next = maps[curAbs]
    for f,t in next[1]:
      if s > f.start and s < f.stop:
        s = t.start + s - f.start
        curAbs = next[0][1]
        break
    else:
      curAbs = next[0][1]
  if s < lowLoc:
    lowLoc = s
    if i == 0:
      startLoc = s
print(startLoc)

flatMap = [[a,b] for a,b in maps['seed'][1]]
cur = 'soil'
while cur != 'location':
  next = maps[cur]
  nextMap = []
  for f,t in next[1]:




for i in range(startLoc):
  s = i
  curAbs = 'location'
  while curAbs != 'seed':
    next = None
    for m in maps.values():
      if m[0][1] == curAbs:
        curAbs = m[0][0]
        next = m[1]
        break
    for t,f in next:
      if s >= f.start and s <= f.stop:
        s = t.start + s - f.start
  if any( [s in x for x in seeds2] ):
    print(i-1)
    break
