t = int(input("t -> "))
y = 0
try:
    while True:
        y = t * y + int(input("x -> "))
except(EOFError):
    print(f"\n      P({t}) = {y}")
