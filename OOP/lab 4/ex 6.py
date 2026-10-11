from abc import ABC, abstractmethod

class GameCharacter(ABC):
    def __init__(self, name, hp):
        if hp <= 0:
            raise ValueError("HP должно быть положительным")
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.level = 1

    @abstractmethod
    def attack(self) -> int:
        pass

    @abstractmethod
    def defend(self, incoming_damage) -> int:
        pass

    @abstractmethod
    def level_up(self) -> None:
        pass

    def start_turn(self):
        pass

    @property
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, incoming_damage):
        real = self.defend(incoming_damage)
        self.hp = max(0, self.hp - real)
        return real

    def _grow(self, hp_bonus):
        self.level += 1
        self.max_hp += hp_bonus
        self.hp = min(self.max_hp, self.hp + hp_bonus)

    def status(self):
        kind = self.__class__.__name__
        return f"{kind:<8s}{self.name:<10s} ур.{self.level} HP {self.hp:>3d}/{self.max_hp}"

class Warrior(GameCharacter):
    WEAPONS = {"меч": 10, "топор": 14, "копьё": 8}

    def __init__(self, name, strength, armor, weapon, hp):
        super().__init__(name, hp)
        if weapon not in self.WEAPONS:
            raise ValueError("Оружие: меч, топор или копьё")
        self.strength, self.armor, self.weapon = strength, armor, weapon

    def attack(self):
        return int(self.strength * 1.2) + self.WEAPONS[self.weapon]

    def defend(self, incoming_damage):
        return max(1, incoming_damage - self.armor)

    def level_up(self):
        self.strength += 3
        self.armor += 1
        self._grow(15)

class Mage(GameCharacter):
    SCHOOLS = {"огонь": 8, "лёд": 5, "молния": 10}

    def __init__(self, name, magic, mana, school, hp):
        super().__init__(name, hp)
        if school not in self.SCHOOLS:
            raise ValueError("Школа: огонь, лёд или молния")
        self.magic, self.mana, self.school = magic, mana, school

    def start_turn(self):
        self.mana += 5

    def attack(self):
        if self.mana >= 10:
            self.mana -= 10
            return int(self.magic * 1.5) + self.SCHOOLS[self.school]
        return 4

    def defend(self, incoming_damage):
        if self.mana >= 5:
            self.mana -= 5
            return int(incoming_damage * 0.8)
        return incoming_damage

    def level_up(self):
        self.magic += 4
        self.mana += 15
        self._grow(8)

class Archer(GameCharacter):
    BOWS = {"короткий": 6, "длинный": 10, "арбалет": 14}

    def __init__(self, name, accuracy, arrows, bow, hp):
        super().__init__(name, hp)
        if bow not in self.BOWS:
            raise ValueError("Лук: короткий, длинный или арбалет")
        self.accuracy, self.arrows, self.bow = accuracy, arrows, bow
        self._hits_taken = 0

    def attack(self):
        if self.arrows > 0:
            self.arrows -= 1
            return int(self.accuracy * 1.3) + self.BOWS[self.bow]
        return 3

    def defend(self, incoming_damage):
        self._hits_taken += 1
        if self._hits_taken % 3 == 0:
            return 0
        return incoming_damage

    def level_up(self):
        self.accuracy += 3
        self.arrows += 6
        self._grow(10)

class Healer(GameCharacter):
    def __init__(self, name, healing, mana, defense, hp):
        super().__init__(name, hp)
        self.healing, self.mana, self.defense = healing, mana, defense

    def start_turn(self):
        self.mana += 3
        if self.hp < self.max_hp and self.mana >= 10:
            self.mana -= 10
            healed = min(self.healing, self.max_hp - self.hp)
            self.hp += healed
            print(f"      ✚ {self.name} лечит себя на {healed}")

    def attack(self):
        return 5 + self.level

    def defend(self, incoming_damage):
        return max(1, incoming_damage - self.defense)

    def level_up(self):
        self.healing += 4
        self.defense += 2
        self._grow(12)

def tournament(fighters, max_rounds=20):
    for rnd in range(1, max_rounds + 1):
        alive = [f for f in fighters if f.is_alive]
        if len(alive) == 1:
            return alive[0]
        print(f"\n--- Раунд {rnd} ---")
        for i, hero in enumerate(fighters):
            if not hero.is_alive:
                continue
            alive = [f for f in fighters if f.is_alive]
            if len(alive) == 1:
                return alive[0]
            hero.start_turn()
            j = (i + 1) % len(fighters)
            while not fighters[j].is_alive or fighters[j] is hero:
                j = (j + 1) % len(fighters)
            target = fighters[j]
            damage = hero.attack()
            real = target.take_damage(damage)
            print(f"  {hero.name} -> {target.name}: урон {damage}, прошло {real}, "
                  f"HP цели {target.hp}")
            if not target.is_alive:
                print(f"  ☠ {target.name} повержен! {hero.name} повышает уровень")
                hero.level_up()
        print("  Состояние:", " | ".join(f"{f.name} {f.hp}" for f in fighters))
    return max(fighters, key=lambda f: f.hp)

if __name__ == "__main__":
    fighters = [
        Warrior("Бирюк", strength=15, armor=8, weapon="меч", hp=120),
        Mage("Алмаз", magic=20, mana=50, school="огонь", hp=80),
        Archer("Ласка", accuracy=18, arrows=12, bow="длинный", hp=90),
        Healer("Айым", healing=15, mana=60, defense=5, hp=100),
    ]

    print("ПЕРСОНАЖИ:")
    for f in fighters:
        print(" ", f.status())

    print("\nДемонстрация level_up() (полиморфно):")
    for f in fighters:
        before = f.max_hp
        f.level_up()
        print(f"  {f.name}: ур. {f.level}, max HP {before} -> {f.max_hp}")

    winner = tournament(fighters)
    print("\n" + "=" * 50)
    print(f"ПОБЕДИТЕЛЬ: {winner.name} ({winner.__class__.__name__})")
    print("Итоговое состояние:")
    for f in fighters:
        print(" ", f.status(), "" if f.is_alive else "(выбыл)")