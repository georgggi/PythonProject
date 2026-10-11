from abc import ABC, abstractmethod
from collections import defaultdict

class Insurance(ABC):
    ANNUAL_DISCOUNT = 0.05

    def __init__(self, client):
        self.client = client

    @abstractmethod
    def monthly_premium(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    def annual_premium(self) -> float:
        return self.monthly_premium() * 12 * (1 - self.ANNUAL_DISCOUNT)

    def row(self):
        kind = self.__class__.__name__
        return (f"{kind:<18s}| {self.client:<10s}| "
                f"{self.monthly_premium():>9,.0f} | {self.annual_premium():>10,.0f}")

class CarInsurance(Insurance):
    VEHICLE_K = {"легковой": 1.0, "грузовой": 1.3, "мотоцикл": 1.5}

    def __init__(self, client, car_value, driver_experience, vehicle_type, accidents_3y):
        super().__init__(client)
        if car_value <= 0:
            raise ValueError("Стоимость авто должна быть > 0")
        if vehicle_type not in self.VEHICLE_K:
            raise ValueError(f"Неизвестный тип ТС: {vehicle_type}")
        self.car_value = car_value
        self.driver_experience = driver_experience
        self.vehicle_type = vehicle_type
        self.accidents_3y = accidents_3y

    def description(self):
        return (f"КАСКО: {self.vehicle_type}, {self.car_value:,.0f} сом, "
                f"стаж {self.driver_experience} л., аварий: {self.accidents_3y}")

    def monthly_premium(self):
        exp_k = 1.5 if self.driver_experience < 3 else 1.1 if self.driver_experience < 10 else 0.9
        acc_k = 1 + 0.2 * self.accidents_3y
        return self.car_value * 0.03 / 12 * self.VEHICLE_K[self.vehicle_type] * exp_k * acc_k

class HealthInsurance(Insurance):
    BASE = {"базовая": 1500, "расширенная": 3000}
    REGION_K = {"Бишкек": 1.2, "Ош": 1.0}

    def __init__(self, client, age, chronic, region, program):
        super().__init__(client)
        if not 0 <= age <= 120:
            raise ValueError("Возраст: от 0 до 120")
        if program not in self.BASE:
            raise ValueError("Программа: базовая или расширенная")
        self.age = age
        self.chronic = chronic
        self.region = region
        self.program = program

    def description(self):
        ch = "есть хронические" if self.chronic else "нет хронических"
        return f"ДМС «{self.program}»: {self.age} лет, {ch}, регион {self.region}"

    def monthly_premium(self):
        age_k = 1.0 if self.age < 30 else 1.3 if self.age < 50 else 1.8
        chronic_k = 1.5 if self.chronic else 1.0
        region_k = self.REGION_K.get(self.region, 0.9)
        return self.BASE[self.program] * age_k * chronic_k * region_k

class TravelInsurance(Insurance):
    DAILY = 150
    COUNTRY_K = {"СНГ": 0.8, "Азия": 1.0, "Шенген": 1.5, "США": 2.5}

    def __init__(self, client, days, country, trip_type, sport):
        super().__init__(client)
        if days <= 0:
            raise ValueError("Число дней должно быть > 0")
        if country not in self.COUNTRY_K:
            raise ValueError(f"Неизвестная страна/регион: {country}")
        if trip_type not in ("турист", "бизнес"):
            raise ValueError("Тип: турист или бизнес")
        self.days = days
        self.country = country
        self.trip_type = trip_type
        self.sport = sport

    def description(self):
        sp = ", со спортом" if self.sport else ""
        return f"Путешествие: {self.country}, {self.days} дн., {self.trip_type}{sp}"

    def _daily_rate(self):
        k = self.COUNTRY_K[self.country]
        k *= 1.2 if self.trip_type == "бизнес" else 1.0
        k *= 1.6 if self.sport else 1.0
        return self.DAILY * k

    def trip_cost(self):
        return self._daily_rate() * self.days

    def monthly_premium(self):
        return self._daily_rate() * 30

    def annual_premium(self):
        return self._daily_rate() * 365 * 0.35

class PropertyInsurance(Insurance):
    RATE = {"квартира": 0.0015, "дом": 0.0025}

    def __init__(self, client, prop_type, value, area, floor):
        super().__init__(client)
        if prop_type not in self.RATE:
            raise ValueError("Тип: квартира или дом")
        if value <= 0 or area <= 0:
            raise ValueError("Стоимость и площадь должны быть > 0")
        self.prop_type = prop_type
        self.value = value
        self.area = area
        self.floor = floor

    def description(self):
        return f"Имущество: {self.prop_type}, {self.area} м², {self.floor} эт., {self.value:,.0f} сом"

    def monthly_premium(self):
        floor_k = 1.2 if self.prop_type == "квартира" and self.floor in (1, 9) else 1.0
        area_k = 1.1 if self.area > 100 else 1.0
        return self.value * self.RATE[self.prop_type] / 12 * floor_k * area_k

if __name__ == "__main__":
    portfolio = [
        CarInsurance("Айдар", 1_500_000, 2, "легковой", 1),
        CarInsurance("Бермет", 3_200_000, 12, "легковой", 0),
        HealthInsurance("Данияр", 27, False, "Бишкек", "базовая"),
        HealthInsurance("Эльвира", 55, True, "Ош", "расширенная"),
        TravelInsurance("Нурлан", 10, "Шенген", "турист", False),
        TravelInsurance("Салтанат", 7, "США", "бизнес", True),
        PropertyInsurance("Тимур", "квартира", 4_500_000, 65, 9),
        PropertyInsurance("Гульнара", "дом", 9_000_000, 140, 2),
    ]

    print("ОПИСАНИЕ ПОЛИСОВ")
    print("-" * 65)
    for p in portfolio:
        print(f"{p.client:<10s} {p.description()}")

    print("\nСТРАХОВЫЕ ВЗНОСЫ (сом)")
    print("-" * 54)
    print(f"{'Тип':<18s}| {'Клиент':<10s}| {'в месяц':>9s} | {'в год':>10s}")
    print("-" * 54)
    for p in portfolio:
        print(p.row())
    print("-" * 54)

    month_total = sum(p.monthly_premium() for p in portfolio)
    year_total = sum(p.annual_premium() for p in portfolio)
    print(f"Портфель: {month_total:,.0f} сом/мес, {year_total:,.0f} сом/год")

    by_type = defaultdict(float)
    for p in portfolio:
        by_type[p.__class__.__name__] += p.annual_premium()
    print("\nДоля видов страхования в годовых взносах:")
    for kind, s in sorted(by_type.items(), key= lambda kv: kv[1], reverse = True):
        print(f"  {kind:<18s}{s:>12,.0f} сом  ({s / year_total * 100:4.1f} %)")

    top = max(portfolio, key=lambda p: p.annual_premium())
    print(f"\nСамый дорогой полис: {top.client} — {top.annual_premium():,.0f} сом/год")
    trip = portfolio[4]
    print(f"Разовая поездка {trip.client}: {trip.trip_cost():,.0f} сом за {trip.days} дн.")