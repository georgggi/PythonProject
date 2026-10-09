class Smartphone:
    def __init__(self, brand, model, ram_gb, battery_mah, year, price):
        self.brand = brand
        self.model = model
        self.ram_gb = ram_gb
        self.battery_mah = battery_mah
        self.year = year
        self.price = price

    def describe(self):
        return (f'{self.brand} {self.model} ({self.year}): ОЗУ {self.ram_gb} ГБ, '
                f'аккумулятор {self.battery_mah} мАч, цена {self.price} $')

    def is_flagship(self, min_ram=8):
        return self.ram_gb >= min_ram

    def battery_days(self, usage_mah_per_day):
        if usage_mah_per_day <= 0:
            return 'Ошибка: расход должен быть > 0'
        return round(self.battery_mah / usage_mah_per_day, 1)

phones = [
    Smartphone('Samsung', 'Galaxy S24', 8, 4000, 2024, 800),
    Smartphone('Apple', 'iPhone 15', 6, 3349, 2023, 900),
    Smartphone('Xiaomi', 'Redmi Note 13', 6, 5000, 2024, 250),
    Smartphone('Google', 'Pixel 8 Pro', 12, 5050, 2023, 950),
]

for p in phones:
    print(p.describe())
    print(f'  Флагман: {p.is_flagship()} | '
          f'Дней без зарядки (расход 1500 мАч): {p.battery_days(1500)}')