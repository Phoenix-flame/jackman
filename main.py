from source.map import *

map = Map("testcases/test1")

a = (map.getAdjacents(map.getCell(1, 1)))

for i in a:
    print(i)
