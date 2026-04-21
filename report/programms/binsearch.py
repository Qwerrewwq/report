x, b = 4, [-5, -2, 3, 4, 4, 5]
i, j = 0, len(b) - 1
while i + 1 != j:
    k = (i + j) // 2
    if b[k] <= x:
        i = k
    else:
        j = k
print(i)
