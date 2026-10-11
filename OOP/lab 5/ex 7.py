def _fmt(v):
    return f"{v:g}"

class Interval:
    def __init__(self, start, end):
        if start > end:
            raise ValueError(f"Начало ({start}) не может быть больше конца ({end})")
        self.start, self.end = start, end

    @property
    def length(self):
        return self.end - self.start

    def __contains__(self, x):
        return self.start <= x <= self.end

    def __and__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        lo, hi = max(self.start, other.start), min(self.end, other.end)
        return Interval(lo, hi) if lo <= hi else None

    def __or__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return Interval(min(self.start, other.start), max(self.end, other.end))

    def __add__(self, shift):
        if not isinstance(shift, (int, float)) or isinstance(shift, bool):
            return NotImplemented
        return Interval(self.start + shift, self.end + shift)

    __radd__ = __add__

    def __len__(self):
        return int(self.length)

    def __bool__(self):
        return self.length != 0

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __str__(self):
        return f"[{_fmt(self.start)}, {_fmt(self.end)}]"

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

    def overlaps(self, other):
        return (self & other) is not None

    def split(self, n):
        if not isinstance(n, int) or n < 1:
            raise ValueError("n должно быть целым числом >= 1")
        step = self.length / n
        parts = []
        for i in range(n):
            lo = self.start + i * step
            hi = self.end if i == n - 1 else self.start + (i + 1) * step
            parts.append(Interval(lo, hi))
        return parts

if __name__ == "__main__":
    a = Interval(1, 5)
    b = Interval(3, 8)
    c = Interval(10, 12)
    print("a =", a, "| b =", b, "| c =", c, "| repr(a) =", repr(a))
    print("\nПринадлежность (оператор in):")
    for x in (0, 1, 3.5, 5, 6):
        print(f"  {x} in {a}: {x in a}")
    print("\nОперации:")
    print("a & b =", a & b, "(пересечение)")
    print("a & c =", a & c, "(пустое пересечение -> None)")
    print("a | b =", a | b, "(охватывающий)")
    print("a | c =", a | c, "(охватывающий, включает «дыру»)")
    print("a + 10 =", a + 10, "| 2.5 + a =", 2.5 + a, "(сдвиг)")
    print("Касание: Interval(0, 2) & Interval(2, 5) =", Interval(0, 2) & Interval(2, 5))
    print("\nДлина:")
    print("len(a) =", len(a), "| len(Interval(0, 2.9)) =", len(Interval(0, 2.9)),
          "| a.length =", a.length)
    print("\nСравнение:")
    print("a == Interval(1, 5):", a == Interval(1, 5), "| a == b:", a == b)
    print("\nbool():")
    point = Interval(7, 7)
    print(f"bool({a}) = {bool(a)} | bool({point}) = {bool(point)}")
    print("\nПересечение интервалов (overlaps):")
    print("a.overlaps(b):", a.overlaps(b), "| a.overlaps(c):", a.overlaps(c))
    print("\nРазбиение (split):")
    for n in (2, 4):
        print(f"Interval(0, 10).split({n}) =", [str(p) for p in Interval(0, 10).split(n)])
    print("Interval(0, 1).split(3) =", [str(p) for p in Interval(0, 1).split(3)])
    print("\nПрактика: объединение нескольких интервалов занятости")
    busy = [Interval(9, 11), Interval(10, 12), Interval(14, 15), Interval(14.5, 16)]
    merged = []
    for iv in sorted(busy, key=lambda i: i.start):
        if merged and merged[-1].overlaps(iv):
            merged[-1] = merged[-1] | iv
        else:
            merged.append(iv)
    print("Исходные:", [str(i) for i in busy])
    print("Объединённые:", [str(i) for i in merged])
    print("\nОбработка ошибок:")
    for action in (lambda: Interval(5, 1), lambda: a.split(0), lambda: a + "x", lambda: a & 5):
        try:
            action()
        except (ValueError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")