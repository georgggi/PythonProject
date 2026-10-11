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

class Dish:
    CATEGORY = "блюдо"

    def __init__(self, name, price, prep_min):
        if price <= 0 or prep_min <= 0:
            raise ValueError("Цена и время приготовления должны быть > 0")
        self.name, self.price, self.prep_min = name, price, prep_min

    def __str__(self):
        return f"{self.name} ({self.CATEGORY}) — {self.price} сом, {self.prep_min} мин"

class Starter(Dish):
    CATEGORY = "закуска"

class Soup(Dish):
    CATEGORY = "суп"

class MainCourse(Dish):
    CATEGORY = "основное"

class Dessert(Dish):
    CATEGORY = "десерт"

class Drink(Dish):
    CATEGORY = "напиток"

class MenuFactory:
    _registry = {"закуска": Starter, "суп": Soup, "основное": MainCourse,
                 "десерт": Dessert, "напиток": Drink}

    @classmethod
    def create(cls, category, name, price, prep_min):
        creator = cls._registry.get(category)
        if creator is None:
            raise ValueError(f"Неизвестная категория: {category}")
        return creator(name, price, prep_min)

class Menu:
    def __init__(self):
        self._dishes = {}

    def add_dish(self, category, name, price, prep_min):
        dish = MenuFactory.create(category, name, price, prep_min)
        self._dishes[name] = dish
        return dish

    def get(self, name):
        if name not in self._dishes:
            raise ValueError(f"Блюда «{name}» нет в меню")
        return self._dishes[name]

    def show(self):
        print("МЕНЮ")
        for d in self._dishes.values():
            print("  ", d)

class OrderItem:
    def __init__(self, dish, qty):
        self.dish, self.qty = dish, qty

    @property
    def cost(self):
        return self.dish.price * self.qty

class Order(Observable):
    TRANSITIONS = {"принят": {"готовится", "отменён"},
                   "готовится": {"готов", "отменён"},
                   "готов": {"выдан"},
                   "выдан": set(),
                   "отменён": set()}

    def __init__(self, number, table):
        super().__init__()
        self.number, self.table = number, table
        self._items = []
        self._status = "принят"

    @property
    def status(self):
        return self._status

    def add_item(self, dish, qty=1):
        if self._status != "принят":
            raise ValueError("Состав заказа можно менять только до начала готовки")
        if qty <= 0:
            raise ValueError("Количество должно быть положительным")
        self._items.append(OrderItem(dish, qty))

    @property
    def total(self):
        return sum(i.cost for i in self._items)

    @property
    def prep_time(self):
        if not self._items:
            return 0
        return max(i.dish.prep_min for i in self._items) + len(self._items) - 1

    def change_status(self, new_status):
        if new_status not in self.TRANSITIONS:
            raise ValueError(f"Неизвестный статус: {new_status}")
        if new_status not in self.TRANSITIONS[self._status]:
            raise ValueError(f"Заказ №{self.number}: переход «{self._status}» → "
                             f"«{new_status}» невозможен")
        old, self._status = self._status, new_status
        self._notify("STATUS_CHANGED", {"order": self, "old": old, "new": new_status})

    def __str__(self):
        names = ", ".join(f"{i.dish.name}×{i.qty}" for i in self._items)
        return f"Заказ №{self.number} (стол {self.table}) [{self._status}]: {names} = {self.total} сом"

class Chef:
    def __init__(self, name):
        self.name = name

    def update(self, event, data):
        o, new = data["order"], data["new"]
        if new == "принят":
            print(f"    [Шеф {self.name}] новый заказ №{o.number}")
        elif new == "готовится":
            print(f"    [Шеф {self.name}] начал готовить №{o.number} (≈{o.prep_time} мин)")
        elif new == "отменён":
            print(f"    [Шеф {self.name}] заказ №{o.number} отменён — остановить готовку")

class Waiter:
    def __init__(self, name):
        self.name = name

    def update(self, event, data):
        o, new = data["order"], data["new"]
        if new == "готов":
            print(f"    [Официант {self.name}] заказ №{o.number} готов — забрать на стол {o.table}")
        elif new == "выдан":
            print(f"    [Официант {self.name}] заказ №{o.number} подан, счёт: {o.total} сом")
        elif new == "отменён":
            print(f"    [Официант {self.name}] сообщить столу {o.table} об отмене №{o.number}")

class Kitchen:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.orders = []
            cls._instance.staff = []
        return cls._instance

    def hire(self, person):
        self.staff.append(person)

    def accept(self, order):
        for person in self.staff:
            order.subscribe(person)
        self.orders.append(order)
        print(f"  Кухня приняла: {order}")

    def stats(self):
        served = [o for o in self.orders if o.status in ("готов", "выдан")]
        paid = [o for o in self.orders if o.status != "отменён"]
        cancelled = [o for o in self.orders if o.status == "отменён"]
        print("\nСТАТИСТИКА КУХНИ")
        print(f"  Всего заказов: {len(self.orders)}, отменено: {len(cancelled)}")
        if served:
            avg_time = sum(o.prep_time for o in served) / len(served)
            print(f"  Среднее время приготовления: {avg_time:.1f} мин")
        if paid:
            avg_check = sum(o.total for o in paid) / len(paid)
            print(f"  Средний чек: {avg_check:.0f} сом")
            print(f"  Выручка: {sum(o.total for o in paid)} сом")

if __name__ == "__main__":
    menu = Menu()
    menu.add_dish("закуска", "Салат Цезарь", 320, 10)
    menu.add_dish("суп", "Лагман", 280, 15)
    menu.add_dish("основное", "Плов", 350, 25)
    menu.add_dish("основное", "Стейк", 780, 30)
    menu.add_dish("десерт", "Чизкейк", 240, 5)
    menu.add_dish("напиток", "Компот", 90, 2)
    menu.show()
    kitchen = Kitchen()
    kitchen.hire(Chef("Бекзат"))
    kitchen.hire(Waiter("Айгуль"))
    print("\n--- Приём заказов ---")
    o1 = Order(1, 3)
    o1.add_item(menu.get("Салат Цезарь"))
    o1.add_item(menu.get("Плов"), 2)
    o1.add_item(menu.get("Компот"), 2)
    kitchen.accept(o1)
    o2 = Order(2, 5)
    o2.add_item(menu.get("Лагман"))
    o2.add_item(menu.get("Стейк"))
    o2.add_item(menu.get("Чизкейк"))
    kitchen.accept(o2)
    o3 = Order(3, 1)
    o3.add_item(menu.get("Стейк"), 2)
    kitchen.accept(o3)
    print("\n--- Жизненный цикл заказа №1 ---")
    for st in ("готовится", "готов", "выдан"):
        o1.change_status(st)
    print("\n--- Заказ №2 ---")
    o2.change_status("готовится")
    o2.change_status("готов")
    print("\n--- Заказ №3 отменён гостем ---")
    o3.change_status("готовится")
    o3.change_status("отменён")
    print("\n--- Ошибки ---")
    for action in (lambda: o1.change_status("готовится"), lambda: o2.add_item(menu.get("Плов")),
                   lambda: menu.get("Борщ"), lambda: o3.change_status("выдан"),
                   lambda: MenuFactory.create("салат", "X", 100, 5),
                   lambda: o2.change_status("в пути")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print()
    for o in kitchen.orders:
        print(o)
    kitchen.stats()
    print("Одна кухня:", Kitchen() is Kitchen())