from deq import Deq
from r2point import R2Point


class Figure:
    """Абстрактная фигура"""

    def __init__(self, triangle):
        self.triangle = triangle

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def counter_outside(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def __init__(self, triangle):
        super().__init__(triangle)

    def add(self, p):
        return Point(p, self.triangle)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, triangle):
        super().__init__(triangle)
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.triangle)

    def counter_outside(self):
        if self.p.distance_to_triangle(*self.triangle) >= 1:
            return 1
        else:
            return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, triangle):
        self.p, self.q = p, q
        super().__init__(triangle)

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.triangle)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.triangle)
        else:
            return Segment(self.p, r, self.triangle)

    def counter_outside(self):
        counter = 0
        if self.q.distance_to_triangle(*self.triangle) >= 1:
            counter += 1
        if self.p.distance_to_triangle(*self.triangle) >= 1:
            counter += 1
        return counter


class Polygon(Figure):
    """Многоугольник"""

    def __init__(self, a, b, c, triangle):
        self.points = Deq()
        self.points.push_first(b)
        self.counter = 0
        super().__init__(triangle)

        for vertex in [a, b, c]:
            if vertex.distance_to_triangle(*self.triangle) >= 1:
                self.counter += 1

        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        super().__init__(triangle)

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(
                R2Point.area(t, self.points.last(), self.points.first())
            )

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                if p.distance_to_triangle(*self.triangle) >= 1:
                    self.counter -= 1
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                if p.distance_to_triangle(*self.triangle) >= 1:
                    self.counter -= 1
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + t.dist(
                self.points.last()
            )
            self.points.push_first(t)

            if t.distance_to_triangle(*self.triangle) >= 1:
                self.counter += 1

        return self

    def counter_outside(self):
        return self.counter


if __name__ == "__main__":  # pragma: no cover start
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
# pragma: no cover end
