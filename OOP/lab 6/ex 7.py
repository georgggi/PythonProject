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

class Guest:
    def __init__(self, name, phone):
        self.name, self.phone = name, phone


class Booking:
    LONG_STAY_DAYS, LONG_STAY_DISCOUNT = 7, 0.10

    def __init__(self, guest, check_in, check_out, nightly_rate):
        if check_out <= check_in:
            raise ValueError("Дата выезда должна быть позже даты заезда")
        self.guest, self.check_in, self.check_out = guest, check_in, check_out
        self.nights = (check_out - check_in).days
        discount = self.LONG_STAY_DISCOUNT if self.nights >= self.LONG_STAY_DAYS else 0.0
        self.nightly_rate = nightly_rate * (1 - discount)
        self.cost = self.nightly_rate * self.nights

    def covers(self, day):
        return self.check_in <= day < self.check_out

class Room(Observable):
    TYPE, PRICE, CAPACITY = "номер", 3000, 2
    STATUSES = ("свободен", "занят", "убирается", "на ремонте")

    def __init__(self, number):
        super().__init__()
        self.number = number
        self._status = "свободен"
        self._bookings = []

    @property
    def status(self):
        return self._status

    def set_status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError(f"Неизвестный статус: {new_status}")
        if new_status == self._status:
            return
        old, self._status = self._status, new_status
        self._notify("STATUS_CHANGED", {"room": self, "old": old, "new": new_status})

    def book(self, guest, check_in, check_out):
        if self._status == "на ремонте":
            raise ValueError(f"Номер {self.number} на ремонте")
        new = Booking(guest, check_in, check_out, self.PRICE)
        for b in self._bookings:
            if check_in < b.check_out and b.check_in < check_out:
                raise ValueError(f"Номер {self.number} занят на эти даты ({b.guest.name})")
        self._bookings.append(new)
        return new

    def booking_on(self, day):
        return next((b for b in self._bookings if b.covers(day)), None)

    def __str__(self):
        return f"№{self.number} {self.TYPE} ({self.PRICE} сом/ночь, до {self.CAPACITY} чел.) [{self._status}]"

class StandardRoom(Room):
    TYPE, PRICE, CAPACITY = "стандарт", 3000, 2

class JuniorSuite(Room):
    TYPE, PRICE, CAPACITY = "полулюкс", 4500, 2

class Suite(Room):
    TYPE, PRICE, CAPACITY = "люкс", 7000, 3

class Apartment(Room):
    TYPE, PRICE, CAPACITY = "апартаменты", 10000, 5

class RoomFactory:
    _registry = {"стандарт": StandardRoom, "полулюкс": JuniorSuite,
                 "люкс": Suite, "апартаменты": Apartment}

    @classmethod
    def create(cls, room_type, number):
        creator = cls._registry.get(room_type)
        if creator is None:
            raise ValueError(f"Неизвестный тип номера: {room_type}")
        return creator(number)

class Reception:
    def update(self, event, data):
        r = data["room"]
        print(f"    [Ресепшн] номер {r.number}: {data['old']} → {data['new']}")

class HousekeepingService:
    def __init__(self):
        self.queue = []

    def update(self, event, data):
        r = data["room"]
        if data["new"] == "убирается":
            self.queue.append(r)
            print(f"    [Housekeeping] добавлена уборка номера {r.number}")
        elif data["new"] == "на ремонте":
            print(f"    [Housekeeping] номер {r.number} исключён из уборки (ремонт)")

    def clean_all(self):
        while self.queue:
            room = self.queue.pop(0)
            print(f"    [Housekeeping] убрано: номер {room.number}")
            room.set_status("свободен")

class HotelChain:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.hotels = []
        return cls._instance

    def register(self, hotel):
        self.hotels.append(hotel)

    def report(self, day):
        print(f"\n######## СЕТЬ ОТЕЛЕЙ, {day:%d.%m.%Y} ########")
        total = 0
        for h in self.hotels:
            total += h.daily_report(day)
        print(f"\nВыручка сети за день: {total:,.0f} сом")

