import math

def _fmt(v):
    return f"{v:g}"

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"({_fmt(self.x)}, {_fmt(self.y)})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def distance_to(self, other):
        return abs(self - other)

class PointSet:
    def __init__(self, points=()):
        self._pts = []
        for p in points:
            self._check(p)
            self._pts.append(p)

    @staticmethod
    def _check(p):
        if not isinstance(p, Point):
            raise TypeError("В наборе могут быть только объекты Point")

    def __len__(self):
        return len(self._pts)

    def __getitem__(self, i):
        return self._pts[i]

    def __setitem__(self, i, point):
        self._check(point)
        self._pts[i] = point

    def __contains__(self, point):
        return point in self._pts

    def __iter__(self):
        return iter(self._pts)

    def __add__(self, other):
        if not isinstance(other, PointSet):
            return NotImplemented
        merged = PointSet(self._pts)
        for p in other:
            if p not in merged:
                merged._pts.append(p)
        return merged

    def __str__(self):
        return "{" + ", ".join(str(p) for p in self._pts) + "}"

    def __repr__(self):
        return f"PointSet({self._pts!r})"

    def _require_nonempty(self):
        if not self._pts:
            raise ValueError("Набор точек пуст")

    def centroid(self):
        self._require_nonempty()
        n = len(self._pts)
        return Point(sum(p.x for p in self._pts) / n, sum(p.y for p in self._pts) / n)

    def nearest_to(self, point):
        self._require_nonempty()
        return min(self._pts, key=lambda p: p.distance_to(point))

    def bounding_box(self):
        self._require_nonempty()
        xs = [p.x for p in self._pts]
        ys = [p.y for p in self._pts]
        return Point(min(xs), min(ys)), Point(max(xs), max(ys))

if __name__ == "__main__":
    p1, p2 = Point(3, 4), Point(1, 2)
    print("p1 =", p1, "| p2 =", p2, "| repr(p1) =", repr(p1))
    print("p1 + p2 =", p1 + p2)
    print("p1 - p2 =", p1 - p2)
    print("abs(p1) =", abs(p1), "(расстояние до начала координат)")
    print(f"p1.distance_to(p2) = {p1.distance_to(p2):.4f}")
    print("p1 == Point(3, 4):", p1 == Point(3, 4), "| p1 == p2:", p1 == p2)
    A = PointSet([Point(0, 0), Point(4, 0), Point(4, 3), Point(1, 5)])
    B = PointSet([Point(4, 3), Point(-2, 1), Point(6, 7)])
    print("\nA =", A)
    print("B =", B)
    print("len(A) =", len(A), "| A[2] =", A[2])
    A[0] = Point(0, 1)
    print("после A[0] = (0, 1):", A)
    print("Point(4, 0) in A:", Point(4, 0) in A, "| Point(9, 9) in A:", Point(9, 9) in A)
    print("\nОбъединение A + B (без дубликатов):")
    C = A + B
    print("C =", C, f"| len = {len(C)}")
    print("\nИтерация по C:")
    for i, p in enumerate(C, 1):
        print(f"  {i}. {str(p):<10} расстояние от начала: {abs(p):.2f}")
    print("\nАнализ набора C:")
    print("Центр масс:", C.centroid())
    target = Point(5, 5)
    near = C.nearest_to(target)
    print(f"Ближайшая к {target}: {near} (расстояние {near.distance_to(target):.3f})")
    lo, hi = C.bounding_box()
    print(f"Ограничивающий прямоугольник: {lo} – {hi}, "
          f"размер {hi.x - lo.x:g}×{hi.y - lo.y:g}")
    print("\nОбработка ошибок:")
    for action in (lambda: PointSet().centroid(), lambda: A.__setitem__(0, (1, 2)),
                   lambda: p1 + 5):
        try:
            action()
        except (ValueError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")
