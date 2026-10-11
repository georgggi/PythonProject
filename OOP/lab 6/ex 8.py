from datetime import date

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

class MaintenanceRecord:
    def __init__(self, day, work, cost):
        if cost < 0:
            raise ValueError("Стоимость работ не может быть отрицательной")
        self.day, self.work, self.cost = day, work, cost

class Driver:
    def __init__(self, name, licence):
        self.name, self.licence = name, licence
        self.vehicles = []

    def __str__(self):
        return f"{self.name} ({self.licence})"

class Vehicle(Observable):
    TYPE, SERVICE_INTERVAL_KM, CAPACITY = "транспорт", 10_000, 0
    STATUSES = ("на маршруте", "в ремонте", "на стоянке", "списан")
    WEEK_HOURS = 40

    def __init__(self, plate, brand):
        super().__init__()
        self.plate, self.brand = plate, brand
        self._status = "на стоянке"
        self.mileage = 0
        self.route_hours = 0
        self._records = []
        self._drivers = []

    @property
    def status(self):
        return self._status

    @property
    def drivers(self):
        return list(self._drivers)

    def set_status(self, new_status):
        if new_status not in self.STATUSES:
            raise ValueError(f"Неизвестный статус: {new_status}")
        if self._status == "списан":
            raise ValueError(f"{self.plate} списан — статус менять нельзя")
        if new_status == self._status:
            return
        old, self._status = self._status, new_status
        self._notify("STATUS_CHANGED", {"vehicle": self, "old": old, "new": new_status})

    def assign_driver(self, driver):
        if driver not in self._drivers:
            self._drivers.append(driver)
            driver.vehicles.append(self)

    def drive(self, km, hours):
        if self._status != "на маршруте":
            raise ValueError(f"{self.plate}: ехать нельзя, статус «{self._status}»")
        if km <= 0 or hours <= 0:
            raise ValueError("Пробег и время должны быть положительными")
        self.mileage += km
        self.route_hours += hours

    def add_maintenance(self, day, work, cost):
        record = MaintenanceRecord(day, work, cost)
        self._records.append(record)
        return record

    @property
    def maintenance_cost(self):
        return sum(r.cost for r in self._records)

    def needs_service(self):
        return self.mileage >= self.SERVICE_INTERVAL_KM * (len(self._records) + 1)

    def __str__(self):
        return f"{self.TYPE:<10s}{self.plate:<15s}{self.brand:<10s}{self._status:<12s}{self.mileage:>7d} км"

class Bus(Vehicle):
    TYPE, SERVICE_INTERVAL_KM, CAPACITY = "автобус", 8_000, 50

class Minibus(Vehicle):
    TYPE, SERVICE_INTERVAL_KM, CAPACITY = "маршрутка", 10_000, 18

class Truck(Vehicle):
    TYPE, SERVICE_INTERVAL_KM, CAPACITY = "грузовик", 6_000, 10

class Car(Vehicle):
    TYPE, SERVICE_INTERVAL_KM, CAPACITY = "легковой", 15_000, 4

class VehicleFactory:
    _registry = {"автобус": Bus, "маршрутка": Minibus, "грузовик": Truck, "легковой": Car}

    @classmethod
    def create(cls, vtype, plate, brand):
        creator = cls._registry.get(vtype)
        if creator is None:
            raise ValueError(f"Неизвестный тип транспорта: {vtype}")
        return creator(plate, brand)

class Dispatcher:
    def update(self, event, data):
        v = data["vehicle"]
        print(f"    [Диспетчер] {v.plate} ({v.TYPE}): {data['old']} → {data['new']}")

class ServiceCenter:
    def __init__(self):
        self.in_service = []

    def update(self, event, data):
        v = data["vehicle"]
        if data["new"] == "в ремонте":
            self.in_service.append(v)
            print(f"    [Сервис] принят в ремонт {v.plate}")
        elif data["old"] == "в ремонте":
            self.in_service.remove(v)
            print(f"    [Сервис] {v.plate} выдан из ремонта -> {data['new']}")
        elif data["new"] == "списан":
            print(f"    [Сервис] {v.plate} списан, снять с обслуживания")

class FleetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.vehicles = []
            cls._instance.observers = []
        return cls._instance

    def add_observer(self, obs):
        self.observers.append(obs)

    def add_vehicle(self, vtype, plate, brand):
        if any(v.plate == plate for v in self.vehicles):
            raise ValueError(f"Транспорт {plate} уже в реестре")
        vehicle = VehicleFactory.create(vtype, plate, brand)
        for obs in self.observers:
            vehicle.subscribe(obs)
        self.vehicles.append(vehicle)
        return vehicle

    def get(self, plate):
        for v in self.vehicles:
            if v.plate == plate:
                return v
        raise ValueError(f"Транспорт {plate} не найден")

    def fleet_report(self):
        print("\n" + "=" * 66)
        print("ОТЧЁТ ПО ТРАНСПОРТНОМУ ПАРКУ")
        print("=" * 66)
        for v in self.vehicles:
            flag = "  ⚠ нужно ТО" if v.needs_service() and v.status != "списан" else ""
            print(f"{v}  ТО: {v.maintenance_cost:>6,.0f} сом{flag}")
        active = [v for v in self.vehicles if v.status != "списан"]
        total_cost = sum(v.maintenance_cost for v in self.vehicles)
        total_km = sum(v.mileage for v in self.vehicles)
        hours = sum(v.route_hours for v in active)
        planned = len(active) * Vehicle.WEEK_HOURS
        print("-" * 66)
        print(f"Всего единиц: {len(self.vehicles)}, активных: {len(active)}")
        by_status = {}
        for v in self.vehicles:
            by_status[v.status] = by_status.get(v.status, 0) + 1
        print("По статусам:", ", ".join(f"{k} — {n}" for k, n in by_status.items()))
        print(f"Расходы на обслуживание: {total_cost:,.0f} сом")
        print(f"Общий пробег: {total_km:,} км")
        if planned:
            print(f"КПД использования парка: {hours / planned * 100:.1f} % "
                  f"({hours} ч на маршруте из {planned} плановых)")
        if total_km:
            print(f"Средняя стоимость обслуживания: {total_cost / total_km:.2f} сом/км")

if __name__ == "__main__":
    fleet = FleetManager()
    fleet.add_observer(Dispatcher())
    service = ServiceCenter()
    fleet.add_observer(service)
    bus = fleet.add_vehicle("автобус", "01 KG 123 AB", "Higer")
    van = fleet.add_vehicle("маршрутка", "01 KG 777 MM", "Sprinter")
    truck = fleet.add_vehicle("грузовик", "01 KG 555 TT", "КАМАЗ")
    car = fleet.add_vehicle("легковой", "01 KG 001 CC", "Toyota")
    aidar, bakyt = Driver("Айдар", "B-1001"), Driver("Бакыт", "D-2002")
    bus.assign_driver(aidar)
    van.assign_driver(aidar)
    van.assign_driver(bakyt)
    truck.assign_driver(bakyt)
    print("Водители:")
    for d in (aidar, bakyt):
        print(f"  {d} -> {[v.plate for v in d.vehicles]}")
    print("\n--- Выезд на маршруты ---")
    for v in (bus, van, truck):
        v.set_status("на маршруте")
    bus.drive(8_200, 32)
    van.drive(5_400, 28)
    truck.drive(3_100, 20)
    print("\n--- Техническое обслуживание ---")
    print("Автобус (пробег 8200 км) нуждается в ТО:", bus.needs_service())
    bus.add_maintenance(date(2026, 5, 3), "Замена масла и колодок", 12_500)
    print("После ТО нуждается в ТО:", bus.needs_service())
    bus.set_status("в ремонте")
    bus.add_maintenance(date(2026, 5, 4), "Замена ремня ГРМ", 18_000)
    van.add_maintenance(date(2026, 4, 20), "Диагностика", 3_000)
    car.set_status("на маршруте")
    car.drive(2_000, 6)
    bus.set_status("на стоянке")
    print("\n--- Списание грузовика ---")
    truck.set_status("списан")
    print("\n--- Ошибки ---")
    for action in (lambda: truck.set_status("на маршруте"), lambda: bus.drive(100, 2),
                   lambda: fleet.add_vehicle("автобус", "01 KG 123 AB", "X"),
                   lambda: fleet.add_vehicle("трактор", "01 KG 000 XX", "X"),
                   lambda: fleet.get("НЕТ"), lambda: van.add_maintenance(date.today(), "X", -5),
                   lambda: van.set_status("летит")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    fleet.fleet_report()
    print("Один менеджер:", FleetManager() is FleetManager())