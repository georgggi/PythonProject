from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")

def _to_decimal(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float, str)) and not isinstance(value, bool):
        try:
            return Decimal(str(value))
        except InvalidOperation:
            raise ValueError(f"Некорректная сумма: {value!r}") from None
    raise TypeError(f"Недопустимый тип суммы: {type(value).__name__}")

class Money:
    def __init__(self, amount, currency="KGS"):
        if not isinstance(currency, str) or len(currency) != 3:
            raise ValueError("Валюта задаётся трёхбуквенным кодом (KGS, USD...)")
        self.amount = _to_decimal(amount)
        self.currency = currency.upper()

    def _check_same(self, other):
        if self.currency != other.currency:
            raise ValueError(f"Разные валюты: {self.currency} и {other.currency}")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, k):
        if isinstance(k, Money):
            return NotImplemented
        try:
            return Money(self.amount * _to_decimal(k), self.currency)
        except TypeError:
            return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, k):
        if isinstance(k, Money):
            return NotImplemented
        try:
            d = _to_decimal(k)
        except TypeError:
            return NotImplemented
        if d == 0:
            raise ZeroDivisionError("Деление суммы на ноль")
        return Money(self.amount / d, self.currency)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.currency == other.currency and self.amount == other.amount

    def __hash__(self):
        return hash((self.amount, self.currency))

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return self.amount < other.amount

    def __gt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return self.amount > other.amount

    def __le__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return self.amount <= other.amount

    def __ge__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_same(other)
        return self.amount >= other.amount

    def __abs__(self):
        return Money(abs(self.amount), self.currency)

    def __bool__(self):
        return self.amount != 0

    def __round__(self, ndigits=0):
        ndigits = 0 if ndigits is None else ndigits
        q = Decimal(1).scaleb(-ndigits)
        return Money(self.amount.quantize(q, rounding=ROUND_HALF_UP), self.currency)

    def convert(self, rate, currency):
        if _to_decimal(rate) <= 0:
            raise ValueError("Курс должен быть положительным")
        return Money(self.amount * _to_decimal(rate), currency)

    def __str__(self):
        return f"{self.amount.quantize(CENT, rounding=ROUND_HALF_UP):.2f} {self.currency}"

    def __repr__(self):
        return f"Money({str(self.amount)!r}, {self.currency!r})"

if __name__ == "__main__":
    a = Money("1500.50")
    b = Money(499.5)
    print("a =", a, "| b =", b, "| repr(a) =", repr(a))
    print("a + b =", a + b)
    print("a - b =", a - b)
    print("b - a =", b - a, "| abs(b - a) =", abs(b - a))
    print("a * 3 =", a * 3, "| 2 * b =", 2 * b)
    print("a / 4 =", a / 4)
    print("\nТочность Decimal против float:")
    print("0.1 + 0.2 (float) =", 0.1 + 0.2)
    print("Money(0.1) + Money(0.2) =", Money(0.1) + Money(0.2))
    print("\nСравнения a и b:")
    print("a == b:", a == b, "| a < b:", a < b, "| a > b:", a > b,
          "| a <= b:", a <= b, "| a >= b:", a >= b)
    print("Money(100) == Money('100.00'):", Money(100) == Money("100.00"))
    print("Money(100) == Money(100, 'USD'):", Money(100) == Money(100, "USD"))
    print("\nОкругление:")
    x = Money(10) / 3
    print("Money(10) / 3 =", x, "| хранится как", x.amount)
    print("round(Money('2.675'), 2) =", round(Money("2.675"), 2))
    print("round(Money('1234.5')) =", round(Money("1234.5")))
    print("\nbool():")
    print("bool(Money(0)) =", bool(Money(0)), "| bool(a) =", bool(a))
    print("\nКонвертация (условный курс 1 KGS = 0.0114 USD):")
    usd = a.convert("0.0114", "USD")
    print(f"{a} -> {usd}")
    print("\nСмета расходов на мероприятие:")
    items = [("Аренда зала", Money(12000), 1), ("Кофе-брейк", Money("350.50"), 40),
             ("Раздаточные материалы", Money(85), 60), ("Диплом участника", Money("120.00"), 25),
             ("Работа ведущего", Money(5000), 1)]
    print("-" * 58)
    total = Money(0)
    for name, price, qty in items:
        line = price * qty
        total = total + line
        print(f"{name:<24s}{str(price):>14s} × {qty:<3d}{str(line):>14s}")
    print("-" * 58)
    vat = round(total * "0.12", 2)
    print(f"{'Итого без НДС':<42s}{str(total):>16s}")
    print(f"{'НДС 12 %':<42s}{str(vat):>16s}")
    grand = total + vat
    print(f"{'ВСЕГО':<42s}{str(grand):>16s}")
    print(f"На одного участника (25 чел.): {round(grand / 25, 2)}")
    budget = Money(60000)
    print(f"Бюджет {budget}: ", "превышен на " + str(grand - budget) if grand > budget
          else "уложились, остаток " + str(budget - grand))
    print("Самая дорогая позиция:", max(items, key=lambda it: it[1] * it[2])[0])
    print("\nОбработка ошибок:")
    for action in (lambda: Money(100) + Money(5, "USD"), lambda: Money(100) < Money(5, "USD"),
                   lambda: Money(100) / 0, lambda: Money(100) + 5,
                   lambda: Money(100) * Money(2), lambda: Money(5, "RUBL")):
        try:
            action()
        except (ValueError, ZeroDivisionError, TypeError) as e:
            print(f"  {type(e).__name__}: {e}")