class Employee:
    total_employees = 0  # счётчик всех сотрудников

    def __init__(self, name, position, base_salary, experience):
        if base_salary <= 0:
            raise ValueError('Зарплата должна быть больше нуля')
        if experience < 0:
            raise ValueError('Стаж не может быть отрицательным')
        self.name = name
        self.position = position
        self.base_salary = base_salary
        self.experience = experience
        Employee.total_employees += 1

    def salary(self):
        return self.base_salary

    def introduce(self):
        return (f'{self.name}, {self.position}, '
                f'стаж {self.experience} лет, '
                f'зарплата {self.salary():.0f} сом')

    def __str__(self):
        return f'{self.name}({self.name})'


class Manager(Employee):
    """Менеджер: зарплата + % бонуса."""

    def __init__(self, name, position, base_salary, experience,
                 department, subordinates, bonus_percent):
        super().__init__(name, position, base_salary, experience)
        self.department = department
        self.subordinates = subordinates
        self.bonus_percent = bonus_percent

    def salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)

    def introduce(self):
        base = super().introduce()
        return (f'[Менеджер] {base} | отдел: {self.department}, '
                f'подчинённых: {self.subordinates}, '
                f'бонус: {self.bonus_percent}%')

class Developer(Employee):
    """Разработчик: надбавка зависит от уровня."""
    LEVELS = {'junior': 0, 'middle': 30, 'senior': 60}  # надбавка, %

    def __init__(self, name, position, base_salary, experience,
                 language, level):
        super().__init__(name, position, base_salary, experience)
        if level not in self.LEVELS:
            raise ValueError(f'Недопустимый уровень: {level}')
        self.language = language
        self.level = level

    def salary(self):
        return self.base_salary * (1 + self.LEVELS[self.level] / 100)

    def introduce(self):
        base = super().introduce()
        return (f'[Разработчик] {base} | язык: {self.language}, '
                f'уровень: {self.level}')

team = [
    Employee('Нурлан', 'Бухгалтер', 40000, 5),
    Manager('Алия', 'Руководитель отдела', 60000, 8,
            'Разработка', 10, 20),
    Manager('Берик', 'Менеджер проектов', 55000, 6,
            'Продажи', 5, 15),
    Developer('Данияр', 'Разработчик', 50000, 1, 'Python', 'junior'),
    Developer('Мээрим', 'Разработчик', 55000, 4, 'JavaScript', 'middle'),
    Developer('Айгуль', 'Разработчик', 50000, 7, 'Java', 'senior'),
]

print(f'Всего сотрудников: {Employee.total_employees}\n')
for emp in team:
    print(emp.introduce())

payroll = sum(emp.salary() for emp in team)
print(f'\nЗарплатный фонд: {payroll:.0f} сом')

top = max(team, key=lambda e: e.salary())
print(f'Самая высокая зарплата: {top.name} — {top.salary():.0f} сом')

print(isinstance(team[1], Employee))       # True
print(issubclass(Developer, Employee))     # True
print(isinstance(team[3], Manager))        # False