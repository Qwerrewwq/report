#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


def triangle_draw(self, triangle):
    self.a, self.b, self.c = triangle
    tk.draw_line(self.a, self.b, "magenta")
    tk.draw_line(self.b, self.c, "magenta")
    tk.draw_line(self.a, self.c, "magenta")
    if R2Point.area(*triangle) > 0:
        tk.draw_neighbourhood(self.a, self.b, self.c, "magenta")
        tk.draw_neighbourhood(self.b, self.c, self.a, "magenta")
        tk.draw_neighbourhood(self.c, self.a, self.b, "magenta")
    if R2Point.area(*triangle) < 0:
        tk.draw_neighbourhood(self.a, self.c, self.b, "magenta")
        tk.draw_neighbourhood(self.b, self.a, self.c, "magenta")
        tk.draw_neighbourhood(self.c, self.b, self.a, "magenta")


setattr(Void, "draw", void_draw)
setattr(Void, "triangle_draw", triangle_draw)
setattr(Point, "draw", point_draw)
setattr(Segment, "draw", segment_draw)
setattr(Polygon, "draw", polygon_draw)


tk = TkDrawer()
tk.clean()
print("Задайте вершины треугольника против часовой стрелки:")
a = R2Point()
print()
b = R2Point()
print()
c = R2Point()
print()
triangle = (a, b, c)
f = Void(triangle)
d = Void(triangle)
d.triangle_draw(triangle)


try:
    while True:
        p = R2Point()
        f = f.add(p)
        print(
            f"S = {f.area()}, P = {f.perimeter()},",
            f"Count = {f.counter_outside()}",
        )
        print()
        tk.clean()
        f.draw(tk)
        d.triangle_draw(triangle)
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
