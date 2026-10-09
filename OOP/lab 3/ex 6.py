class Food:
    def __init__(self, name, kcal, protein, fat, carbs, price_kg):
        self.name, self.kcal = name, kcal
        self.protein, self.fat, self.carbs = protein, fat, carbs
        self.price_kg = price_kg

    def label(self):
        return (f'{self.name}: {self.kcal} ккал/100г | '
                f'Б {self.protein} / Ж {self.fat} / У {self.carbs} г | {self.price_kg} сом/кг')

    def calories_per_serving(self, serving_g):
        return self.kcal * serving_g / 100

class Dairy(Food):
    TYPES = ('молоко', 'кефир', 'йогурт', 'сыр')

    def __init__(self, name, kcal, protein, fat, carbs, price_kg,
                 fat_percent, shelf_days, dairy_type):
        super().__init__(name, kcal, protein, fat, carbs, price_kg)
        if dairy_type not in self.TYPES:
            raise ValueError('Недопустимый тип молочного продукта')
        self.fat_percent, self.shelf_days, self.dairy_type = fat_percent, shelf_days, dairy_type

    def is_fresh(self, days):
        return days <= self.shelf_days

    def label(self):
        return (f'[{self.dairy_type}] {super().label()} | жирность {self.fat_percent}%, '
                f'срок {self.shelf_days} дн.')

class Bakery(Food):
    TYPES = ('хлеб', 'булочка', 'торт')

    def __init__(self, name, kcal, protein, fat, carbs, price_kg,
                 ingredients, weight_g, bakery_type):
        super().__init__(name, kcal, protein, fat, carbs, price_kg)
        if bakery_type not in self.TYPES:
            raise ValueError('Недопустимый тип выпечки')
        self.ingredients, self.weight_g, self.bakery_type = ingredients, weight_g, bakery_type

    def label(self):
        return (f'[{self.bakery_type}] {super().label()} | вес {self.weight_g} г | '
                f'состав: {", ".join(self.ingredients)}')

    def calories_per_serving(self, serving_g=None):
        return super().calories_per_serving(serving_g or self.weight_g)

products = [
    Dairy('Молоко', 60, 3.0, 3.2, 4.7, 90, 3.2, 5, 'молоко'),
    Dairy('Кефир', 52, 3.4, 2.5, 4.0, 85, 2.5, 7, 'кефир'),
    Dairy('Сыр', 350, 24, 28, 0.5, 700, 45, 60, 'сыр'),
    Bakery('Хлеб белый', 250, 8, 3, 50, 60, ['мука', 'вода', 'дрожжи'], 400, 'хлеб'),
    Bakery('Булочка с маком', 330, 8, 10, 52, 150, ['мука', 'мак', 'сахар'], 100, 'булочка'),
    Bakery('Наполеон', 420, 5, 25, 45, 800, ['мука', 'масло', 'крем'], 150, 'торт'),
]

for p in products:
    print(p.label())
    print(f'  Порция 150 г: {p.calories_per_serving(150):.0f} ккал')

for p in products:
    if isinstance(p, Dairy):
        print(f'{p.name} через 6 дней свежий? {p.is_fresh(6)}')