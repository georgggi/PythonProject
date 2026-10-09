class Book:
    category = 'Печатное издание'

    def __init__(self, title, author, year, pages):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages

    def age(self):
        return 2026 - self.year

    def describe(self):
        return (f'«{self.title}», {self.author}, {self.year} г., '
                f'{self.pages} стр. [{Book.category}]')

    def is_long_read(self):
        return self.pages > 400

books = [
    Book('Война и мир', 'Л. Толстой', 1869, 1300),
    Book('Маленький принц', 'А. де Сент-Экзюпери', 1943, 96),
    Book('Манас', 'Народный эпос', 1995, 520),
]

for b in books:
    print(b.describe())
    print(f'  Возраст книги: {b.age()} лет')
    print(f'  Долгое чтение: {b.is_long_read()}')
    print()

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

class Movie:
    def __init__(self, title, director, year, genre, rating, duration):
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.rating = rating
        self.duration = duration

    def is_classic(self):
        return self.year < 2000

    def describe(self):
        return (f'«{self.title}» ({self.year}), реж. {self.director}, '
                f'{self.genre}, рейтинг {self.rating}')

    def duration_hours(self):
        h, m = divmod(self.duration, 60)
        return f'{h} ч {m} мин'

movies = [
    Movie('Крёстный отец', 'Ф. Коппола', 1972, 'драма', 9.2, 175),
    Movie('Один дома', 'К. Коламбус', 1990, 'комедия', 7.7, 103),
    Movie('Шрек', 'Э. Адамсон', 2001, 'анимация', 7.9, 90),
]

for m in movies:
    print(m.describe())
    print(f'  Классика: {m.is_classic()} | Длительность: {m.duration_hours()}')

class Planet:
    body_type = 'Небесное тело'

    def __init__(self, name, diameter_km, mass_earth, moons, has_atmosphere):
        self.name = name
        self.diameter_km = diameter_km
        self.mass_earth = mass_earth
        self.moons = moons
        self.has_atmosphere = has_atmosphere

    def describe(self):
        atm = 'есть' if self.has_atmosphere else 'нет'
        return (f'{self.name}: d={self.diameter_km} км, масса={self.mass_earth} M⊕, '
                f'спутников: {self.moons}, атмосфера: {atm}')

    def gravity(self, earth_g=9.8):
        return round(earth_g * self.mass_earth, 2)

    def is_giant(self):
        return self.diameter_km > 50000

planets = [
    Planet('Земля', 12742, 1.0, 1, True),
    Planet('Марс', 6779, 0.107, 2, True),
    Planet('Юпитер', 139820, 317.8, 95, True),
]

for p in planets:
    print(p.describe())
    print(f'  Гравитация: {p.gravity()} | Гигант: {p.is_giant()}')

biggest = max(planets, key=lambda p: p.diameter_km)
print(f'\nСамая большая планета: {biggest.name}')

class Student:
    institution = 'КГТУ им. И. Раззакова'

    def __init__(self, full_name, group, year, gpa):
        self.full_name = full_name
        self.group = group
        self.year = year
        self.gpa = gpa

    def introduce(self):
        return (f'{self.full_name}, гр. {self.group}, {self.year} курс, '
                f'{Student.institution}, GPA {self.gpa}')

    def academic_status(self):
        if self.gpa >= 3.5:
            return 'Отличник'
        if self.gpa >= 2.5:
            return 'Хорошист'
        if self.gpa >= 1.5:
            return 'Удовлетворительно'
        return 'Задолженность'

    def scholarship(self, base=3000):
        status = self.academic_status()
        if status == 'Отличник':
            return base * 1.5
        if status == 'Хорошист':
            return base
        return 0

students = [
    Student('Асанов Эрлан', 'ИТ-1-25', 1, 3.8),
    Student('Бекова Айжан', 'ИИ-2-24', 2, 2.9),
    Student('Токтогулов Руслан', 'ИТ-3-23', 3, 1.2),
]

for s in students:
    print(s.introduce())
    print(f'  Статус: {s.academic_status()} | Стипендия: {s.scholarship()} сом')

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

class WeatherStation:
    def __init__(self, name, city, altitude_m, temperature, humidity, wind_speed):
        self.name = name
        self.city = city
        self.altitude_m = altitude_m
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

    def describe(self):
        return (f'Станция «{self.name}» ({self.city}, {self.altitude_m} м): '
                f'{self.temperature}°C, влажность {self.humidity}%, '
                f'ветер {self.wind_speed} м/с')

    def feels_like(self):
        return round(self.temperature - self.wind_speed * 0.7)

    def weather_status(self):
        t = self.temperature
        if t > 30:
            return 'Жарко'
        if t > 15:
            return 'Тепло'
        if t > 5:
            return 'Прохладно'
        return 'Холодно'

    def is_comfortable(self):
        return 40 <= self.humidity <= 70 and 18 <= self.temperature <= 26

stations = [
    WeatherStation('Центр', 'Бишкек', 760, 32, 35, 2),
    WeatherStation('Озеро', 'Чолпон-Ата', 1650, 22, 55, 3),
    WeatherStation('Перевал', 'Тоо-Ашуу', 3200, 2, 80, 12),
]

for s in stations:
    print(s.describe())
    print(f'  Ощущается как: {s.feels_like()}°C | Погода: {s.weather_status()} | '
          f'Комфортно: {s.is_comfortable()}')