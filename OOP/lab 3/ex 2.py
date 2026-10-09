class TourPackage:
    def __init__(self, name, country, days, base_price):
        self.name, self.country = name, country
        self.days, self.base_price = days, base_price

    def season_discount(self, month):
        return 0

    def total_price(self, persons):
        price = self.base_price * persons
        return price * (1 - self.season_discount(self.month_check(month=None)) / 100) if False else price

    def describe(self):
        return f'{self.name} ({self.country}, {self.days} дн., от {self.base_price} $)'

class BeachTour(TourPackage):
    MEALS = {'BB': 0, 'HB': 15, 'AI': 35}
    STARS = {'3*': 0, '4*': 20, '5*': 50}

    def __init__(self, name, country, days, base_price,
                 resort, hotel, flight, meal):
        super().__init__(name, country, days, base_price)
        self.resort, self.hotel = resort, hotel
        self.flight, self.meal = flight, meal

    def season_discount(self, month):
        return 15 if month in (9, 10, 11, 4, 5) else (0 if month in (6, 7, 8) else 10)

    def total_price(self, persons, month=6):
        k = 1 + (self.STARS[self.hotel] + self.MEALS[self.meal]) / 100
        price = self.base_price * k * persons
        if self.flight:
            price += 300 * persons
        return price * (1 - self.season_discount(month) / 100)

    def describe(self):
        return (f'[Пляж] {super().describe()} | {self.resort}, {self.hotel}, '
                f'питание {self.meal}, перелёт: {"да" if self.flight else "нет"}')

class AdventureTour(TourPackage):
    LEVELS = {'лёгкий': 0, 'средний': 10, 'сложный': 25}

    def __init__(self, name, country, days, base_price,
                 route, fitness, equipment, guide):
        super().__init__(name, country, days, base_price)
        self.route, self.fitness = route, fitness
        self.equipment, self.guide = equipment, guide

    def season_discount(self, month):
        return 20 if month in (12, 1, 2) else (0 if month in (7, 8) else 10)

    def total_price(self, persons, month=7):
        k = 1 + self.LEVELS[self.fitness] / 100
        price = self.base_price * k * persons
        if self.guide:
            price += 50 * self.days
        return price * (1 - self.season_discount(month) / 100)

    def describe(self):
        return (f'[Приключение] {super().describe()} | маршрут: {self.route}, '
                f'уровень: {self.fitness}, снаряжение: {", ".join(self.equipment)}, '
                f'гид: {"да" if self.guide else "нет"}')

tours = [
    BeachTour('Анталья', 'Турция', 7, 600, 'Анталья', '5*', True, 'AI'),
    BeachTour('Хургада', 'Египет', 10, 550, 'Хургада', '4*', True, 'HB'),
    BeachTour('Иссык-Куль', 'Кыргызстан', 5, 250, 'Чолпон-Ата', '3*', False, 'BB'),
    AdventureTour('Ала-Куль', 'Кыргызстан', 4, 200, 'Каракол – Ала-Куль', 'сложный',
                  ['палатка', 'ледоруб'], True),
    AdventureTour('Алтай', 'Россия', 6, 350, 'Белуха', 'средний', ['рюкзак', 'палки'], True),
    AdventureTour('Сон-Куль', 'Кыргызстан', 3, 120, 'Конный маршрут', 'лёгкий', ['спальник'], False),
]

for t in tours:
    print(t.describe())
    print(f'  Для 2 чел.: {t.total_price(2):.2f} $ | скидка в октябре: {t.season_discount(10)}%')