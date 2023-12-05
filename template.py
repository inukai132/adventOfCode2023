import requests

DAY = 2

inp = requests.get(f"https://adventofcode.com/2023/day/{DAY}/input", headers={'cookie':'session='}).text.split('\n')

for l in inp:
  print(l)
