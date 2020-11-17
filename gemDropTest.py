def gemDrop(m, cells):
    n = m
    for k in range(cells):
        for i in range(cells):
            for j in range(cells):
                if n[j][i] == -1:
                    if j == 0:
                        n[j][i] = -1
                    else:
                        n[j][i] = n[j-1][i]
                        n[j-1][i] = -1
    return n

m1 =     [['O', 'O', 'Y', 'Y', 'R', 'P', 'Y', 'B'],
          ['G', 'P', 'R', 'R', 'W', 'W', 'R', 'O'],
          ['W', 'P', 'O', 'Y', 'G', 'O', 'Y', 'G'],
          ['B', 'O', 'R', 'O', 'W', 'W', 'G', 'O'],
          ['G', 'B', 'R', 'W', 'R', 'W', 'P', 'B'],
          ['Y', 'P', 'B', 'B', 'O', 'O', 'R', 'G'],
          ['B', 'R', 'P', 'P', 'R', 'G', 'B', 'P'],
          ['O',  -1,  -1,  -1, 'Y', 'R', 'G', 'R']]

m2 =     [['O', 'O', 'Y', 'Y', 'R', 'P', 'Y', 'B'],
          ['G', 'P', 'R', 'R', 'W', 'W', 'R', 'O'],
          ['W', 'P', 'O', 'Y', 'G', 'O', 'Y', 'G'],
          ['B', 'O', 'R', 'O', 'W', 'W', 'G', 'O'],
          ['G', 'B', 'R', 'W', 'R', 'W', 'P', 'B'],
          ['Y', 'P', -1, 'B', 'O', 'O', 'R', 'G'],
          ['B', 'R', -1, 'P', 'R', 'G', 'B', 'P'],
          ['O', 'Y', -1, 'G', 'Y', 'R', 'G', 'R']]

m3 =     [['O', 'O', 'Y', 'Y', 'R', 'P', 'Y', 'B'],
          ['G', 'P', 'R', 'R', 'W', 'W', 'R', 'O'],
          ['W', 'P', 'O',  -1,  -1,  -1, 'Y', 'G'],
          ['B', 'O', 'R', 'O', 'W',  -1, 'G', 'O'],
          ['G', 'B', 'R', 'W', 'R',  -1, 'P', 'B'],
          ['Y', 'P', 'B', 'B', 'O', 'O', 'R', 'G'],
          ['B', 'R', 'P', 'P', 'R', 'G', 'B', 'P'],
          ['O', 'Y', 'B', 'G', 'Y', 'R', 'G', 'R']]

gemDrop(m1, 8)
for row in m1:
    print(row)
print()
gemDrop(m2, 8)
for row in m2:
    print(row)
print()
gemDrop(m3, 8)
for row in m3:
    print(row)
print()
