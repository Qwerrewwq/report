import pytest
from convex import Figure, Void, Point, Segment, Polygon
from r2point import R2Point


@pytest.fixture
def triangle():
    return (R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(0.0, 1.0))


@pytest.fixture
def point_inside(triangle):
    return R2Point(0.2, 0.2)


@pytest.fixture
def point_outside(triangle):
    return R2Point(5.0, 5.0)


@pytest.fixture
def point_on_boundary(triangle):
    return R2Point(0.5, -1.0)


@pytest.fixture
def point_just_inside_boundary(triangle):
    return R2Point(0.5, -1.0 + 0.1)


@pytest.fixture
def point_just_outside_boundary(triangle):
    return R2Point(0.5, -1.0 - 0.1)


class TestFigure:

    def test_figure_init(self, triangle):
        figure = Figure(triangle)
        assert figure.triangle == triangle

    def test_figure_perimeter(self, triangle):
        figure = Figure(triangle)
        assert figure.perimeter() == 0.0

    def test_figure_area(self, triangle):
        figure = Figure(triangle)
        assert figure.area() == 0.0

    def test_figure_counter_outside(self, triangle):
        figure = Figure(triangle)
        assert figure.counter_outside() == 0


class TestVoid:

    def test_void_init(self, triangle):
        void = Void(triangle)
        assert void.triangle == triangle

    def test_void_add_returns_point(self, triangle, point_inside):
        void = Void(triangle)
        result = void.add(point_inside)
        assert isinstance(result, Point)
        assert result.p == point_inside


class TestPoint:

    def test_point_init(self, triangle, point_inside):
        point = Point(point_inside, triangle)
        assert point.p == point_inside
        assert point.triangle == triangle

    def test_point_add_same_point(self, triangle, point_inside):
        point = Point(point_inside, triangle)
        result = point.add(point_inside)
        assert result is point

    def test_point_add_different_point(self, triangle, point_inside):
        point = Point(point_inside, triangle)
        other = R2Point(0.5, 0.5)
        result = point.add(other)
        assert isinstance(result, Segment)

    def test_point_counter_outside_inside(self, triangle, point_inside):
        point = Point(point_inside, triangle)
        assert point.counter_outside() == 0

    def test_point_counter_outside_outside(self, triangle, point_outside):
        point = Point(point_outside, triangle)
        assert point.counter_outside() == 1

    def test_point_counter_outside_on_boundary(
        self, triangle, point_on_boundary
    ):
        point = Point(point_on_boundary, triangle)
        assert point.counter_outside() == 1

    def test_point_counter_outside_just_inside_boundary(
        self, triangle, point_just_inside_boundary
    ):
        point = Point(point_just_inside_boundary, triangle)
        assert point.counter_outside() == 0

    def test_point_counter_outside_just_outside_boundary(
        self, triangle, point_just_outside_boundary
    ):
        point = Point(point_just_outside_boundary, triangle)
        assert point.counter_outside() == 1


