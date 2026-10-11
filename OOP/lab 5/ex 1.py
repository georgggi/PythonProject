import math

class Fraction:
    def __init__(self, num, den=1):
        if not isinstance(num, int) or not isinstance(den, int):
            raise TypeError("Числитель и знаменатель должны быть целыми числами")
        if den == 0:
            raise ValueError("Знаменатель не может быть равен нулю")
        if den < 0:
            num, den = -num, -den
        g = math.gcd(num, den)
        self.num = num // g
        self.den = den // g

    @staticmethod
    def _coerce(other):
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other)
        return None

    def __add__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self.num * o.den + o.num * self.den, self.den * o.den)

    __radd__ = __add__

    def __sub__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self.num * o.den - o.num * self.den, self.den * o.den)

    def __rsub__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is None else o - self

    def __mul__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return Fraction(self.num * o.num, self.den * o.den)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        if o.num == 0:
            raise ZeroDivisionError("Деление на нулевую дробь")
        return Fraction(self.num * o.den, self.den * o.num)

    def __neg__(self):
        return Fraction(-self.num, self.den)

    def __abs__(self):
        return Fraction(abs(self.num), self.den)

    def __eq__(self, other):
        o = self._coerce(other)
        if o is None:
            return NotImplemented
        return self.num == o.num and self.den == o.den

    def __hash__(self):
        return hash((self.num, self.den))

    def __lt__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is None else self.num * o.den < o.num * self.den

    def __gt__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is None else self.num * o.den > o.num * self.den

    def __le__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is None else self.num * o.den <= o.num * self.den

    def __ge__(self, other):
        o = self._coerce(other)
        return NotImplemented if o is None else self.num * o.den >= o.num * self.den

    def __float__(self):
        return self.num / self.den

    def __int__(self):
        q = abs(self.num) // self.den
        return q if self.num >= 0 else -q

    def __str__(self):
        return f"{self.num}/{self.den}"

    def __repr__(self):
        return f"Fraction({self.num}, {self.den})"

if __name__ == "__main__":
    a, b = Fraction(1, 3), Fraction(1, 6)
    print("a =", a, "| b =", b, "| repr(a) =", repr(a))
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a / b = {a / b}")
    print(f"-a = {-a} | abs(Fraction(-3, 4)) = {abs(Fraction(-3, 4))}")
    print("\nАвтосокращение и знак:")
    print("Fraction(6, 8)   ->", Fraction(6, 8))
    print("Fraction(3, -9)  ->", Fraction(3, -9), "(знак в числителе)")
    print("Fraction(0, 5)   ->", Fraction(0, 5))
    print("\nСравнения a=1/3, b=1/6:")
    print("a == b:", a == b, "| a < b:", a < b, "| a > b:", a > b,
          "| a <= b:", a <= b, "| a >= b:", a >= b)
    print("Fraction(2, 6) == Fraction(1, 3):", Fraction(2, 6) == Fraction(1, 3))
    print("\nПреобразования:")
    x = Fraction(-7, 2)
    print(f"x = {x}: float = {float(x)}, int = {int(x)}")
    print("\nСмешанные операции с int:")
    print("Fraction(1, 2) + 1 =", Fraction(1, 2) + 1)
    print("2 * Fraction(3, 4) =", 2 * Fraction(3, 4))
    print("\nЦепочка (1/3 + 1/6) * 4/5 - 1/10:")
    step1 = Fraction(1, 3) + Fraction(1, 6)
    step2 = step1 * Fraction(4, 5)
    result = step2 - Fraction(1, 10)
    print(f"  1/3 + 1/6      = {step1}")
    print(f"  (...) * 4/5    = {step2}")
    print(f"  (...) - 1/10   = {result}  ≈ {float(result):.4f}")
    print("\nСортировка и sum():")
    fr = [Fraction(3, 4), Fraction(1, 2), Fraction(5, 6), Fraction(1, 3)]
    print("sorted:", [str(f) for f in sorted(fr)])
    print("sum   :", sum(fr))
    print("в set :", len({Fraction(1, 2), Fraction(2, 4), Fraction(3, 6)}), "уникальная дробь")
    print("\nОбработка ошибок:")
    for action in (lambda: Fraction(1, 0), lambda: Fraction(1, 2) / Fraction(0, 3),
                   lambda: Fraction(1, 2) + 0.5, lambda: Fraction(1.5, 2)):
        try:
            action()
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")