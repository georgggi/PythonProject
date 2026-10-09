class Pet:
    category = 'Домашнее животное'
    SOUNDS = {'кошка': 'Мяу!', 'собака': 'Гав!',
              'попугай': 'Кррр!', 'черепаха': 'Молчит'}

    def __init__(self, name, species, age, weight):
        self.name = name
        self.species = species
        self.age = age
        self.weight = weight

    def describe(self):
        return (f'{self.name} ({self.species}), {self.age} лет, '
                f'{self.weight} кг [{Pet.category}]')

    def is_adult(self):
        return self.age >= 2

    def sound(self):
        return Pet.SOUNDS.get(self.species, '...')

pets = [
    Pet('Барсик', 'кошка', 3, 4.5),
    Pet('Рекс', 'собака', 1, 12.0),
    Pet('Кеша', 'попугай', 5, 0.1),
    Pet('Тортилла', 'черепаха', 20, 2.3),
]

for p in pets:
    print(p.describe())
    print(f'  Взрослый: {p.is_adult()} | Звук: {p.sound()}')