import requests
from aoclib import *

DAY = 12



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inp='''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

inp = inp.strip().split('\n')

def invalidTest(s,p):
  if s.count('?') > 1:
    return True
  poss = set()
  if '?' in s:
    for c in ['.','#']:
      st = s[:s.index('?')]+c+s[s.index('?')+1:]
      poss.add(st)
  else:
    poss.add(s)
  for s in poss:
    si = s.find('#')
    pi = 0
    pt = None
    good = True
    while si < len(s):
      if s[si] == '#':
        if pt is None:
          if pi >= len(p):
            good = False
            break
          pt = p[pi]
          pi+=1
        pt -= 1
      if pt and pt < 0:
        good = False
        break
      if s[si] == '.':
        if pt:
          good = False
          break
        pt = None
      si += 1
    if good and pi == len(p):
      return True



def quickTest(s,p):
  totalSpaces = s.count('?')+s.count('#')
  if totalSpaces < sum(p):
    return False
  return invalidTest(s,p)

def solveRecurse(s,p):
  if '?' not in s:
    if quickTest(s,p):
      arrangements.append(s)
      return True
    else:
      return False
  i = s.index('?')
  for t in ['.','#']:
    s_ = s[:i]+t+s[i+1:]
    if quickTest(s_,p):
      solveRecurse(s_,p)
  return False

def solveRecurse2(args, arrangements=[]):
  s,p=args
  if '?' not in s:
    if quickTest(s,p):
      arrangements.append(s)
      return arrangements
    else:
      return arrangements
  i = s.index('?')
  for t in ['.','#']:
    s_ = s[:i]+t+s[i+1:]
    if quickTest(s_,p):
      solveRecurse2((s_,p),arrangements)
  return arrangements


arrangements = []
arrangements2 = []
pats2 = []
pats = []
for l in inp:
  springs, pattern = l.split(' ')
  pattern = [int(a) for a in pattern.split(',')]
  #solveRecurse(springs,pattern)
  pats.append((springs,pattern))
  pats2.append((springs*5,pattern*5))

if __name__ == "__main__":
  from multiprocessing import Pool
  p = Pool()
  arrs = list(p.imap_unordered(solveRecurse2, pats2, chunksize=100))
  print(arrs)
  print(sum([len(a) for a in arrs]))
