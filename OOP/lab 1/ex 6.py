class Student:
    institution = 'КГТУ им. И. Раззакова'

    def __init__(self, full_name, group, year, gpa):
        self.full_name = full_name
        self.group = group
        self.year = year
        self.gpa = gpa

    def introduce(self):
        return (f'{self.full_name}, гр. {self.group}, {self.year} курс, '
                f'{Student.institution}, GPA {self.gpa}')

    def academic_status(self):
        if self.gpa >= 3.5:
            return 'Отличник'
        if self.gpa >= 2.5:
            return 'Хорошист'
        if self.gpa >= 1.5:
            return 'Удовлетворительно'
        return 'Задолженность'

    def scholarship(self, base=3000):
        status = self.academic_status()
        if status == 'Отличник':
            return base * 1.5
        if status == 'Хорошист':
            return base
        return 0

students = [
    Student('Асанов Эрлан', 'ИТ-1-25', 1, 3.8),
    Student('Бекова Айжан', 'ИИ-2-24', 2, 2.9),
    Student('Токтогулов Руслан', 'ИТ-3-23', 3, 1.2),
]

for s in students:
    print(s.introduce())
    print(f'  Статус: {s.academic_status()} | Стипендия: {s.scholarship()} сом')