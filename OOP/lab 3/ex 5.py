class Property:
    CURRENT_YEAR = 2026

    def __init__(self, address, area, price, year_built):
        self.address, self.area = address, area
        self.price, self.year_built = price, year_built

    def price_per_sqm(self):
        return self.price / self.area

    def is_affordable(self, budget):
        return self.price <= budget

    def age(self):
        return self.CURRENT_YEAR - self.year_built

    def describe(self):
        return (f'{self.address} | {self.area} м² | {self.price:,} $ | '
                f'{self.age()} лет | {self.price_per_sqm():.0f} $/м²')

class Apartment(Property):
    def __init__(self, address, area, price, year_built,
                 floor, rooms, balcony, kind):
        super().__init__(address, area, price, year_built)
        self.floor, self.rooms = floor, rooms
        self.balcony, self.kind = balcony, kind

    def describe(self):
        return (f'[Квартира] {super().describe()} | {self.rooms}-комн., '
                f'этаж {self.floor}, балкон: {"да" if self.balcony else "нет"}, {self.kind}')

class House(Property):
    def __init__(self, address, area, price, year_built,
                 floors, plot_sotka, material, garage):
        super().__init__(address, area, price, year_built)
        self.floors, self.plot_sotka = floors, plot_sotka
        self.material, self.garage = material, garage

    def describe(self):
        return (f'[Дом] {super().describe()} | {self.floors} эт., '
                f'участок {self.plot_sotka} сот., {self.material}, '
                f'гараж: {"да" if self.garage else "нет"}')

objects = [
    Apartment('Бишкек, ул. Ахунбаева 1', 65, 70000, 2023, 5, 2, True, 'новостройка'),
    Apartment('Бишкек, ул. Токтогула 10', 48, 52000, 1985, 3, 2, False, 'вторичка'),
    Apartment('Ош, ул. Ленина 5', 90, 85000, 2020, 7, 3, True, 'новостройка'),
    House('Чолпон-Ата, ул. Озёрная 3', 150, 120000, 2015, 2, 8, 'кирпич', True),
    House('Токмок, ул. Садовая 7', 110, 65000, 1998, 1, 6, 'газобетон', False),
    House('Каракол, ул. Горная 12', 130, 90000, 2010, 2, 10, 'дерево', True),
]

for o in objects:
    print(o.describe())

budget = 80000
print(f'\nДоступно при бюджете {budget} $:')
for o in objects:
    if o.is_affordable(budget):
        print(' -', o.address)

best = min(objects, key=lambda o: o.price_per_sqm())
print(f'\nЛучшее соотношение цена/площадь: {best.address} ({best.price_per_sqm():.0f} $/м²)')