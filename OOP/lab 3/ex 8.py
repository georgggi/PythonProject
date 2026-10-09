class Mountain:
    def __init__(self, name, height, country, first_ascent):
        self.name, self.height = name, height
        self.country, self.first_ascent = country, first_ascent

    def is_highaltitude(self):
        return self.height > 5000

    def describe(self):
        return (f'{self.name} ({self.country}), {self.height} м, '
                f'первое восхождение: {self.first_ascent}')

    def climbing_difficulty(self):
        return 'не определена'

class Peak(Mountain):
    LEVELS = {1: 'очень лёгкая', 2: 'лёгкая', 3: 'средняя', 4: 'сложная', 5: 'экстремальная'}

    def __init__(self, name, height, country, first_ascent,
                 difficulty, route_type, length_km):
        super().__init__(name, height, country, first_ascent)
        if difficulty not in self.LEVELS:
            raise ValueError('Сложность 1–5')
        self.difficulty, self.route_type, self.length_km = difficulty, route_type, length_km

    def climbing_difficulty(self):
        return f'{self.LEVELS[self.difficulty]} ({self.difficulty}/5)'

    def describe(self):
        return (f'[Вершина] {super().describe()} | маршрут: {self.route_type}, '
                f'{self.length_km} км | сложность: {self.climbing_difficulty()}')

class Volcano(Mountain):
    def __init__(self, name, height, country, first_ascent,
                 status, last_eruption, crater_m):
        super().__init__(name, height, country, first_ascent)
        self.status, self.last_eruption, self.crater_m = status, last_eruption, crater_m

    def climbing_difficulty(self):
        return {'активный': 'опасно, нужно разрешение',
                'спящий': 'умеренно, возможна активность',
                'потухший': 'безопасно'}[self.status]

    def describe(self):
        return (f'[Вулкан] {super().describe()} | {self.status}, '
                f'извержение: {self.last_eruption}, кратер {self.crater_m} м | '
                f'{self.climbing_difficulty()}')

mountains = [
    Peak('Победа', 7439, 'Кыргызстан', 1938, 5, 'ледовый', 25),
    Peak('Ленина', 7134, 'Кыргызстан', 1928, 3, 'смешанный', 18),
    Peak('Алтын-Арашан', 4000, 'Кыргызстан', 1950, 2, 'скальный', 10),
    Volcano('Фудзи', 3776, 'Япония', 663, 'спящий', 1707, 500),
    Volcano('Этна', 3357, 'Италия', 1800, 'активный', 2024, 300),
    Volcano('Килиманджаро', 5895, 'Танзания', 1889, 'потухший', -360000, 2400),
]

for m in mountains:
    print(m.describe())
    print(f'  Высокогорная: {m.is_highaltitude()}\n')

print('Высокогорные:', [m.name for m in mountains if m.is_highaltitude()])
print('Самая высокая:', max(mountains, key=lambda m: m.height).name)