import math

def _fmt(v):
    return f"{v:.4g}"

class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def __add__(self, other):
        if not isinstance(other, Vector3D):
            return NotImplemented
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if not isinstance(other, Vector3D):
            return NotImplemented
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k):
        if not isinstance(k, (int, float)) or isinstance(k, bool):
            return NotImplemented
        return Vector3D(self.x * k, self.y * k, self.z * k)

    __rmul__ = __mul__

    def __neg__(self):
        return Vector3D(-self.x, -self.y, -self.z)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __eq__(self, other):
        if not isinstance(other, Vector3D):
            return NotImplemented
        return (math.isclose(self.x, other.x, abs_tol=1e-9) and
                math.isclose(self.y, other.y, abs_tol=1e-9) and
                math.isclose(self.z, other.z, abs_tol=1e-9))

    def __hash__(self):
        return hash((round(self.x, 9), round(self.y, 9), round(self.z, 9)))

    def __str__(self):
        return f"({_fmt(self.x)}, {_fmt(self.y)}, {_fmt(self.z)})"

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __len__(self):
        return 3

    def length(self):
        return abs(self)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.x)

    def normalize(self):
        n = abs(self)
        if n == 0:
            raise ZeroDivisionError("Нельзя нормализовать нулевой вектор")
        return Vector3D(self.x / n, self.y / n, self.z / n)

    def angle_between(self, other):
        n = abs(self) * abs(other)
        if n == 0:
            raise ZeroDivisionError("Угол с нулевым вектором не определён")
        cos = max(-1.0, min(1.0, self.dot(other) / n))
        return math.degrees(math.acos(cos))

    def is_orthogonal(self, other):
        return math.isclose(self.dot(other), 0.0, abs_tol=1e-9)


if __name__ == "__main__":
    a = Vector3D(1, 2, 3)
    b = Vector3D(4, -5, 6)
    print("a =", a, "| b =", b)
    print("repr(a) =", repr(a), "| len(a) =", len(a))
    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * 2 =", a * 2, "| 3 * a =", 3 * a)
    print("-a    =", -a)
    print(f"abs(a) = {abs(a):.4f} | a.length() = {a.length():.4f}")
    print("a == Vector3D(1, 2, 3):", a == Vector3D(1, 2, 3), "| a == b:", a == b)
    print("\nСкалярное и векторное произведения:")
    print("a · b =", a.dot(b))
    c = a.cross(b)
    print("a × b =", c)
    print("(a × b) ⟂ a:", c.is_orthogonal(a), "| (a × b) ⟂ b:", c.is_orthogonal(b))
    print("\nНормализация:")
    n = a.normalize()
    print(f"a.normalize() = ({n.x:.4f}, {n.y:.4f}, {n.z:.4f}), длина = {abs(n):.4f}")
    print("\nУглы между векторами:")
    i, j, k = Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)
    print(f"угол(i, j)       = {i.angle_between(j):.2f}°")
    print(f"угол(i, i+j)     = {i.angle_between(i + j):.2f}°")
    print(f"угол(i, -i)      = {i.angle_between(-i):.2f}°")
    print(f"угол(a, b)       = {a.angle_between(b):.2f}°")
    print("\nПроверка ортогональности:")
    for name, (u, v) in {"i и j": (i, j), "i и k": (i, k), "a и b": (a, b),
                         "(1,2,0) и (-2,1,5)": (Vector3D(1, 2, 0), Vector3D(-2, 1, 5))}.items():
        print(f"  {name:<20s} dot = {u.dot(v):>5.1f} -> ортогональны: {u.is_orthogonal(v)}")
    print("i × j == k:", i.cross(j) == k)
    print("\nОбработка ошибок:")
    for action in (lambda: Vector3D().normalize(), lambda: a * b, lambda: a + 5):
        try:
            action()
        except (ZeroDivisionError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")