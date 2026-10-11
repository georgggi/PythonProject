import math
from itertools import zip_longest

def _num(v):
    return str(int(v)) if float(v).is_integer() else f"{v:g}"

class Polynomial:
    def __init__(self, coeffs):
        c = list(coeffs)
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self._c = c or [0]

    @staticmethod
    def _coerce(other):
        if isinstance(other, Polynomial):
            return other
        if isinstance(other, (int, float)) and not isinstance(other, bool):
            return Polynomial([other])
        return None

    def degree(self):
        return len(self._c) - 1

    def derivative(self):
        if self.degree() == 0:
            return Polynomial([0])
        return Polynomial([i * self._c[i] for i in range(1, len(self._c))])

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Polynomial([a + b for a, b in zip_longest(self._c, o._c, fillvalue=0)])

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Polynomial([a - b for a, b in zip_longest(self._c, o._c, fillvalue=0)])

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        res = [0] * (len(self._c) + len(o._c) - 1)
        for i, a in enumerate(self._c):
            for j, b in enumerate(o._c):
                res[i + j] += a * b
        return Polynomial(res)

    __rmul__ = __mul__

    def __neg__(self):
        return Polynomial([-a for a in self._c])

    def __len__(self):
        return self.degree() + 1

    def __getitem__(self, i):
        if i < 0:
            raise IndexError("Степень не может быть отрицательной")
        return self._c[i] if i < len(self._c) else 0

    def __setitem__(self, i, value):
        if i < 0:
            raise IndexError("Степень не может быть отрицательной")
        if i >= len(self._c):
            self._c.extend([0] * (i + 1 - len(self._c)))
        self._c[i] = value
        while len(self._c) > 1 and self._c[-1] == 0:
            self._c.pop()

    def __call__(self, x):
        result = 0
        for coef in reversed(self._c):
            result = result * x + coef
        return result

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return NotImplemented
        return len(self._c) == len(other._c) and all(
            math.isclose(a, b, abs_tol=1e-9) for a, b in zip(self._c, other._c))

    __hash__ = None

    def __str__(self):
        terms = []
        for p in range(self.degree(), -1, -1):
            c = self._c[p]
            if c == 0:
                continue
            mag = abs(c)
            if p == 0:
                body = _num(mag)
            else:
                coef = "" if mag == 1 else _num(mag)
                body = f"{coef}x" if p == 1 else f"{coef}x^{p}"
            terms.append(("-" if c < 0 else "+", body))
        if not terms:
            return "0"
        sign, body = terms[0]
        s = ("-" if sign == "-" else "") + body
        for sign, body in terms[1:]:
            s += f" {sign} {body}"
        return s

    def __repr__(self):
        return f"Polynomial({self._c})"

def quadratic_roots(p):
    if p.degree() != 2:
        raise ValueError("Нужен многочлен второй степени")
    a, b, c = p[2], p[1], p[0]
    d = b * b - 4 * a * c
    if d < 0:
        raise ValueError("Вещественных корней нет (D < 0)")
    return (-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a)

def check_vieta(p):
    x1, x2 = quadratic_roots(p)
    a, b, c = p[2], p[1], p[0]
    s_ok = math.isclose(x1 + x2, -b / a)
    p_ok = math.isclose(x1 * x2, c / a)
    print(f"  P(x) = {p}")
    print(f"  корни: x1 = {x1:g}, x2 = {x2:g} | P(x1) = {p(x1):.1e}, P(x2) = {p(x2):.1e}")
    print(f"  x1 + x2 = {x1 + x2:g}, -b/a = {-b / a:g} -> {s_ok}")
    print(f"  x1 * x2 = {x1 * x2:g},  c/a = {c / a:g} -> {p_ok}")
    rebuilt = Polynomial([-x1, 1]) * Polynomial([-x2, 1]) * a
    print(f"  a(x - x1)(x - x2) = {rebuilt} -> совпадает с P: {rebuilt == p}")

if __name__ == "__main__":
    p = Polynomial([-1, 2, 3])
    q = Polynomial([5, 0, 0, 1])
    print("p =", p, "| repr:", repr(p))
    print("q =", q)
    print("p + q =", p + q)
    print("p - q =", p - q)
    print("p * q =", p * q)
    print("-p    =", -p)
    print("p * 2 =", p * 2)
    print(f"\nlen(p) = {len(p)}, degree(p) = {p.degree()}")
    print("p[2] =", p[2], "| p[0] =", p[0], "| p[7] =", p[7])
    p[1] = 4
    print("после p[1] = 4:", p)
    p[1] = 2
    print("p(2) =", p(2), "(3*4 + 2*2 - 1 = 15)")
    print("p(0) =", p(0), "| q(-1) =", q(-1))
    print("\nПроизводные:")
    print("p'  =", p.derivative())
    print("q'  =", q.derivative())
    print("q'' =", q.derivative().derivative())
    print("Polynomial([7]).derivative() =", Polynomial([7]).derivative())
    print("\nРавенство:", Polynomial([1, 2]) == Polynomial([1, 2, 0, 0]),
          "(старшие нули отбрасываются)")
    print("Нулевой многочлен:", Polynomial([0, 0]))
    print("Особые случаи вывода:", Polynomial([0, -1, 0, 1]))
    print("\nТеорема Виета:")
    print("Пример 1:")
    check_vieta(Polynomial([3, -5, 2]))
    print("Пример 2:")
    check_vieta(Polynomial([8, -6, 1]))
    print("\nОшибки:")
    for action in (lambda: quadratic_roots(Polynomial([1, 0, 1])),
                   lambda: p[-1], lambda: p + "x"):
        try:
            action()
        except (ValueError, IndexError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")