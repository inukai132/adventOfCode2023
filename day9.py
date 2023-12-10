import requests

DAY = 9

inp = ''
try:
  inp = open(F"INPUT{DAY}","r").read()
except Exception:
  inp = requests.get(f"https://adventofcode.com/2023/day/{DAY}/input", headers={'cookie':'session=53616c7465645f5fdd43845c5356a0c1945ec6af39857de05986f0b1429dcec01d14f21459ebed0f9abfbfcff006c9e3b3282785b66d2d9fbb4969cb6b69e296'}).text
  open(F"INPUT{DAY}", "w").write(inp)


def predict(nums):
  deltas = [nums.copy()]
  cur = nums.copy()
  while True:
    layer = []
    for i in range(len(cur)-1):
      d = cur[i+1] - cur[i]
      layer.append(d)
    if not any(layer):
      break
    deltas.append(layer)
    cur = layer
  end = 0
  for d in deltas[::-1]:
    end += d[-1]
  return end

def predict2(nums):
  deltas = [nums.copy()]
  cur = nums.copy()
  while True:
    layer = []
    for i in range(len(cur)-1):
      d = cur[i+1] - cur[i]
      layer.append(d)
    if not any(layer):
      break
    deltas.append(layer)
    cur = layer
  end = 0
  for d in deltas[::-1]:
    end = d[0]-end
  return end

inp = inp.strip().split('\n')

total = 0
total2 = 0
for l in inp:
  nums = [int(a) for a in l.split(' ')]
  total += predict(nums)
  total2 += predict2(nums)
print(total)
print(total2)
