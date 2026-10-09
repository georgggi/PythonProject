class Instrument:
    def __init__(self, name, country, year, kind):
        self.name, self.country, self.year, self.kind = name, country, year, kind
        self.tuned = False

    def play(self):
        return f'{self.name} играет'

    def tune(self):
        self.tuned = True
        return f'{self.name} настроен'

    def describe(self):
        return f'{self.name} ({self.kind}, {self.country}, {self.year} г.)'

class StringInstrument(Instrument):
    def __init__(self, name, country, year, strings, body_material, play_type):
        super().__init__(name, country, year, 'струнный')
        self.strings, self.body_material, self.play_type = strings, body_material, play_type

    def play(self):
        way = 'смычком' if self.play_type == 'смычковый' else 'щипком'
        return f'{super().play()} {way}: звучит {self.strings} струн'

    def tune(self):
        super().tune()
        return f'{self.name}: натянуты и настроены {self.strings} струн'

    def describe(self):
        return f'{super().describe()} | дека: {self.body_material}, {self.play_type}'

class WindInstrument(Instrument):
    def __init__(self, name, country, year, note_range, material, wind_type):
        super().__init__(name, country, year, 'духовой')
        self.note_range, self.material, self.wind_type = note_range, material, wind_type

    def play(self):
        return f'{super().play()}: дуют в {self.wind_type} инструмент, диапазон {self.note_range}'

    def tune(self):
        super().tune()
        return f'{self.name}: подстроена длина трубки/язычка'

    def describe(self):
        return f'{super().describe()} | {self.material}, {self.wind_type}, {self.note_range}'

orchestra = [
    StringInstrument('Скрипка', 'Италия', 1550, 4, 'ель', 'смычковый'),
    StringInstrument('Гитара', 'Испания', 1700, 6, 'кедр', 'щипковый'),
    StringInstrument('Комуз', 'Кыргызстан', 1000, 3, 'абрикос', 'щипковый'),
    WindInstrument('Труба', 'Германия', 1500, 'E3–C6', 'металл', 'медный'),
    WindInstrument('Флейта', 'Франция', 1847, 'C4–C7', 'металл', 'деревянный'),
    WindInstrument('Кларнет', 'Германия', 1700, 'E3–C7', 'дерево', 'деревянный'),
]

print('=== Описание ===')
for i in orchestra:
    print(i.describe())
print('\n=== Настройка ===')
for i in orchestra:
    print(i.tune())
print('\n=== Концерт ===')
for i in orchestra:
    print(i.play())

print('\nВсе настроены:', all(i.tuned for i in orchestra))