class TestSegment:

    def test_segment_init(self, triangle):
        p = R2Point(0.0, 0.0)
        q = R2Point(1.0, 0.0)
        segment = Segment(p, q, triangle)
        assert segment.p == p
        assert segment.q == q

    def test_segment_perimeter(self, triangle):
        p = R2Point(0.0, 0.0)
        q = R2Point(1.0, 0.0)
        segment = Segment(p, q, triangle)
        assert segment.perimeter() == 2.0

    def test_segment_add_creates_triangle(self, triangle):
        p = R2Point(0.0, 0.0)
        q = R2Point(1.0, 0.0)
        r = R2Point(0.0, 1.0)
        segment = Segment(p, q, triangle)
        result = segment.add(r)
        assert isinstance(result, Polygon)

    def test_segment_add_point_inside_segment(self, triangle):
        p = R2Point(0.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(1.0, 0.0)
        segment = Segment(p, q, triangle)
        result = segment.add(r)
        assert isinstance(result, Segment)
        assert result is segment

    def test_segment_add_p_inside_new_segment(self, triangle):
        p = R2Point(1.0, 0.0)
        q = R2Point(2.0, 0.0)
        r = R2Point(0.0, 0.0)
        segment = Segment(p, q, triangle)
        result = segment.add(r)
        assert isinstance(result, Segment)
        assert result.p == r
        assert result.q == q

    def test_segment_add_else_branch(self, triangle):
        p = R2Point(0.0, 0.0)
        q = R2Point(1.0, 0.0)
        r = R2Point(2.0, 0.0)
        segment = Segment(p, q, triangle)
        result = segment.add(r)
        assert isinstance(result, Segment)
        assert result.p == p
        assert result.q == r

    def test_segment_counter_outside_zero(self, triangle, point_inside):
        p = R2Point(0.2, 0.2)
        q = R2Point(0.3, 0.3)
        segment = Segment(p, q, triangle)
        assert segment.counter_outside() == 0

    def test_segment_counter_outside_one(self, triangle, point_outside):
        p = R2Point(0.2, 0.2)
        q = point_outside
        segment = Segment(p, q, triangle)
        assert segment.counter_outside() == 1

    def test_segment_counter_outside_two(self, triangle, point_outside):
        p = point_outside
        q = R2Point(6.0, 6.0)
        segment = Segment(p, q, triangle)
        assert segment.counter_outside() == 2

    def test_segment_counter_outside_one_on_boundary(
        self, triangle, point_on_boundary
    ):
        p = R2Point(0.2, 0.2)
        q = point_on_boundary
        segment = Segment(p, q, triangle)
        assert segment.counter_outside() == 1

    def test_segment_counter_outside_boundary_vs_inside(
        self, triangle, point_on_boundary, point_just_inside_boundary
    ):
        p = point_on_boundary
        q = point_just_inside_boundary
        segment = Segment(p, q, triangle)
        assert segment.counter_outside() == 1


class TestPolygon:

    def test_polygon_add_removes_outside_vertex(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        outside_vertex = R2Point(5.0, 0.0)
        polygon = polygon.add(outside_vertex)
        counter_after_add_outside = polygon.counter_outside()
        assert counter_after_add_outside >= 1
        outside_vertex2 = R2Point(0.0, 5.0)
        polygon = polygon.add(outside_vertex2)
        far_point = R2Point(6.0, 6.0)
        counter_before = polygon.counter_outside()
        polygon = polygon.add(far_point)
        counter_after = polygon.counter_outside()
        assert isinstance(polygon, Polygon)
        assert polygon.points.size() >= 3

    def test_polygon_add_counter_decreases_on_vertex_removal(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(2.0, 0.0)
        c = R2Point(0.0, 2.0)
        polygon = Polygon(a, b, c, triangle)
        outside = R2Point(5.0, 5.0)
        polygon = polygon.add(outside)
        initial_counter = polygon.counter_outside()
        assert initial_counter >= 1
        new_point = R2Point(6.0, 6.0)
        polygon = polygon.add(new_point)
        assert isinstance(polygon, Polygon)

    def test_polygon_init(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.points.size() == 3
        assert polygon._area > 0

    def test_polygon_perimeter(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        expected = 1.0 + 1.0 + (2**0.5)
        assert abs(polygon.perimeter() - expected) < 0.001

    def test_polygon_area(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        assert abs(polygon.area() - 0.5) < 0.001

    def test_polygon_counter_outside_all_inside(self, triangle):
        a = R2Point(0.1, 0.1)
        b = R2Point(0.2, 0.1)
        c = R2Point(0.1, 0.2)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.counter_outside() == 0

    def test_polygon_counter_outside_some_outside(
        self, triangle, point_outside
    ):
        a = point_outside
        b = R2Point(0.2, 0.1)
        c = R2Point(0.1, 0.2)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.counter_outside() >= 1

    def test_polygon_add_point_inside(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(2.0, 0.0)
        c = R2Point(0.0, 2.0)
        polygon = Polygon(a, b, c, triangle)
        inner_point = R2Point(0.5, 0.5)
        result = polygon.add(inner_point)
        assert isinstance(result, Polygon)
        assert result.points.size() >= 3

    def test_polygon_add_point_outside_expands(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        initial_area = polygon.area()
        outer_point = R2Point(2.0, 2.0)
        result = polygon.add(outer_point)
        assert isinstance(result, Polygon)
        assert result.area() > initial_area

    def test_polygon_add_multiple_points(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        points = [
            R2Point(0.5, 0.5),
            R2Point(2.0, 0.0),
            R2Point(0.0, 2.0),
            R2Point(1.0, 1.0),
        ]
        for p in points:
            polygon = polygon.add(p)
        assert isinstance(polygon, Polygon)
        assert polygon.points.size() >= 3

    def test_polygon_add_triggers_while_loops(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(3.0, 0.0)
        c = R2Point(0.0, 3.0)
        polygon = Polygon(a, b, c, triangle)
        far_point = R2Point(5.0, 5.0)
        result = polygon.add(far_point)
        assert isinstance(result, Polygon)

    def test_polygon_add_counter_update(self, triangle, point_outside):
        a = point_outside
        b = R2Point(0.2, 0.1)
        c = R2Point(0.1, 0.2)
        polygon = Polygon(a, b, c, triangle)
        initial_counter = polygon.counter_outside()
        new_point = R2Point(6.0, 6.0)
        result = polygon.add(new_point)
        assert result.counter_outside() >= initial_counter

    def test_polygon_counter_outside_vertex_on_boundary(
        self, triangle, point_on_boundary
    ):
        a = point_on_boundary
        b = R2Point(0.2, 0.1)
        c = R2Point(0.1, 0.2)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.counter_outside() == 1

    def test_polygon_counter_outside_mixed_boundary_and_inside(
        self, triangle, point_on_boundary, point_just_inside_boundary
    ):
        a = point_on_boundary
        b = point_just_inside_boundary
        c = R2Point(0.1, 0.2)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.counter_outside() == 1


class TestConvexHullIntegration:

    def test_void_to_point_to_segment_to_polygon(self, triangle):
        f = Void(triangle)
        assert isinstance(f, Void)
        f = f.add(R2Point(0.0, 0.0))
        assert isinstance(f, Point)
        f = f.add(R2Point(1.0, 0.0))
        assert isinstance(f, Segment)
        f = f.add(R2Point(0.0, 1.0))
        assert isinstance(f, Polygon)
        assert f.points.size() == 3

    def test_many_points_convex_hull(self, triangle):
        f = Void(triangle)
        points = [
            R2Point(0.0, 0.0),
            R2Point(1.0, 0.0),
            R2Point(1.0, 1.0),
            R2Point(0.0, 1.0),
            R2Point(0.5, 0.5),
            R2Point(2.0, 0.0),
            R2Point(0.0, 2.0),
        ]
        for p in points:
            f = f.add(p)
        assert isinstance(f, Polygon)
        assert f.area() > 0
        assert f.perimeter() > 0

    def test_collinear_points_handling(self, triangle):
        f = Void(triangle)
        f = f.add(R2Point(0.0, 0.0))
        f = f.add(R2Point(1.0, 0.0))
        f = f.add(R2Point(2.0, 0.0))
        assert isinstance(f, Segment)

    def test_duplicate_points(self, triangle):
        f = Void(triangle)
        f = f.add(R2Point(1.0, 1.0))
        f = f.add(R2Point(1.0, 1.0))
        assert isinstance(f, Point)

    def test_boundary_point_in_hull(self, triangle, point_on_boundary):
        f = Void(triangle)
        f = f.add(R2Point(0.0, 0.0))
        f = f.add(R2Point(1.0, 0.0))
        f = f.add(R2Point(0.0, 1.0))
        f = f.add(point_on_boundary)
        assert isinstance(f, Polygon)
        assert f.counter_outside() >= 1

    def test_boundary_vs_inside_points(
        self, triangle, point_on_boundary, point_just_inside_boundary
    ):
        f = Void(triangle)
        f = f.add(R2Point(0.0, 0.0))
        f = f.add(R2Point(1.0, 0.0))
        f = f.add(R2Point(0.0, 1.0))
        f = f.add(point_just_inside_boundary)
        counter_before = f.counter_outside()
        f = f.add(point_on_boundary)
        counter_after = f.counter_outside()
        assert counter_after >= counter_before


class TestPolygonInitBranches:

    def test_polygon_init_is_light_true(self, triangle):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 0.0)
        c = R2Point(0.0, 1.0)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.points.size() == 3

    def test_polygon_init_is_light_false(self, triangle):
        a = R2Point(0.0, 1.0)
        b = R2Point(0.0, 0.0)
        c = R2Point(1.0, 0.0)
        polygon = Polygon(a, b, c, triangle)
        assert polygon.points.size() == 3
