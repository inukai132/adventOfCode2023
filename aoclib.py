

class Cell:
  neighbors = {}
  value = None
  def __init__(self, val):
    self.value = val

  def __eq__(self, other):
    if type(other) == type(self.value):
      return other == self.value
    if type(other) == type(self):
      return other.value == self.value
    raise NotImplementedError(f"Cannot __eq__ between {type(other)} and Cell")

  def __lt__(self, other):
    if type(other) == type(self.value):
      return other > self.value
    if type(other) == type(self):
      return other.value > self.value
    raise NotImplementedError(f"Cannot __lt__ between {type(other)} and Cell")
  def __le__(self, other):
    if type(other) == type(self.value):
      return other >= self.value
    if type(other) == type(self):
      return other.value >= self.value
    raise NotImplementedError(f"Cannot __le__ between {type(other)} and Cell")

  def __gt__(self, other):
    if type(other) == type(self.value):
      return other < self.value
    if type(other) == type(self):
      return other.value < self.value
    raise NotImplementedError(f"Cannot __gt__ between {type(other)} and Cell")
  def __ge__(self, other):
    if type(other) == type(self.value):
      return other <= self.value
    if type(other) == type(self):
      return other.value <= self.value
    raise NotImplementedError(f"Cannot __ge__ between {type(other)} and Cell")
class Grid:
  grid = []
  def __init__(self, rows):
    for r in rows:
      self.grid.append([])
      for c in r:
        self.grid[-1].append(c)

  def testSurround(self, x, y, test, dx=1, dy=1):
    res = []
    for ti in range(max(y - dy, 0), min(y + dy + 1, len(self.grid))):
      for tj in range(max(x - dx, 0), min(x + dx + 1, len(self.grid[ti]))):
        res.append(test(self.grid[ti][tj]))
    return res

def makeAOCLink(d):
    return f"https://adventofcode.com/2023/day/{d}/input"

AOCHeaders={'cookie':'session=53616c7465645f5fdd43845c5356a0c1945ec6af39857de05986f0b1429dcec01d14f21459ebed0f9abfbfcff006c9e3b3282785b66d2d9fbb4969cb6b69e296'}