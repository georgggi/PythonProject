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