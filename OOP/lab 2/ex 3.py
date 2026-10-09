class MedCard:
    def __init__(self, patient, age, blood_group):
        self.__patient = patient
        self.__blood_group = blood_group
        self.__diagnoses = []
        self.age = age

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not 0 <= value <= 150:
            raise ValueError('Возраст должен быть в диапазоне 0–150')
        self.__age = value

    @property
    def is_adult(self):
        return self.__age >= 18

    def add_diagnosis(self, text):
        if text and text not in self.__diagnoses:
            self.__diagnoses.append(text)

    def remove_diagnosis(self, text):
        if text in self.__diagnoses:
            self.__diagnoses.remove(text)
            return True
        print(f'Диагноз «{text}» не найден')
        return False

    def summary(self):
        diag = ', '.join(self.__diagnoses) if self.__diagnoses else 'нет'
        adult = 'взрослый' if self.is_adult else 'ребёнок'
        return (f'Пациент: {self.__patient} | Возраст: {self.age} ({adult}) | '
                f'Группа крови: {self.__blood_group} | Диагнозы: {diag}')

c1 = MedCard('Иванов И.И.', 45, 'A(II)+')
c1.add_diagnosis('гипертония')
c1.add_diagnosis('гастрит')
c2 = MedCard('Сыдыкова Н.К.', 12, 'O(I)+')
c2.add_diagnosis('аллергический ринит')
c3 = MedCard('Орозов Б.А.', 70, 'B(III)-')

for c in (c1, c2, c3):
    print(c.summary())

print()
c1.remove_diagnosis('гастрит')
c1.remove_diagnosis('астма')
print(c1.summary())