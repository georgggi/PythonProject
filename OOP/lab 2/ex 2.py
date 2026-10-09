class StudentCard:
    def __init__(self, name, card_id, gpa):
        self.__name = name
        self.__card_id = card_id
        self.gpa = gpa

    @property
    def name(self):
        return self.__name

    @property
    def gpa(self):
        return self.__gpa

    @gpa.setter
    def gpa(self, value):
        if not 0.0 <= value <= 4.0:
            raise ValueError('GPA должен быть в диапазоне 0.0–4.0')
        self.__gpa = value

    @property
    def status(self):
        if self.__gpa >= 3.5:
            return 'Отличник'
        if self.__gpa >= 2.5:
            return 'Хорошист'
        if self.__gpa >= 1.0:
            return 'Удовлетворительно'
        return 'Отчислен'

    def __str__(self):
        return f'{self.name} (билет №{self.__card_id}): GPA {self.__gpa} — {self.status}'

students = [
    StudentCard('Асанов Эрлан', 1001, 3.9),
    StudentCard('Бекова Айжан', 1002, 3.2),
    StudentCard('Токтогулов Руслан', 1003, 2.1),
    StudentCard('Мамытова Алина', 1004, 1.4),
    StudentCard('Эсенов Тимур', 1005, 0.6),
]
for s in students:
    print(s)

avg = sum(s.gpa for s in students) / len(students)
excellent = sum(1 for s in students if s.status == 'Отличник')
print(f'\nСредний GPA: {avg:.2f}')
print(f'Количество отличников: {excellent}')