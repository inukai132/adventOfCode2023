import requests

DAY = 2

inp = requests.get(f"https://adventofcode.com/2023/day/{DAY}/input", headers={'cookie':'session=53616c7465645f5fdd43845c5356a0c1945ec6af39857de05986f0b1429dcec01d14f21459ebed0f9abfbfcff006c9e3b3282785b66d2d9fbb4969cb6b69e296'}).text.split('\n')

for l in inp:
  print(l)
