from datetime import date, timedelta

class Observable:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, sub):
        if sub not in self._subscribers:
            self._subscribers.append(sub)

    def unsubscribe(self, sub):
        if sub in self._subscribers:
            self._subscribers.remove(sub)

    def _notify(self, event, data):
        for sub in list(self._subscribers):
            sub.update(event, data)

class Book:
    GENRE = "общая"
    LOAN_DAYS = 21
    FINE_PER_DAY = 5   # сом

    def __init__(self, title, author):
        self.title, self.author = title, author
        self.available = True

    def __str__(self):
        mark = "в наличии" if self.available else "выдана"
        return f"«{self.title}» — {self.author} [{self.GENRE}, {mark}]"

class FictionBook(Book):
    GENRE, LOAN_DAYS, FINE_PER_DAY = "художественная", 21, 5

class ScienceBook(Book):
    GENRE, LOAN_DAYS, FINE_PER_DAY = "научная", 30, 8

class ChildrenBook(Book):
    GENRE, LOAN_DAYS, FINE_PER_DAY = "детская", 14, 3

class Textbook(Book):
    GENRE, LOAN_DAYS, FINE_PER_DAY = "учебник", 60, 10

class BookFactory:
    _registry = {"художественная": FictionBook, "научная": ScienceBook,
                 "детская": ChildrenBook, "учебник": Textbook}

    @classmethod
    def create(cls, genre, title, author):
        creator = cls._registry.get(genre)
        if creator is None:
            raise ValueError(f"Неизвестный жанр: {genre}")
        return creator(title, author)

class LibraryCatalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._books = []
        return cls._instance

    def add(self, book):
        self._books.append(book)

    def search(self, query):
        q = query.lower()
        return [b for b in self._books if q in b.title.lower() or q in b.author.lower()]

    def stats(self):
        total = len(self._books)
        free = sum(b.available for b in self._books)
        print(f"Каталог: всего книг {total}, в наличии {free}, на руках {total - free}")

class Reader:
    MAX_BOOKS = 3

    def __init__(self, name, ticket):
        self.name, self.ticket = name, ticket
        self.borrowed = []
        self.fines = 0

    def update(self, event, data):
        print(f"    [Читатель {self.name}] {data['text']}")

    def pay_fines(self):
        paid, self.fines = self.fines, 0
        return paid

class Librarian:
    def __init__(self, name):
        self.name = name
        self.journal = []

    def update(self, event, data):
        self.journal.append((event, data["text"]))
        print(f"    [Библиотекарь {self.name}] {event}: {data['text']}")

class Loan:
    def __init__(self, book, reader, issued):
        self.book, self.reader, self.issued = book, reader, issued
        self.due = issued + timedelta(days=book.LOAN_DAYS)

class Library(Observable):
    def __init__(self, name, librarian):
        super().__init__()
        self.name = name
        self.subscribe(librarian)
        self._books = []
        self._readers = []
        self._loans = []

    def add_book(self, genre, title, author):
        book = BookFactory.create(genre, title, author)
        self._books.append(book)
        LibraryCatalog().add(book)
        return book

    def register_reader(self, reader):
        if reader not in self._readers:
            self._readers.append(reader)

    def _notify_both(self, event, text, reader):
        data = {"text": text}
        self._notify(event, data)
        reader.update(event, data)

    def issue(self, title, reader, today):
        if reader not in self._readers:
            raise ValueError(f"{reader.name} не зарегистрирован в библиотеке")
        if reader.fines > 0:
            raise ValueError(f"У {reader.name} неоплаченный штраф {reader.fines} сом")
        if len(reader.borrowed) >= Reader.MAX_BOOKS:
            raise ValueError(f"{reader.name}: достигнут лимит {Reader.MAX_BOOKS} книги")
        book = next((b for b in self._books if b.title == title and b.available), None)
        if book is None:
            raise ValueError(f"Книга «{title}» недоступна")
        book.available = False
        loan = Loan(book, reader, today)
        self._loans.append(loan)
        reader.borrowed.append(book)
        self._notify_both("BOOK_ISSUED",
                          f"выдана «{title}», вернуть до {loan.due:%d.%m.%Y}", reader)
        return loan

    def return_book(self, title, reader, today):
        loan = next((l for l in self._loans
                     if l.book.title == title and l.reader is reader), None)
        if loan is None:
            raise ValueError(f"{reader.name} не брал «{title}»")
        days_late = max(0, (today - loan.due).days)
        fine = days_late * loan.book.FINE_PER_DAY
        loan.book.available = True
        reader.borrowed.remove(loan.book)
        self._loans.remove(loan)
        reader.fines += fine
        text = f"возвращена «{title}»"
        text += f", просрочка {days_late} дн., штраф {fine} сом" if fine else ", в срок"
        self._notify_both("BOOK_RETURNED", text, reader)
        return fine

    def report(self):
        print(f"\nБиблиотека «{self.name}»: книг {len(self._books)}, "
              f"читателей {len(self._readers)}, активных выдач {len(self._loans)}")
        for r in self._readers:
            titles = ", ".join(b.title for b in r.borrowed) or "—"
            print(f"  {r.name:<10s} билет {r.ticket} | на руках: {titles} | штраф: {r.fines} сом")

if __name__ == "__main__":
    aidar, bermet, nurlan = Reader("Айдар", "A-001"), Reader("Бермет", "A-002"), Reader("Нурлан", "A-003")
    outsider = Reader("Посторонний", "X-999")

    lib = Library("Центральная", Librarian("Гульнара"))
    for r in (aidar, bermet, nurlan):
        lib.register_reader(r)
    lib.add_book("художественная", "Белый пароход", "Ч. Айтматов")
    lib.add_book("художественная", "Джамиля", "Ч. Айтматов")
    lib.add_book("научная", "Краткая история времени", "С. Хокинг")
    lib.add_book("детская", "Маленький принц", "А. де Сент-Экзюпери")
    lib.add_book("учебник", "Python для начинающих", "М. Лутц")
    LibraryCatalog().stats()
    print("Поиск «Айтматов»:", [b.title for b in LibraryCatalog().search("айтматов")])
    d0 = date(2026, 3, 1)
    print("\n--- Выдача ---")
    lib.issue("Белый пароход", aidar, d0)
    lib.issue("Маленький принц", bermet, d0)
    lib.issue("Python для начинающих", nurlan, d0)
    print("\n--- Возврат ---")
    lib.return_book("Маленький принц", bermet, d0 + timedelta(days=10))      # в срок
    lib.return_book("Белый пароход", aidar, d0 + timedelta(days=30))         # 9 дней просрочки
    print("\n--- Ограничения ---")
    for action in (lambda: lib.issue("Джамиля", aidar, d0 + timedelta(days=31)),
                   lambda: lib.issue("Белый пароход", outsider, d0),
                   lambda: lib.issue("Python для начинающих", bermet, d0),
                   lambda: lib.return_book("Джамиля", bermet, d0),
                   lambda: BookFactory.create("комикс", "X", "Y")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print(f"\nАйдар оплатил штраф: {aidar.pay_fines()} сом")
    lib.issue("Джамиля", aidar, d0 + timedelta(days=32))
    lib.report()
    LibraryCatalog().stats()
    print("Один каталог:", LibraryCatalog() is LibraryCatalog())
