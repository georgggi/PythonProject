class Planet:
    body_type = 'Небесное тело'

    def __init__(self, name, diameter_km, mass_earth, moons, has_atmosphere):
        self.name = name
        self.diameter_km = diameter_km
        self.mass_earth = mass_earth
        self.moons = moons
        self.has_atmosphere = has_atmosphere

    def describe(self):
        atm = 'есть' if self.has_atmosphere else 'нет'
        return (f'{self.name}: d={self.diameter_km} км, масса={self.mass_earth} M⊕, '
                f'спутников: {self.moons}, атмосфера: {atm}')

    def gravity(self, earth_g=9.8):
        return round(earth_g * self.mass_earth, 2)

    def is_giant(self):
        return self.diameter_km > 50000

planets = [
    Planet('Земля', 12742, 1.0, 1, True),
    Planet('Марс', 6779, 0.107, 2, True),
    Planet('Юпитер', 139820, 317.8, 95, True),
]

for p in planets:
    print(p.describe())
    print(f'  Гравитация: {p.gravity()} | Гигант: {p.is_giant()}')

biggest = max(planets, key=lambda p: p.diameter_km)
print(f'\nСамая большая планета: {biggest.name}')