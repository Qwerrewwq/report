from math import sqrt


class R2Point:
    """Точка (Point) на плоскости (R2)"""

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежит ли точка внутри заданного треугольника?
    def inside_of_triangle(self, a, b, c):
        s1 = R2Point.area(a, b, self)
        s2 = R2Point.area(b, c, self)
        s3 = R2Point.area(c, a, self)

        return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (
            s1 <= 0 and s2 <= 0 and s3 <= 0
        )

    # Расстояние до отрезка
    def distance_to_segment(self, a, b):
        vec_ab = R2Point(b.x - a.x, b.y - a.y)
        vec_ap = R2Point(self.x - a.x, self.y - a.y)
        t = (vec_ab.x * vec_ap.x + vec_ab.y * vec_ap.y) / (
            vec_ab.x**2 + vec_ab.y**2
        )
        if t < 0:
            return self.dist(a)
        elif t > 1:
            return self.dist(b)
        else:
            return abs(R2Point.area(a, b, self)) * 2 / a.dist(b)

    # Расстояние до треугольника
    def distance_to_triangle(self, a, b, c):
        if self.inside_of_triangle(a, b, c):
            return 0.0
        else:
            return min(
                self.distance_to_segment(a, b),
                self.distance_to_segment(b, c),
                self.distance_to_segment(a, c),
            )

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (
            (a.x <= self.x and self.x <= b.x)
            or (a.x >= self.x and self.x >= b.x)
        ) and (
            (a.y <= self.y and self.y <= b.y)
            or (a.y >= self.y and self.y >= b.y)
        )

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


if __name__ == "__main__":  # pragma: no cover start
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
    # pragma: no cover end
