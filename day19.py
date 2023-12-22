import requests
from aoclib import *
import json
DAY = 19



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inp = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

inpp = '''in{x<11:a,x>30:d,R}
a{m<11:b,R}
b{a<11:c,R}
c{s<11:A,R}
d{m>30:e,R}
e{a>30:f,R}
f{s>30:A,R}

{x=787,m=2655,a=1222,s=2876}'''


instructs, data = inp.strip().split('\n\n')
instructs = instructs.split('\n')
data = data.split('\n')
accept = []
reject = []
total = 0

funcs = {'A':[], 'R':[]}
for l in instructs:
  name = l[:l.index('{')]
  instrs = [a.split(':') if ':' in a else ("True", a) for a in l.split('{')[1].split('}')[0].split(',')]
  funcs[name] = instrs

import re
for d in data:
  d = {a:int(b) for a,b in re.findall(r"([xmas])=(\d*)", d)}
  instr = 'in'
  x=d['x']
  m=d['m']
  a=d['a']
  s=d['s']
  while True:
    if instr == 'A':
      accept.append(d)
      total += x+m+a+s
      break
    if instr == 'R':
      reject.append(d)
      break
    for cond,dest in funcs[instr]:
      if eval(cond):
        instr = dest
        break
#print(total)

class Node:
  def __init__(self, name):
    self.name = name
    self.children = []
    self.parents = []

  def addConnection(self, cond, child):
    self.children.append((cond, child))
    child.parents.append((cond, self))

  def __repr__(self):
    return F"Node '{self.name}' with {len(self.children)} children and {len(self.parents)} parents"

queue = []
queue.append(('in', funcs['in']))
finished = set()
cur = None
nodes = {}
while queue:
  curName, cur = queue.pop()
  finished.add(curName)
  if curName in nodes:
    curNode = nodes[curName]
  else:
    curNode = Node(curName)
    nodes[curName] = curNode
  conds = []
  for cond, dest in cur:
    if dest in nodes:
      destNode = nodes[dest]
    else:
      destNode = Node(dest)
      nodes[dest] = destNode
    curNode.addConnection(conds+[cond], destNode)
    conds.append(f"!{cond}")
    if dest not in finished:
      queue.append((dest, funcs[dest]))


#print(len(nodes))

def dfs(node, goods):
  branches = []
  for conds, child in node.children:
    for cond in conds:
      thisGood = goods.copy()
      if cond != "True":
        invert = False
        if cond[0] == '!':
          invert = True
          cond = cond[1:]
        var = cond[0]
        cond = cond[1:]
        gl = cond[0]
        cond = cond[1:]
        restr = int(cond)
        if gl == '>':
          if invert:
            restr = pow(2,restr-1)-1
          else:
            restr = (pow(2,4000-restr-1)-1)<<restr
        else:
          if invert:
            restr = (pow(2,4000-restr-1)-1)<<restr
          else:
            restr = pow(2,restr-1)-1
        thisGood[var] &= restr
      branches += dfs(child, goods)
  if node.name == 'A':
    return [goods]
  elif node.name == 'R':
    return []
  else:
    return branches


def getCond(node):
  conds = []
  cond = []
  for c,p in node.parents:
    cond = []
    c = [a for a in c if a != 'True']
    sc = getCond(p)
    if len(sc) == 1:
      sc = sc[0]
    cond = c+sc
    conds.append(cond)
  return conds


eq = getCond(nodes['A'])
print(' || '.join(['('+' && '.join(c)+')' for c in eq]))
import string
nodesSymbs = {}
nodesSymbs_ = {}
eq_=[]
import boolean
algebra = boolean.BooleanAlgebra()
TRUE, FALSE, NOT, AND, OR, symbol = algebra.definition()
b_eq=FALSE
for b in eq:
  b_=[]
  subEq = TRUE
  for n in b:
    inv=False
    if n[0] == '!':
      inv=True
      n=n[1:]
    if n not in nodesSymbs:
      x = len(nodesSymbs)
      x = string.ascii_letters[x%26]+str(x//26)
      nodesSymbs[n] = x
      nodesSymbs_[n] = algebra.symbols(x)[0]
    b_.append(('!' if inv else '')+nodesSymbs[n])
    subEq = subEq & NOT(nodesSymbs_[n]) if inv else nodesSymbs_[n]
  eq_.append(b_)
  b_eq = b_eq | subEq
  b_eq = b_eq.simplify()

alg = ' || '.join(['('+' && '.join(c)+')' for c in eq_])
print(alg)
print(b_eq.simplify())

print(nodesSymbs)
for s in b_eq.objects:
  for k,v in nodesSymbs.items():
    if v==s:
      print(F"{v}: {k}")
      break

exit()