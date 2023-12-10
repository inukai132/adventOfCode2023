import requests

DAY = 2

inp = requests.get(f"https://adventofcode.com/2023/day/{DAY}/input", headers={'cookie':'session=53616c7465645f5fdd43845c5356a0c1945ec6af39857de05986f0b1429dcec01d14f21459ebed0f9abfbfcff006c9e3b3282785b66d2d9fbb4969cb6b69e296'}).text.split('\n')

sum = 0
powerSum = 0
for l in inp:
  if not len(l):
    continue
  game, games = l.split(': ')
  gameNo = int(game.split(' ')[-1])
  games = games.strip().split('; ')
  colors = {'red':-1, 'blue':-1,'green':-1}
  for round in games:
    cs = round.strip().split(', ')
    for x in cs:
      v,c = x.split(' ')
      colors[c] = max(colors[c],int(v))
  powerSum += colors['blue']*colors['red']*colors['green']
  if colors['blue'] > 14 or colors['red'] > 12 or colors['green'] > 13:
    continue
  sum += gameNo
print(sum)
print(powerSum)