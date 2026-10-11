class Time:
    def __init__(self, hours=0, minutes=0, seconds=0):
        for v in (hours, minutes, seconds):
            if not isinstance(v, int):
                raise TypeError("Часы, минуты и секунды должны быть целыми")
        total = hours * 3600 + minutes * 60 + seconds
        if total < 0:
            raise ValueError("Время не может быть отрицательным")
        self._total = total

    @property
    def hours(self):
        return self._total // 3600

    @property
    def minutes(self):
        return self._total % 3600 // 60

    @property
    def seconds(self):
        return self._total % 60

    @classmethod
    def from_seconds(cls, s):
        if s < 0:
            raise ValueError("Количество секунд не может быть отрицательным")
        return cls(0, 0, int(s))

    def to_minutes(self):
        return self._total / 60

    def __int__(self):
        return self._total

    def __bool__(self):
        return self._total != 0

    def __add__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return Time.from_seconds(self._total + other._total)

    def __sub__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        if other._total > self._total:
            raise ValueError(f"Результат отрицательный: {self} - {other}")
        return Time.from_seconds(self._total - other._total)

    def __eq__(self, other):
        if not isinstance(other, Time):
            return NotImplemented
        return self._total == other._total

    def __hash__(self):
        return hash(self._total)

    def __lt__(self, other):
        return self._total < other._total if isinstance(other, Time) else NotImplemented

    def __le__(self, other):
        return self._total <= other._total if isinstance(other, Time) else NotImplemented

    def __gt__(self, other):
        return self._total > other._total if isinstance(other, Time) else NotImplemented

    def __ge__(self, other):
        return self._total >= other._total if isinstance(other, Time) else NotImplemented

    def __str__(self):
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def __repr__(self):
        return f"Time({self.hours}, {self.minutes}, {self.seconds})"

if __name__ == "__main__":
    t1 = Time(1, 30, 45)
    t2 = Time(0, 45, 30)
    print("t1 =", t1, "| t2 =", t2, "| repr(t1) =", repr(t1))
    print("\nНормализация в конструкторе:")
    print("Time(0, 0, 135)  ->", Time(0, 0, 135))
    print("Time(0, 150, 0)  ->", Time(0, 150, 0))
    print("Time(1, 59, 61)  ->", Time(1, 59, 61))
    print("\nАрифметика:")
    print("t1 + t2 =", t1 + t2)
    print("t1 - t2 =", t1 - t2)
    print("Time(0, 59, 59) + Time(0, 0, 1) =", Time(0, 59, 59) + Time(0, 0, 1))
    print("\nСравнения t1 и t2:")
    print("t1 == t2:", t1 == t2, "| t1 < t2:", t1 < t2, "| t1 <= t2:", t1 <= t2,
          "| t1 > t2:", t1 > t2, "| t1 >= t2:", t1 >= t2)
    print("Time(0, 90) == Time(1, 30):", Time(0, 90) == Time(1, 30))
    print("\nПреобразования:")
    print("int(t1) =", int(t1), "секунд")
    print(f"t1.to_minutes() = {t1.to_minutes():.2f} мин")
    print("Time.from_seconds(3725) =", Time.from_seconds(3725))
    print("\nbool():")
    print("bool(Time()) =", bool(Time()), "| bool(Time(0, 0, 1)) =", bool(Time(0, 0, 1)))
    if not Time():
        print("Нулевое время считается «пустым» (False)")
    print("\nРасписание занятий (начало, длительность пары):")
    lessons = [
        ("Программирование", Time(11, 50), Time(1, 30)),
        ("Математика", Time(8, 30), Time(1, 30)),
        ("ООП", Time(13, 30), Time(1, 30)),
        ("Физика", Time(10, 10), Time(1, 30)),
    ]
    lessons.sort(key=lambda item: item[1])        # сортировка работает через __lt__
    print("-" * 62)
    print(f"{'Предмет':<18s}{'Начало':>10s}{'Конец':>10s}{'Перерыв до':>14s}")
    print("-" * 62)
    prev_end = None
    for name, start, dur in lessons:
        end = start + dur
        pause = str(start - prev_end) if prev_end is not None else "—"
        print(f"{name:<18s}{str(start):>10s}{str(end):>10s}{pause:>14s}")
        prev_end = end
    print("-" * 62)
    total = sum((d for _, _, d in lessons), Time())
    print(f"Всего занятий: {len(lessons)}, суммарное время: {total} "
          f"({total.to_minutes():.0f} мин)")
    first, last = lessons[0][1], prev_end
    print(f"Университетский день: {first} – {last}, длительность {last - first}")
    print("\nОбработка ошибок:")
    for action in (lambda: Time(0, 10) - Time(1, 0), lambda: Time(-1, 0, 0),
                   lambda: Time(1.5, 0, 0), lambda: Time(1) + 5):
        try:
            action()
        except (ValueError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")
