class Athlete:
    def __init__(self, name, age, country):
        self.name, self.age, self.country = name, age, country
        self.medals = []

    def add_medal(self, medal, year):
        if medal not in ('золото', 'серебро', 'бронза'):
            raise ValueError('Медаль: золото/серебро/бронза')
        self.medals.append((medal, year))

    def medals_count(self):
        return len(self.medals)

    def avg_speed(self):
        return 0.0

    def achievement(self):
        return f'{self.name} ({self.country}, {self.age} л.), медалей: {self.medals_count()}'

class Swimmer(Athlete):
    def __init__(self, name, age, country, specialty, record_100, style):
        super().__init__(name, age, country)
        self.specialty, self.record_100, self.style = specialty, record_100, style

    def avg_speed(self):
        return 100 / self.record_100

    def achievement(self):
        return (f'[Пловец] {super().achievement()} | {self.style}, '
                f'рекорд 100м: {self.record_100} с, v={self.avg_speed():.2f} м/с')

class Sprinter(Athlete):
    def __init__(self, name, age, country, distance, record, starts):
        super().__init__(name, age, country)
        self.distance, self.record, self.starts = distance, record, starts

    def avg_speed(self):
        return self.distance / self.record

    def achievement(self):
        return (f'[Спринтер] {super().achievement()} | {self.distance} м за '
                f'{self.record} с, стартов: {self.starts}, v={self.avg_speed():.2f} м/с')

s1 = Swimmer('Аскар', 22, 'Кыргызстан', 'кроль', 52.5, 'вольный')
s2 = Swimmer('Лена', 20, 'Россия', 'баттерфляй', 58.0, 'баттерфляй')
r1 = Sprinter('Усейн', 29, 'Ямайка', 100, 9.8, 40)
r2 = Sprinter('Тимур', 24, 'Казахстан', 200, 20.9, 25)

s1.add_medal('золото', 2024); s1.add_medal('бронза', 2025)
s2.add_medal('серебро', 2025)
r1.add_medal('золото', 2023); r1.add_medal('золото', 2024); r1.add_medal('серебро', 2025)

athletes = [s1, s2, r1, r2]
for a in athletes:
    print(a.achievement())

fastest = max(athletes, key=lambda a: a.avg_speed())
most = max(athletes, key=lambda a: a.medals_count())
print(f'\nСамый быстрый: {fastest.name} ({fastest.avg_speed():.2f} м/с)')
print(f'Больше всех медалей: {most.name} ({most.medals_count()})')