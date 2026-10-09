class WeatherStation:
    def __init__(self, name, city, altitude_m, temperature, humidity, wind_speed):
        self.name = name
        self.city = city
        self.altitude_m = altitude_m
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

    def describe(self):
        return (f'Станция «{self.name}» ({self.city}, {self.altitude_m} м): '
                f'{self.temperature}°C, влажность {self.humidity}%, '
                f'ветер {self.wind_speed} м/с')

    def feels_like(self):
        return round(self.temperature - self.wind_speed * 0.7)

    def weather_status(self):
        t = self.temperature
        if t > 30:
            return 'Жарко'
        if t > 15:
            return 'Тепло'
        if t > 5:
            return 'Прохладно'
        return 'Холодно'

    def is_comfortable(self):
        return 40 <= self.humidity <= 70 and 18 <= self.temperature <= 26

stations = [
    WeatherStation('Центр', 'Бишкек', 760, 32, 35, 2),
    WeatherStation('Озеро', 'Чолпон-Ата', 1650, 22, 55, 3),
    WeatherStation('Перевал', 'Тоо-Ашуу', 3200, 2, 80, 12),
]

for s in stations:
    print(s.describe())
    print(f'  Ощущается как: {s.feels_like()}°C | Погода: {s.weather_status()} | '
          f'Комфортно: {s.is_comfortable()}')