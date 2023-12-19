import requests
from aoclib import *

DAY = 15

def HASH(s):
  o=0
  for c in s:
    o+= ord(c)
    o *= 17
    o %= 256
  return o

try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)

inpp='rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
print(sum(map(HASH, inp.split(','))))
boxes = [[] for _ in range(256)]
for instr in inp.split(','):
  if '=' in instr:
    fl = int(instr[-1])
    lab = instr[:-2]
    box = HASH(lab)
    if lab in [a[0] for a in boxes[box]]:
      idx = [a[0] for a in boxes[box]].index(lab)
      boxes[box][idx][1] = fl
    else:
      boxes[box].append([lab,fl])
  elif '-' in instr:
    lab = instr[:-1]
    box = HASH(lab)
    if lab in [a[0] for a in boxes[box]]:
      idx = [a[0] for a in boxes[box]].index(lab)
      boxes[box] = boxes[box][:idx]+boxes[box][idx+1:]

total = 0
for i in range(256):
  box = boxes[i]
  for j in range(len(box)):
    total += (i+1)*(j+1)*(box[j][1])
print(total)
