import requests
import string

DAY = 3
try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(f"https://adventofcode.com/2023/day/{DAY}/input", headers={'cookie':'session=53616c7465645f5fdd43845c5356a0c1945ec6af39857de05986f0b1429dcec01d14f21459ebed0f9abfbfcff006c9e3b3282785b66d2d9fbb4969cb6b69e296'}).text
  open(f"INPUT{DAY}",'w').write(inp)
inp = inp.strip().split('\n')
def checkSurround(i,j,map):
  for ti in range(max(i-1,0),min(i+2,len(map[i]))):
    for tj in range(max(j-1,0),min(j+2,len(map))):
      if map[ti][tj] in string.punctuation.replace('.',''):
        return True
  return False

def gearCheck(i,j,map):
  nears=set()
  for ti in range(max(i-1,0),min(i+2,len(map[i]))):
    for tj in range(max(j-1,0),min(j+2,len(map))):
      if map[ti][tj] in string.digits:
        nj = tj
        while nj in range(len(map[ti])) and map[ti][nj] in string.digits:
          nj -= 1
        nj += 1
        num = int(map[ti][nj])
        nj+=1
        while nj in range(len(map[ti])) and map[ti][nj] in string.digits:
          num *=10
          num +=int(map[ti][nj])
          nj += 1
        nears.add(num)
  nears = list(nears)
  if len(nears) == 2:
    return nears[0]*nears[1]
  else:
    return 0

sum=0
gearsSum=0
print('\n'.join(inp))
for i in range(len(inp)):
  line = inp[i]
  j=0
  while j < len(line):
    good = False
    if line[j] == '*':
      gearsSum += gearCheck(i,j,inp)
    if line[j] not in string.digits:
      j+=1
      continue
    num = int(line[j])
    if checkSurround(i,j,inp):
      good = True
    j+=1
    while j < len(line) and line[j] in string.digits:
      num *= 10
      num += int(line[j])
      if not good and checkSurround(i,j,inp):
        good = True
      j+=1
    if good:
      sum += num
print(sum)
print(gearsSum)




