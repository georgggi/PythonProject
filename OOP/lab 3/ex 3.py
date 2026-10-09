class Appliance:
    ENERGY = ['C', 'B', 'A', 'A+', 'A++']

    def __init__(self, brand, power_w, price, energy_class):
        self.brand, self.power_w = brand, power_w
        self.price, self.energy_class = price, energy_class

    def spec(self):
        return (f'{self.brand} | {self.power_w} Вт | {self.price} сом | '
                f'класс {self.energy_class}')

    def energy_cost(self, hours, rate):
        """Стоимость электроэнергии: кВт·ч × тариф."""
        return self.power_w / 1000 * hours * rate

    def compare(self, other):
        r = [f'Цена: {self.brand} {self.price} vs {other.brand} {other.price}']
        r.append(f'Мощность: {self.power_w} vs {other.power_w} Вт')
        a, b = self.ENERGY.index(self.energy_class), self.ENERGY.index(other.energy_class)
        better = self.brand if a > b else other.brand if b > a else 'одинаково'
        r.append(f'Эффективнее по классу: {better}')
        return '\n'.join(r)

class WashingMachine(Appliance):
    def __init__(self, brand, power_w, price, energy_class, drum_kg, modes, temp):
        super().__init__(brand, power_w, price, energy_class)
        self.drum_kg, self.modes, self.temp = drum_kg, modes, temp

    def spec(self):
        return (f'[Стиралка] {super().spec()} | барабан {self.drum_kg} кг | '
                f'режимы: {", ".join(self.modes)} | до {self.temp}°C')

class Refrigerator(Appliance):
    def __init__(self, brand, power_w, price, energy_class, volume_l, chambers, freezer_t):
        super().__init__(brand, power_w, price, energy_class)
        self.volume_l, self.chambers, self.freezer_t = volume_l, chambers, freezer_t

    def spec(self):
        return (f'[Холодильник] {super().spec()} | {self.volume_l} л | '
                f'камер: {self.chambers} | морозилка {self.freezer_t}°C')

    def energy_cost(self, hours, rate):
        return super().energy_cost(hours, rate) * 0.4

w1 = WashingMachine('LG', 2000, 35000, 'A+', 8, ['хлопок', 'синтетика', 'быстрая'], 90)
w2 = WashingMachine('Bosch', 2200, 42000, 'A++', 9, ['хлопок', 'эко', 'шерсть'], 95)
f1 = Refrigerator('Samsung', 150, 60000, 'A+', 350, 2, -18)
f2 = Refrigerator('Atlant', 130, 38000, 'A', 280, 2, -18)

devices = [w1, w2, f1, f2]
for d in devices:
    print(d.spec())
    print(f'  Работа 10 ч при тарифе 3 сом/кВт·ч: {d.energy_cost(10, 3):.2f} сом')

print('\nСравнение стиральных машин:')
print(w1.compare(w2))
print('\nСравнение холодильников:')
print(f1.compare(f2))