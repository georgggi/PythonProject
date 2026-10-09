class Recipe:
    def __init__(self, dish_name, cuisine, cook_time, difficulty, servings):
        self.dish_name = dish_name
        self.cuisine = cuisine
        self.cook_time = cook_time
        self.difficulty = difficulty
        self.servings = servings

    def is_quick(self, limit):
        return self.cook_time < limit

    def describe(self):
        return (f'{self.dish_name} ({self.cuisine} кухня) | '
                f'{self.cook_time} мин | {self.difficulty} | '
                f'порций: {self.servings}')

    def per_person_time(self):
        if self.servings <= 0:
            return 'Ошибка: число порций должно быть > 0'
        return round(self.cook_time / self.servings, 1)

recipes = [
    Recipe('Паста карбонара', 'итальянская', 25, 'лёгкий', 2),
    Recipe('Суши-роллы', 'японская', 60, 'сложный', 4),
    Recipe('Бешбармак', 'кыргызская', 150, 'средний', 6),
    Recipe('Буррито', 'мексиканская', 30, 'лёгкий', 3),
]

for r in recipes:
    print(r.describe())
    print(f'  Быстрое (<40 мин): {r.is_quick(40)}')
    print(f'  Время на порцию: {r.per_person_time()} мин')