import requests
from aoclib import *

DAY = 8



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inpp='''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
inp = inp.strip().split('\n')

instr = inp[0]
nodes = []
nodeIdxs = []
for l in inp[2:]:
  node, nexts = l.split(' = ')
  left,right = nexts.strip('()').split(', ')
  for n in [node, left, right]:
    if n not in nodeIdxs:
      nodeIdxs.append(n)
  nodes.append((nodeIdxs.index(node), nodeIdxs.index(left), nodeIdxs.index(right)))

st = nodeIdxs.index('AAA')
ed = nodeIdxs.index('ZZZ')

cur = st
steps = 0
i = 0
while cur != ed:
  steps += 1
  cur = nodes[cur]['LR'.index(instr[i])+1]
  i=(i+1)%len(instr)
print(steps)