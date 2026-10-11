from abc import ABC, abstractmethod

class Trip(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def duration_hours(self) -> float:
        pass

    @abstractmethod
    def co2_emission(self) -> float:
        pass

    def row(self):
        kind = self.__class__.__name__
        return (f"{kind:<10s}| {self.title:<32s}| {self.cost():>8,.0f} | "
                f"{self.duration_hours():>6.1f} | {self.co2_emission():>7.1f}")

class TaxiTrip(Trip):
    TIER_K = {"эконом": 1.0, "комфорт": 1.3, "бизнес": 1.8}

    def __init__(self, km, price_per_km, tier, rush_hour):
        super().__init__(f"Такси {tier}" + (", час пик" if rush_hour else ""))
        if km <= 0 or price_per_km <= 0:
            raise ValueError("Расстояние и цена за км должны быть > 0")
        if tier not in self.TIER_K:
            raise ValueError("Тип: эконом, комфорт или бизнес")
        self.km, self.price_per_km, self.tier, self.rush_hour = km, price_per_km, tier, rush_hour

    def cost(self):
        return self.km * self.price_per_km * self.TIER_K[self.tier] * (1.3 if self.rush_hour else 1.0)

    def duration_hours(self):
        return self.km / 85 + (1.5 if self.rush_hour else 0)

    def co2_emission(self):
        return self.km * 0.17

class BusTrip(Trip):
    def __init__(self, route, ticket_price, transfers, length_km):
        super().__init__(f"Автобус {route}")
        if length_km <= 0 or ticket_price < 0 or transfers < 0:
            raise ValueError("Некорректные параметры автобуса")
        self.ticket_price, self.transfers, self.length_km = ticket_price, transfers, length_km

    def cost(self):
        return self.ticket_price * (1 + self.transfers)

    def duration_hours(self):
        return self.length_km / 60 + self.transfers * 1.0

    def co2_emission(self):
        return self.length_km * 0.03

class AirTrip(Trip):
    CLASS_K = {"эконом": 1.0, "бизнес": 2.5, "первый": 4.0}

    def __init__(self, distance_km, travel_class, extra_baggage_kg):
        super().__init__(f"Самолёт {travel_class}")
        if distance_km <= 0 or extra_baggage_kg < 0:
            raise ValueError("Некорректные параметры перелёта")
        if travel_class not in self.CLASS_K:
            raise ValueError("Класс: эконом, бизнес или первый")
        self.distance_km, self.travel_class, self.extra_baggage_kg = distance_km, travel_class, extra_baggage_kg

    def cost(self):
        return self.distance_km * 8 * self.CLASS_K[self.travel_class] + self.extra_baggage_kg * 150

    def duration_hours(self):
        return self.distance_km / 800 + 3.0

    def co2_emission(self):
        return self.distance_km * 0.15 * (1.0 if self.travel_class == "эконом" else 1.5)

class TrainTrip(Trip):
    CAR_K = {"плацкарт": 1.0, "купе": 1.6, "СВ": 2.8}

    def __init__(self, distance_km, car_class, speed_kmh):
        super().__init__(f"Поезд {car_class}")
        if distance_km <= 0 or speed_kmh <= 0:
            raise ValueError("Расстояние и скорость должны быть > 0")
        if car_class not in self.CAR_K:
            raise ValueError("Вагон: плацкарт, купе или СВ")
        self.distance_km, self.car_class, self.speed_kmh = distance_km, car_class, speed_kmh

    def cost(self):
        return self.distance_km * 2.5 * self.CAR_K[self.car_class]

    def duration_hours(self):
        return self.distance_km / self.speed_kmh

    def co2_emission(self):
        return self.distance_km * 0.03

def score(trip, trips, w_cost=0.4, w_time=0.3, w_co2=0.3):
    best_cost = min(t.cost() for t in trips)
    best_time = min(t.duration_hours() for t in trips)
    best_co2 = min(t.co2_emission() for t in trips)
    return (w_cost * trip.cost() / best_cost
            + w_time * trip.duration_hours() / best_time
            + w_co2 * trip.co2_emission() / best_co2)


if __name__ == "__main__":
    trips = [
        TaxiTrip(1200, 15, "эконом", False),
        TaxiTrip(1200, 15, "комфорт", True),
        BusTrip("Алматы–Астана", 9_000, 0, 1250),
        BusTrip("Алматы–Караганда–Астана", 8_000, 1, 1300),
        AirTrip(1000, "эконом", 10),
        AirTrip(1000, "бизнес", 0),
        TrainTrip(1200, "плацкарт", 80),
        TrainTrip(1200, "купе", 80),
    ]

    print("МАРШРУТ: Алматы — Астана")
    print("-" * 73)
    print(f"{'Тип':<10s}| {'Вариант':<32s}| {'Цена':>8s} | {'Часы':>6s} | {'CO2, кг':>7s}")
    print("-" * 73)
    for t in trips:
        print(t.row())
    print("-" * 73)

    cheapest = min(trips, key=lambda t: t.cost())
    fastest = min(trips, key=lambda t: t.duration_hours())
    greenest = min(trips, key=lambda t: t.co2_emission())
    print(f"Самый дешёвый:     {cheapest.title} ({cheapest.cost():,.0f} сом)")
    print(f"Самый быстрый:     {fastest.title} ({fastest.duration_hours():.1f} ч)")
    print(f"Самый экологичный: {greenest.title} ({greenest.co2_emission():.1f} кг CO2)")

    print("\nКомплексный рейтинг (цена 40 %, время 30 %, CO2 30 %; меньше — лучше):")
    ranked = sorted(trips, key=lambda t: score(t, trips))
    for place, t in enumerate(ranked, 1):
        print(f"  {place}. {t.title:<32s} балл {score(t, trips):.2f}")
    print(f"\nОПТИМАЛЬНЫЙ МАРШРУТ: {ranked[0].title}")