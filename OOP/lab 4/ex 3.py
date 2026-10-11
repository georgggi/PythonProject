from abc import ABC, abstractmethod

class Beverage(ABC):
    def __init__(self, volume_ml):
        if volume_ml <= 0:
            raise ValueError("Объём должен быть положительным")
        self.volume_ml = volume_ml

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def calories(self) -> float:
        pass

    @abstractmethod
    def price(self) -> float:
        pass

    def kcal_per_100ml(self):
        return self.calories() / self.volume_ml * 100

    def menu_line(self):
        return (f"{self.description():<44s}| {self.volume_ml:>4d} мл | "
                f"{self.calories():6.1f} ккал | {self.price():6.0f} сом")

class Coffee(Beverage):
    KCAL_100 = {"эспрессо": 3, "американо": 2, "капучино": 45, "латте": 55}
    PRICE = {"эспрессо": 90, "американо": 100, "капучино": 150, "латте": 160}

    def __init__(self, kind, volume_ml, milk=False, sugar_spoons=0):
        super().__init__(volume_ml)
        if kind not in self.KCAL_100:
            raise ValueError(f"Неизвестный тип кофе: {kind}")
        if sugar_spoons < 0:
            raise ValueError("Сахар не может быть отрицательным")
        self.kind = kind
        self.milk = milk
        self.sugar_spoons = sugar_spoons

    def description(self):
        extra = ", с молоком" if self.milk else ""
        sugar = f", сахар×{self.sugar_spoons}" if self.sugar_spoons else ""
        return f"Кофе {self.kind}{extra}{sugar}"

    def calories(self):
        kcal = self.KCAL_100[self.kind] * self.volume_ml / 100
        if self.milk and self.kind in ("эспрессо", "американо"):
            kcal += self.volume_ml * 0.15 * 0.6
        return kcal + self.sugar_spoons * 20

    def price(self):
        p = self.PRICE[self.kind] * self.volume_ml / 250
        if self.milk and self.kind in ("эспрессо", "американо"):
            p += 30
        return round(p)


class Tea(Beverage):
    ADDITIVES = {
        "лимон": (3, 10), "мёд": (64, 40), "сахар": (20, 0),
        "мята": (1, 10), "имбирь": (2, 15),
    }
    BASE_PRICE = {"чёрный": 60, "зелёный": 70, "травяной": 80}

    def __init__(self, kind, volume_ml, additives=()):
        super().__init__(volume_ml)
        if kind not in self.BASE_PRICE:
            raise ValueError(f"Неизвестный тип чая: {kind}")
        for a in additives:
            if a not in self.ADDITIVES:
                raise ValueError(f"Неизвестная добавка: {a}")
        self.kind = kind
        self.additives = list(additives)

    def description(self):
        add = f" ({', '.join(self.additives)})" if self.additives else ""
        return f"Чай {self.kind}{add}"

    def calories(self):
        return self.volume_ml / 100 * 1 + sum(self.ADDITIVES[a][0] for a in self.additives)

    def price(self):
        base = self.BASE_PRICE[self.kind] * self.volume_ml / 300
        return round(base + sum(self.ADDITIVES[a][1] for a in self.additives))

class Juice(Beverage):
    KCAL_100 = {"яблоко": 46, "апельсин": 45, "вишня": 54, "томат": 17}

    def __init__(self, fruit, volume_ml, natural=True, concentration=100):
        super().__init__(volume_ml)
        if fruit not in self.KCAL_100:
            raise ValueError(f"Неизвестный фрукт: {fruit}")
        if not 0 < concentration <= 100:
            raise ValueError("Концентрация: от 1 до 100 %")
        self.fruit = fruit
        self.natural = natural
        self.concentration = concentration

    def description(self):
        kind = "сок" if self.natural else f"нектар {self.concentration}%"
        return f"{kind.capitalize()} {self.fruit}"

    def calories(self):
        sugar_added = 0 if self.natural else self.volume_ml * 0.08  # сироп в нектаре
        return self.KCAL_100[self.fruit] * self.volume_ml / 100 * self.concentration / 100 + sugar_added

    def price(self):
        k = 1.0 if self.natural else 0.6
        return round(120 * self.volume_ml / 250 * k)

class Smoothie(Beverage):
    KCAL_PER_ML = {"фруктовый": 0.65, "овощной": 0.30, "протеиновый": 0.90}
    PRICE = {"фруктовый": 190, "овощной": 170, "протеиновый": 230}

    def __init__(self, ingredients, volume_ml, kind):
        super().__init__(volume_ml)
        if kind not in self.KCAL_PER_ML:
            raise ValueError(f"Неизвестный тип смузи: {kind}")
        if not ingredients:
            raise ValueError("Укажите ингредиенты")
        self.ingredients = list(ingredients)
        self.kind = kind

    def description(self):
        return f"Смузи {self.kind} ({', '.join(self.ingredients)})"

    def calories(self):
        return self.KCAL_PER_ML[self.kind] * self.volume_ml

    def price(self):
        return round(self.PRICE[self.kind] * self.volume_ml / 350 + 10 * len(self.ingredients))

if __name__ == "__main__":
    menu = [
        Coffee("эспрессо", 60),
        Coffee("американо", 250, milk=True, sugar_spoons=1),
        Coffee("капучино", 300),
        Coffee("латте", 350, sugar_spoons=2),
        Tea("чёрный", 300, ["лимон"]),
        Tea("зелёный", 300),
        Tea("травяной", 350, ["мёд", "мята", "имбирь"]),
        Juice("апельсин", 250, natural=True),
        Juice("яблоко", 250, natural=False, concentration=50),
        Juice("томат", 200),
        Smoothie(["банан", "клубника", "йогурт"], 350, "фруктовый"),
        Smoothie(["шпинат", "огурец", "сельдерей"], 350, "овощной"),
        Smoothie(["банан", "протеин", "молоко"], 400, "протеиновый"),
    ]

    print("МЕНЮ КАФЕ")
    print("-" * 80)
    for item in menu:
        print(item.menu_line())
    print("-" * 80)

    lowest = min(menu, key=lambda b: b.calories())
    lowest_100 = min(menu, key=lambda b: b.kcal_per_100ml())
    highest = max(menu, key=lambda b: b.calories())
    cheapest = min(menu, key=lambda b: b.price())

    print(f"Самый низкокалорийный напиток (порция): {lowest.description()} — {lowest.calories():.1f} ккал")
    print(f"Самый низкокалорийный на 100 мл: {lowest_100.description()} — {lowest_100.kcal_per_100ml():.1f} ккал")
    print(f"Самый калорийный: {highest.description()} — {highest.calories():.1f} ккал")
    print(f"Самый дешёвый: {cheapest.description()} — {cheapest.price():.0f} сом")

    print("\nТоп-3 напитка с наименьшей калорийностью:")
    for b in sorted(menu, key=lambda b: b.calories())[:3]:
        print(f"  {b.description():<40s} {b.calories():6.1f} ккал")

    print(f"\nЗаказ из всего меню: {sum(b.price() for b in menu):.0f} сом, "
          f"{sum(b.calories() for b in menu):.0f} ккал")