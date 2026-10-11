import math
from abc import ABC, abstractmethod

HOURS_PER_YEAR = 8760
HOUSEHOLD_KWH_YEAR = 3000

class EnergySource(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def generate(self, hours) -> float:
        pass

    @abstractmethod
    def efficiency(self) -> float:
        pass

    def annual_output(self) -> float:
        pass
        return self.generate(HOURS_PER_YEAR)

    @staticmethod
    def _check_hours(hours):
        if hours < 0:
            raise ValueError("Время не может быть отрицательным")

    def row(self):
        kind = self.__class__.__name__
        gwh = self.annual_output() / 1e6
        return f"{kind:<15s}| {self.name:<14s}| {self.efficiency():5.1f} % | {gwh:>9.2f} ГВт·ч"

class SolarPanel(EnergySource):
    CAPACITY_FACTOR = {"экватор": 0.25, "средние широты": 0.15, "север": 0.10}

    def __init__(self, name, area_m2, efficiency_pct, peak_kw, region):
        super().__init__(name)
        if region not in self.CAPACITY_FACTOR:
            raise ValueError("Регион: экватор, средние широты или север")
        self.area_m2, self._eff, self.peak_kw, self.region = area_m2, efficiency_pct, peak_kw, region

    def generate(self, hours):
        self._check_hours(hours)
        return self.peak_kw * hours * self.CAPACITY_FACTOR[self.region]

    def efficiency(self):
        return self._eff

class WindTurbine(EnergySource):
    AIR_DENSITY = 1.225
    CP = 0.40
    AVAILABILITY = 0.9

    def __init__(self, name, wind_speed, rotor_diameter, tower_height):
        super().__init__(name)
        self.wind_speed, self.rotor_diameter, self.tower_height = wind_speed, rotor_diameter, tower_height

    def power_kw(self):
        v = self.wind_speed * (self.tower_height / 10) ** 0.14
        if v < 3 or v > 25:
            return 0.0
        area = math.pi * (self.rotor_diameter / 2) ** 2
        return 0.5 * self.AIR_DENSITY * area * v ** 3 * self.CP / 1000

    def generate(self, hours):
        self._check_hours(hours)
        return self.power_kw() * hours * self.AVAILABILITY

    def efficiency(self):
        return self.CP * 100

class HydroPower(EnergySource):
    G = 9.81
    AVAILABILITY = 0.6

    def __init__(self, name, head_m, flow_m3s, efficiency):
        super().__init__(name)
        if not 0 < efficiency <= 1:
            raise ValueError("КПД задаётся долей от 0 до 1")
        self.head_m, self.flow_m3s, self._eff = head_m, flow_m3s, efficiency

    def power_kw(self):
        return 1000 * self.G * self.flow_m3s * self.head_m * self._eff / 1000

    def generate(self, hours):
        self._check_hours(hours)
        return self.power_kw() * hours * self.AVAILABILITY

    def efficiency(self):
        return self._eff * 100

class NuclearReactor(EnergySource):
    def __init__(self, name, power_mw, efficiency_pct, load_factor):
        super().__init__(name)
        if not 0 < load_factor <= 1:
            raise ValueError("Коэффициент загрузки: от 0 до 1")
        self.power_mw, self._eff, self.load_factor = power_mw, efficiency_pct, load_factor

    def generate(self, hours):
        self._check_hours(hours)
        return self.power_mw * 1000 * hours * self.load_factor

    def efficiency(self):
        return self._eff

if __name__ == "__main__":
    sources = [
        SolarPanel("СЭС Кара-Балта", 10_000, 20, 2_000, "средние широты"),
        SolarPanel("СЭС Сахара", 10_000, 20, 2_000, "экватор"),
        WindTurbine("ВЭС Ветряк-1", 9, 100, 90),
        HydroPower("ГЭС Токтогул", 60, 25, 0.9),
        NuclearReactor("АЭС Блок-1", 1_000, 33, 0.9),
    ]
    print("ВЫРАБОТКА ЗА 24 ЧАСА:")
    for s in sources:
        print(f"  {s.name:<14s} {s.generate(24):>12,.0f} кВт·ч")

    print("\nСРАВНЕНИЕ ЗА ГОД")
    print("-" * 58)
    for s in sources:
        print(s.row())
    print("-" * 58)

    total = sum(s.annual_output() for s in sources)
    best = max(sources, key=lambda s: s.annual_output())
    most_eff = max(sources, key=lambda s: s.efficiency())
    print(f"Суммарная выработка: {total / 1e6:,.2f} ГВт·ч")
    print(f"Больше всего энергии: {best.name} ({best.annual_output() / 1e6:,.2f} ГВт·ч)")
    print(f"Наивысший КПД: {most_eff.name} ({most_eff.efficiency():.1f} %)")

    print("\nРейтинг и обеспечение семей электричеством:")
    for rank, s in enumerate(sorted(sources, key=lambda s: s.annual_output(), reverse=True), 1):
        homes = s.annual_output() / HOUSEHOLD_KWH_YEAR
        print(f"  {rank}. {s.name:<14s} ≈ {homes:>9,.0f} семей")