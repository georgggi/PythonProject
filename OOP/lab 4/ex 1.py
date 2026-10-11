from abc import ABC, abstractmethod

class Spacecraft(ABC):
    FUEL_COEF = 0.0

    def __init__(self, name, mass_kg):
        if mass_kg <= 0:
            raise ValueError("Масса аппарата должна быть положительной")
        self.name = name
        self.mass_kg = mass_kg

    @abstractmethod
    def launch(self) -> str:
        pass

    @abstractmethod
    def mission_description(self) -> str:
        pass

    @abstractmethod
    def fuel_consumption(self, distance_km) -> float:
        pass

    @staticmethod
    def _check_distance(distance_km):
        if distance_km < 0:
            raise ValueError("Расстояние не может быть отрицательным")

    def table_row(self, distance_km):
        kind = self.__class__.__name__
        fuel = self.fuel_consumption(distance_km)
        return f"{kind:<13s}| {self.name:<14s}| {self.mass_kg:>9,.0f} кг | {fuel:>9.2f} кг"

class Satellite(Spacecraft):
    FUEL_COEF = 2e-6
    PURPOSES = {
        "связь": "ретрансляция сигнала телевидения и интернета",
        "навигация": "определение координат (аналог GPS/ГЛОНАСС)",
        "наблюдение": "съёмка поверхности Земли",
        "метео": "мониторинг погоды и климата",
    }

    def __init__(self, name, mass_kg, orbit_km, period_min, purpose):
        super().__init__(name, mass_kg)
        if purpose not in self.PURPOSES:
            raise ValueError(f"Недопустимое назначение: {purpose}")
        self.orbit_km = orbit_km
        self.period_min = period_min
        self.purpose = purpose

    def launch(self):
        return (f"Спутник «{self.name}» выведен на орбиту {self.orbit_km} км "
                f"(период {self.period_min} мин)")

    def mission_description(self):
        return f"Назначение: {self.purpose} — {self.PURPOSES[self.purpose]}"

    def fuel_consumption(self, distance_km):
        self._check_distance(distance_km)
        return self.mass_kg * distance_km * self.FUEL_COEF

class SpaceStation(Spacecraft):
    FUEL_COEF = 5e-7

    def __init__(self, name, mass_kg, crew, modules, service_years, experiments):
        super().__init__(name, mass_kg)
        self.crew = crew
        self.modules = modules
        self.service_years = service_years
        self.experiments = list(experiments)

    def launch(self):
        return (f"Станция «{self.name}» собирается на орбите из "
                f"{self.modules} модулей")

    def mission_description(self):
        return (f"Экипаж {self.crew} чел., срок службы {self.service_years} лет, "
                f"экспериментов: {len(self.experiments)} "
                f"({', '.join(self.experiments)})")

    def fuel_consumption(self, distance_km):
        self._check_distance(distance_km)
        return self.mass_kg * distance_km * self.FUEL_COEF * (1 + 0.05 * self.crew)

class Rover(Spacecraft):
    FUEL_COEF = 1e-5

    def __init__(self, name, mass_kg, planet, speed_kmh, power_source, travelled_km=0):
        super().__init__(name, mass_kg)
        if power_source not in ("солнечный", "ядерный"):
            raise ValueError("Источник энергии: солнечный или ядерный")
        self.planet = planet
        self.speed_kmh = speed_kmh
        self.power_source = power_source
        self.travelled_km = travelled_km

    def launch(self):
        return f"Ровер «{self.name}» совершает посадку на планету {self.planet}"

    def mission_description(self):
        return (f"Исследование поверхности ({self.planet}), источник энергии: "
                f"{self.power_source}, пройдено {self.travelled_km} км")

    def fuel_consumption(self, distance_km):
        self._check_distance(distance_km)
        k = 0.2 if self.power_source == "солнечный" else 1.0
        return self.mass_kg * distance_km * self.FUEL_COEF * k

class Probe(Spacecraft):
    FUEL_COEF = 4e-6

    def __init__(self, name, mass_kg, target, distance_mln_km, active):
        super().__init__(name, mass_kg)
        if target not in ("планета", "комета", "астероид"):
            raise ValueError("Цель: планета, комета или астероид")
        self.target = target
        self.distance_mln_km = distance_mln_km
        self.active = active

    def launch(self):
        return (f"Зонд «{self.name}» стартует к цели ({self.target}), "
                f"расстояние {self.distance_mln_km} млн км")

    def mission_description(self):
        state = "активна" if self.active else "завершена"
        return f"Пролёт и изучение: {self.target}, миссия {state}"

    def fuel_consumption(self, distance_km):
        self._check_distance(distance_km)
        if not self.active:
            return 0.0
        return self.mass_kg * distance_km * self.FUEL_COEF

if __name__ == "__main__":
    fleet = [
        Satellite("Sputnik-K", 1500, 36000, 1436, "связь"),
        Satellite("MeteoSat", 800, 800, 101, "метео"),
        SpaceStation("МКС", 420000, 7, 16, 30, ["биология", "физика", "медицина"]),
        Rover("Perseverance", 1025, "Марс", 0.14, "ядерный", 28.5),
        Probe("Voyager-X", 720, "планета", 4500, True),
    ]

    print("=" * 58)
    print("ЗАПУСК И ЗАДАЧИ МИССИЙ (полиморфный обход)")
    print("=" * 58)
    for craft in fleet:
        print(craft.launch())
        print("  ", craft.mission_description())

    dist = 1000
    print(f"\nРасход топлива на {dist} км:")
    print("-" * 58)
    for craft in fleet:
        print(craft.table_row(dist))
    print("-" * 58)

    total = sum(c.fuel_consumption(dist) for c in fleet)
    top = max(fleet, key=lambda c: c.fuel_consumption(dist))
    economy = min(fleet, key=lambda c: c.fuel_consumption(dist))
    print(f"Суммарный расход флота: {total:.2f} кг")
    print(f"Самый затратный: {top.name} ({top.__class__.__name__})")
    print(f"Самый экономичный: {economy.name} ({economy.__class__.__name__})")
    print("\nСортировка по массе:")
    for craft in sorted(fleet, key= lambda c: c.mass_kg):
        print(f"  {craft.name:<14s} {craft.mass_kg:>9,.0f} кг")