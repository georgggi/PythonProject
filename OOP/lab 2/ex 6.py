class TariffPlan:
    def __init__(self, name, price, speed_mbps, minutes, sms):
        self.__name = name
        self.__price = price
        self.__speed = speed_mbps
        self.__minutes = minutes
        self.__sms = sms

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError('Цена должна быть больше 0')
        self.__price = value

    @property
    def speed(self):
        return self.__speed

    def annual_cost(self):
        return self.__price * 12

    def discount_price(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError('Скидка должна быть от 0 до 100%')
        return round(self.__price * (1 - percent / 100), 2)

    def price_per_mbps(self):
        return round(self.price / self.speed, 2)

    def compare(self, other):
        cheaper = self.name if self.price < other.price else other.name
        faster = self.name if self.speed > other.speed else other.name
        return f'{self.__name} vs {other.name}: дешевле — {cheaper}, быстрее — {faster}'

    def __str__(self):
        return (f'{self.name:9s} | {self.price} сом/мес | {self.__speed:4} Мбит/с | '
                f'{self.__minutes:4} мин | {self.__sms:4} SMS')

plans = [
    TariffPlan('Старт', 300, 30, 200, 50),
    TariffPlan('Оптимум', 500, 100, 500, 100),
    TariffPlan('Премиум', 900, 300, 1000, 300),
    TariffPlan('Безлимит', 1200, 500, 3000, 500),
]
for p in plans:
    print(p)

print()
print(plans[0].compare(plans[1]))
print(f'Годовая стоимость «{plans[1].name}»: {plans[1].annual_cost()} сом')
print(f'«{plans[2].name}» со скидкой 15%: {plans[2].discount_price(15)} сом')

best = min(plans, key=lambda p: p.price_per_mbps())
print(f'Оптимальный (дешевле всего за 1 Мбит/с): {best.name}, {best.price_per_mbps()} сом')