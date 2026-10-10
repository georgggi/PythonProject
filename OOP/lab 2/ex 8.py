class HealthMetrics:
    def __init__(self, name, height_cm, weight_kg, age, sex=None):
        self.__name = name
        self.__age = age
        self.__sex = sex
        self.__height = height_cm
        self.__weight = weight_kg

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if not 50 <= value <= 250:
            raise ValueError('Рост должен быть в диапазоне 50–250 см')
        self.__height = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if not 2 <= value <= 500:
            raise ValueError('Вес должен быть в диапазоне 2–500 кг')
        self.__weight = value

    def bmi(self):
        h = self.__height / 100
        return round(self.__weight / h ** 2, 1)

    def bmi_status(self):
        b = self.bmi()
        if b < 18.5:
            return 'Недовес'
        if b < 25:
            return 'Норма'
        if b < 30:
            return 'Избыточный вес'
        if b < 40:
            return 'Ожирение'
        return 'Морбидное ожирение'

    def daily_calories(self, activity=1.2):
        w, h, a = self.weight, self.height, self.__age
        if self.__sex == 'м':
            bmr = 88.362 + 13.397 * w + 4.799 * h - 5.677 * a
        else:
            bmr = 447.593 + 9.247 * w + 3.098 * h - 4.330 * a
        return round(bmr * activity)

    def __str__(self):
        return (f'{self.__name:8s} | ИМТ {self.bmi():5} | {self.bmi_status():18s} | '
                f'{self.daily_calories()} ккал/сут')

patients = [
    HealthMetrics('Айдар', 178, 52, 25, 'м'),
    HealthMetrics('Айгуль', 165, 58, 30, 'ж'),
    HealthMetrics('Бекзод', 175, 88, 40, 'м'),
    HealthMetrics('Нургуль', 160, 110, 45, 'ж'),
]
for p in patients:
    print(p)