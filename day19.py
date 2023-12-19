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

inpp = '''px{a<2006:qkq,m>2090:A,rfg}
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
    #conds.append(f"!{cond}")
    if dest not in finished:
      queue.append((dest, funcs[dest]))


#print(len(nodes))

def dfs(node, goods):
  branches = []
  for cond, child in node.children:
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
    branches.append(dfs(child, goods))
  if node.name == 'A':
    goodCnt = 1
    for g in goods:
      goodCnt *= goods[g].bit_count()
    return goodCnt
  elif node.name == 'R':
    return 0



goods = {
  'x':2**4000-1,
  'm':2**4000-1,
  'a':2**4000-1,
  's':2**4000-1,
}

eq = [nodes['A']]
while any([type(a) == Node for a in eq]):
  for i,n in enumerate(eq):
    if type(n) == Node:
      break
  node = eq[i]
  repl = ['(']
  for cond,p in node.parents:
    repl.append('(')
    if cond != 'True':
      repl.append(' and '.join(cond))
      repl.append(' and ')
    repl.append(p)
    repl.append(')')
    repl.append(' or ')
  if repl[-1] == ' or ':
    repl = repl[:-1]
  if len(node.parents) == 0:
    repl.append('True')
  repl.append(')')
  eq = eq[:i] + repl + eq[i+1:]
eq = eq[1:-1]
eq = ''.join(eq)
eqb = eq
while True:
  eq = eq.replace('(True)','True')
  eq = eq.replace(' and True','')
  eq = eq.replace('True and ','')
  if eqb == eq:
    break
  eqb = eq
print(eq)

MAX = 4000
def doThing(n):
  x=(n%MAX)+1
  n//=MAX
  m=(n%MAX)+1
  n//=MAX
  a=(n%MAX)+1
  n//=MAX
  s=(n%MAX)+1
  if eval(eq):
    return 1
  return 0


if __name__ == '__main__':
  from multiprocessing import Pool
  p = Pool()
  print(sum(p.imap_unordered(doThing, range(MAX**4), chunksize=MAX)))


#
# parentSum = dfs(nodes['A'], ['True'], goods)
# print(parentSum)
