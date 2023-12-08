import requests
from aoclib import *

DAY = 7

CARDS = "AKQJT98765432"
CARDS2 = "AKQT98765432J"

def testHands(hand):
  if 'J' not in hand:
    return sortFn2(hand)

  best = ['A',-1]
  for c in CARDS2[:-1]:
    cur = sortFn2(hand, c)
    if cur > best[1]:
      best = [c, cur]
  return sortFn2(hand, best[0])

def getHandType(hand):
  cards = {a:hand.count(a) for a in hand}
  if len(cards) == 1:
    return 7
  elif len(cards) == 2:
    if list(cards.values())[0] in [1,4]:
      return 6
    else:
      return 5
  elif len(cards) == 3:
    if any([a == 3 for a in cards.values()]):
      return 4
    else:
      return 3
  elif len(cards) == 4:
    return 2
  else:
    return 1

def sortFn(a):
  typeA = getHandType(a)
  return typeA*10000000000+ \
    (13-CARDS.index(a[0]))*100000000+ \
    (13-CARDS.index(a[1]))*1000000+ \
    (13-CARDS.index(a[2]))*10000+ \
    (13-CARDS.index(a[3]))*100+ \
    (13-CARDS.index(a[4]))

def sortFn2(a, repl='J'):
  typeA = getHandType(a.replace('J',repl))
  return typeA*10000000000+ \
    (13-CARDS2.index(a[0]))*100000000+ \
    (13-CARDS2.index(a[1]))*1000000+ \
    (13-CARDS2.index(a[2]))*10000+ \
    (13-CARDS2.index(a[3]))*100+ \
    (13-CARDS2.index(a[4]))


try:
  inp = open(f"INPUT{DAY}",'r').read()
except Exception:
  inp = requests.get(makeAOCLink(DAY), headers=AOCHeaders)
  assert inp.status_code == 200
  inp = inp.text.strip()
  open(f"INPUT{DAY}",'w').write(inp)
inp='''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
inp = inp.strip().split('\n')

hands = []
for l in inp:
  hand, bid = l.split(' ')
  bid = int(bid)
  hands.append((hand,bid))

hands.sort(key=lambda x:sortFn(x[0]), reverse=True)
total = 0
for i,h in enumerate(hands):
  total += (len(hands)-i)*h[1]
print(total)

hands.sort(key=lambda x:testHands(x[0]), reverse=True)
total = 0
for i,h in enumerate(hands):
  total += (len(hands)-i)*h[1]
print(total)
