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