class Hotel:
    def __init__(self, name, reception, housekeeping):
        self.name = name
        self.reception, self.housekeeping = reception, housekeeping
        self._rooms = {}
        HotelChain().register(self)

    def add_room(self, room_type, number):
        room = RoomFactory.create(room_type, number)
        room.subscribe(self.reception)
        room.subscribe(self.housekeeping)
        self._rooms[number] = room
        return room

    def room(self, number):
        if number not in self._rooms:
            raise ValueError(f"Номера {number} нет в отеле «{self.name}»")
        return self._rooms[number]

    def check_in(self, number, day):
        room = self.room(number)
        if room.booking_on(day) is None:
            raise ValueError(f"На {day:%d.%m} нет брони номера {number}")
        room.set_status("занят")

    def check_out(self, number):
        self.room(number).set_status("убирается")

    def daily_report(self, day):
        rooms = list(self._rooms.values())
        working = [r for r in rooms if r.status != "на ремонте"]
        occupied = [r for r in working if r.booking_on(day)]
        revenue = sum(r.booking_on(day).nightly_rate for r in occupied)
        load = len(occupied) / len(working) * 100 if working else 0
        print(f"\nОтель «{self.name}» — отчёт за {day:%d.%m.%Y}")
        print("-" * 58)
        for r in rooms:
            b = r.booking_on(day)
            who = f"{b.guest.name}, {b.nightly_rate:,.0f}/ночь" if b else "—"
            print(f"  {r.number:<4d}{r.TYPE:<12s}{r.status:<12s}{who}")
        print("-" * 58)
        print(f"  Номеров: {len(rooms)} (в ремонте {len(rooms) - len(working)}), "
              f"занято по броням: {len(occupied)}")
        print(f"  Загрузка: {load:.0f} %  | Выручка: {revenue:,.0f} сом")
        return revenue

if __name__ == "__main__":
    reception, housekeeping = Reception(), HousekeepingService()
    hotel = Hotel("Ала-Тоо", reception, housekeeping)
    for rtype, num in (("стандарт", 101), ("стандарт", 102), ("полулюкс", 201),
                       ("люкс", 301), ("апартаменты", 401)):
        hotel.add_room(rtype, num)
    aidar, bermet, nurlan = Guest("Айдар", "+996 555 100 200"), Guest("Бермет", "+996 700 300 400"), Guest("Нурлан", "+996 777 500 600")
    d = date(2026, 6, 10)
    print("--- Бронирование ---")
    b1 = hotel.room(101).book(aidar, d, d + timedelta(days=3))
    b2 = hotel.room(201).book(bermet, d - timedelta(days=1), d + timedelta(days=8))
    b3 = hotel.room(301).book(nurlan, d, d + timedelta(days=2))
    for num, b in ((101, b1), (201, b2), (301, b3)):
        print(f"  №{num}: {b.guest.name}, {b.nights} ноч., {b.cost:,.0f} сом "
              f"(ставка {b.nightly_rate:,.0f})")
    print("\n--- Заезд ---")
    for num in (101, 201, 301):
        hotel.check_in(num, d)
    print("\n--- Ремонт номера 102 ---")
    hotel.room(102).set_status("на ремонте")
    HotelChain().report(d)
    print("\n--- Через 2 дня: выезд гостя из №301 и уборка ---")
    hotel.check_out(301)
    housekeeping.clean_all()
    print("\n--- Ошибки ---")
    for action in (lambda: hotel.room(101).book(nurlan, d + timedelta(days=1), d + timedelta(days=4)),
                   lambda: hotel.room(102).book(nurlan, d, d + timedelta(days=1)),
                   lambda: hotel.room(401).book(nurlan, d, d),
                   lambda: hotel.room(999), lambda: hotel.check_in(401, d),
                   lambda: hotel.room(401).set_status("сломан"),
                   lambda: RoomFactory.create("президентский", 1)):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print("\n--- Ремонт закончен ---")
    hotel.room(102).set_status("свободен")
    HotelChain().report(d + timedelta(days=2))
    print("Одна сеть:", HotelChain() is HotelChain())