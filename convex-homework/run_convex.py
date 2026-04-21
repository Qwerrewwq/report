#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Figure, Void

print("Задайте вершины треугольника против часовой стрелки:")
a = R2Point()
print()
b = R2Point()
print()
c = R2Point()
print()
triangle = (a, b, c)
f = Void(triangle)

try:
    while True:
        p = R2Point()
        f = f.add(p)
        print(
            f"S = {f.area()}, P = {f.perimeter()},",
            f"Count = {f.counter_outside()}",
        )
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
