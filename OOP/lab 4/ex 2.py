from abc import ABC, abstractmethod
from collections import defaultdict

class MedicalWorker(ABC):
    def __init__(self, name, department):
        self.name = name
        self.department = department

    @abstractmethod
    def treat(self, patient) -> str:
        pass

    @abstractmethod
    def prescribe(self) -> str:
        pass

    @abstractmethod
    def calculate_workload(self) -> float:
        pass

    def workload_level(self):
        w = self.calculate_workload()
        if w < 70:
            return "низкая"
        if w <= 100:
            return "нормальная"
        return "ПЕРЕГРУЗКА"

    def row(self):
        kind = self.__class__.__name__
        return (f"{kind:<11s}| {self.name:<12s}| {self.department:<16s}| "
                f"{self.calculate_workload():6.1f} % | {self.workload_level()}")

class Therapist(MedicalWorker):
    NORM_PER_DAY = 20

    def __init__(self, name, department, specialization, appointments_per_day, experience):
        super().__init__(name, department)
        self.specialization = specialization
        self.appointments_per_day = appointments_per_day
        self.experience = experience

    def treat(self, patient):
        return f"Терапевт {self.name} осматривает пациента {patient} ({self.specialization})"

    def prescribe(self):
        return "Назначает: анализы, ЭКГ, курс лекарственной терапии"

    def calculate_workload(self):
        k = 0.9 if self.experience >= 10 else 1.0
        return self.appointments_per_day / self.NORM_PER_DAY * 100 * k

class Surgeon(MedicalWorker):
    NORM_PER_MONTH = 16

    def __init__(self, name, department, specialization, operations_per_month, category):
        super().__init__(name, department)
        if category not in ("первая", "высшая"):
            raise ValueError("Категория: первая или высшая")
        self.specialization = specialization
        self.operations_per_month = operations_per_month
        self.category = category

    def treat(self, patient):
        return f"Хирург {self.name} проводит операцию пациенту {patient}"

    def prescribe(self):
        return "Назначает: предоперационную подготовку, послеоперационный режим"

    def calculate_workload(self):
        return self.operations_per_month / self.NORM_PER_MONTH * 100

class Nurse(MedicalWorker):
    NORMS = {"дневная": 12, "ночная": 18, "суточная": 24}

    def __init__(self, name, department, ward, shift, patients):
        super().__init__(name, department)
        if shift not in self.NORMS:
            raise ValueError("Смена: дневная, ночная или суточная")
        self.ward = ward
        self.shift = shift
        self.patients = patients

    def treat(self, patient):
        return f"Медсестра {self.name} ставит капельницу пациенту {patient} ({self.ward})"

    def prescribe(self):
        return "Права назначения нет — выполняет назначения врача"

    def calculate_workload(self):
        return self.patients / self.NORMS[self.shift] * 100

class Pharmacist(MedicalWorker):
    BASE = {"дневная": 50, "ночная": 40, "суточная": 80}

    def __init__(self, name, pharmacy, shift, controlled_drugs):
        super().__init__(name, pharmacy)
        if shift not in self.BASE:
            raise ValueError("Смена: дневная, ночная или суточная")
        self.shift = shift
        self.controlled_drugs = list(controlled_drugs)

    def treat(self, patient):
        return f"Фармацевт {self.name} консультирует {patient} по приёму препаратов"

    def prescribe(self):
        return (f"Отпускает по рецепту; контролируемых препаратов: "
                f"{len(self.controlled_drugs)}")

    def calculate_workload(self):
        return self.BASE[self.shift] + 4 * len(self.controlled_drugs)

if __name__ == "__main__":
    staff = [
        Therapist("Иванова А.", "Терапия", "кардиология", 22, 12),
        Therapist("Сыдыков Б.", "Терапия", "общая практика", 26, 4),
        Surgeon("Омуров Т.", "Хирургия", "травматология", 14, "высшая"),
        Surgeon("Ким Д.", "Хирургия", "общая хирургия", 20, "первая"),
        Nurse("Асанова Г.", "Терапия", "палата 3", "дневная", 10),
        Nurse("Петрова Н.", "Хирургия", "реанимация", "суточная", 28),
        Pharmacist("Жумабаев К.", "Аптека №1", "дневная", ["морфин", "кодеин", "трамадол"]),
    ]

    print("ПОЛИМОРФНЫЙ ОБХОД: лечение и назначения")
    print("-" * 69)
    for w in staff:
        print(w.treat("Алиев Р."))
        print("   ", w.prescribe())

    print("\nНАГРУЗКА ПЕРСОНАЛА")
    print("-" * 66)
    for w in staff:
        print(w.row())

    avg = sum(w.calculate_workload() for w in staff) / len(staff)
    print("-" * 66)
    print(f"Средняя нагрузка на персонал: {avg:.1f} %")

    print("\nСВОДКА ПО ОТДЕЛЕНИЯМ")
    print("-" * 60)
    by_dept = defaultdict(list)
    for w in staff:
        by_dept[w.department].append(w)
    for dept, workers in by_dept.items():
        d_avg = sum(x.calculate_workload() for x in workers) / len(workers)
        overloaded = [x.name for x in workers if x.calculate_workload() > 100]
        print(f"{dept:<16s} сотрудников: {len(workers)} | средняя нагрузка: {d_avg:6.1f} %")
        if overloaded:
            print(f"   перегружены: {', '.join(overloaded)}")