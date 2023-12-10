import requests
from aoclib import *

DAY = 6



try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)
inp = inp.strip().split('\n')

times = [int(a) for a in inp[0].split(':')[-1].strip().split(' ') if len(a)]
dsts = [int(a) for a in inp[1].split(':')[-1].strip().split(' ') if len(a)]

times2 = int(''.join([a for a in inp[0].split(':')[-1].strip().split(' ') if len(a)]))
dsts2 = int(''.join([a for a in inp[1].split(':')[-1].strip().split(' ') if len(a)]))

wins = 1
for i in range(len(times)):
  ct = times[i]
  cd = dsts[i]
  wtw = 0
  for i in range(ct):
    dst = (ct-i)*i
    if dst > cd:
      wtw += 1
  wins *= wtw

print(wins)
wtw=0

for i in range(times2):
  dst = (times2 - i) * i
  if dst > dsts2:
    wtw += 1
print(wtw)