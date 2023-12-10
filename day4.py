import requests
import builtins
from aoclib import *

DAY = 4

try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text
  open(f"INPUT{DAY}",'w').write(inp)

inp1 = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''
inp = inp.strip().split('\n')

sum=0
cards = []
cardCnt = [1 for _ in range(len(inp))]
for i,l in enumerate(inp):
  cardNo,rest = l.split(':')
  winner,have = rest.split('|')
  winner = [int(i) for i in winner.split(' ') if len(i)]
  have = [int(i) for i in have.split(' ') if len(i)]
  wins = 0
  for w in winner:
    if w in have:
      wins+=1
  if wins:
    sum += 2**(wins-1)
    for ci in range(1,wins+1):
      if i+ci < len(cardCnt):
        cardCnt[i+ci] += 1*cardCnt[i]
  cards.append((cardNo, winner, have, wins,1))
print(sum)
print(builtins.sum(cardCnt))

p2wins = []
unscanned = cards.copy()
