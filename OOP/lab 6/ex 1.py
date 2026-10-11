from abc import ABC

class Observable:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, sub):
        if sub not in self._subscribers:
            self._subscribers.append(sub)

    def unsubscribe(self, sub):
        if sub in self._subscribers:
            self._subscribers.remove(sub)

    def _notify(self, event, data):
        for sub in list(self._subscribers):
            sub.update(event, data)

class Owner:
    def __init__(self, name):
        self.name = name

    def update(self, event, data):
        print(f"    [Владелец {self.name}] {data['text']}")

class SecurityService:
    def __init__(self):
        self.alerts = []

    def update(self, event, data):
        dev, new = data["device"], data["new"]
        if isinstance(dev, SecurityLock) and new.get("locked") is False:
            self._alert(f"ЗАМОК «{dev.name}» ОТКРЫТ")
        elif isinstance(dev, Camera) and new.get("recording") is False:
            self._alert(f"КАМЕРА «{dev.name}» ОТКЛЮЧЕНА")

    def _alert(self, text):
        self.alerts.append(text)
        print(f"    [Охрана] ВНИМАНИЕ: {text}")

class Device(Observable, ABC):
    KIND = "Устройство"
    SCHEMA = {}
    DEFAULTS = {}

    def __init__(self, name, **state):
        super().__init__()
        self.name = name
        self._state = dict(self.DEFAULTS)
        for key, value in state.items():
            self._validate(key, value)
            self._state[key] = value

    def _validate(self, key, value):
        if key not in self.SCHEMA:
            raise ValueError(f"{self.KIND}: неизвестный параметр «{key}»")
        rule = self.SCHEMA[key]
        if not isinstance(value, rule[0]) or (rule[0] is int and isinstance(value, bool)):
            raise ValueError(f"{self.KIND}: «{key}» должен быть {rule[0].__name__}")
        if len(rule) == 3 and not rule[1] <= value <= rule[2]:
            raise ValueError(f"{self.KIND}: «{key}» вне диапазона {rule[1]}–{rule[2]}")

    @property
    def state(self):
        return dict(self._state)

    def set_state(self, **changes):
        old = self.state
        for key, value in changes.items():
            self._validate(key, value)
        self._state.update(changes)
        if self._state != old:
            text = f"{self.KIND} «{self.name}»: {old} -> {self._state}"
            self._notify("STATE_CHANGED",
                         {"device": self, "old": old, "new": self.state, "text": text})

    def __str__(self):
        return f"{self.KIND:<12s} {self.name:<14s} {self._state}"

class Lamp(Device):
    KIND = "Лампа"
    SCHEMA = {"on": (bool,), "brightness": (int, 0, 100)}
    DEFAULTS = {"on": False, "brightness": 0}

class Thermostat(Device):
    KIND = "Термостат"
    SCHEMA = {"target": (int, 5, 35), "mode": (str,)}
    DEFAULTS = {"target": 21, "mode": "heat"}

class SecurityLock(Device):
    KIND = "Замок"
    SCHEMA = {"locked": (bool,)}
    DEFAULTS = {"locked": True}

class Camera(Device):
    KIND = "Камера"
    SCHEMA = {"recording": (bool,), "motion_detection": (bool,)}
    DEFAULTS = {"recording": True, "motion_detection": True}

class DeviceFactory:
    _registry = {"lamp": Lamp, "thermostat": Thermostat,
                 "lock": SecurityLock, "camera": Camera}

    @classmethod
    def create(cls, kind, name, **state):
        creator = cls._registry.get(kind)
        if creator is None:
            raise ValueError(f"Неизвестный тип устройства: {kind}")
        return creator(name, **state)

class HomeController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = {}
        return cls._instance

    def register(self, home_name, device):
        self._registry[f"{home_name}/{device.name}"] = device

    def summary(self):
        print(f"Реестр контроллера: {len(self._registry)} устройств")
        kinds = {}
        for dev in self._registry.values():
            kinds[dev.KIND] = kinds.get(dev.KIND, 0) + 1
        for kind, n in kinds.items():
            print(f"  {kind:<12s} {n}")

class SmartHome:
    def __init__(self, name, owner, security):
        self.name = name
        self.owner = owner
        self.security = security
        self._devices = {}
        self._scenes = {}

    def add_device(self, kind, name, **state):
        if name in self._devices:
            raise ValueError(f"Устройство «{name}» уже есть")
        device = DeviceFactory.create(kind, name, **state)
        device.subscribe(self.owner)
        device.subscribe(self.security)
        self._devices[name] = device
        HomeController().register(self.name, device)
        return device

    def define_scene(self, scene_name, actions):
        for dev_name in actions:
            if dev_name not in self._devices:
                raise ValueError(f"В сцене «{scene_name}» нет устройства «{dev_name}»")
        self._scenes[scene_name] = actions

    def scene(self, scene_name):
        if scene_name not in self._scenes:
            raise ValueError(f"Сцена «{scene_name}» не определена")
        print(f"\n>>> Сцена «{scene_name}»")
        for dev_name, changes in self._scenes[scene_name].items():
            self._devices[dev_name].set_state(**changes)

    def report(self):
        print(f"\nДом «{self.name}»: устройств {len(self._devices)}")
        for dev in self._devices.values():
            print("  ", dev)


if __name__ == "__main__":
    owner = Owner("Айдар")
    security = SecurityService()
    home = SmartHome("Дом на Ала-Арче", owner, security)
    home.add_device("lamp", "Гостиная", on=True, brightness=80)
    home.add_device("lamp", "Спальня")
    home.add_device("thermostat", "Климат")
    home.add_device("lock", "Входная дверь")
    home.add_device("camera", "Двор")
    home.define_scene("Вечер", {"Гостиная": {"on": True, "brightness": 40},
                                "Климат": {"target": 23}})
    home.define_scene("Ночь", {"Гостиная": {"on": False, "brightness": 0},
                               "Спальня": {"on": True, "brightness": 10},
                               "Климат": {"target": 18},
                               "Входная дверь": {"locked": True}})
    home.define_scene("Уход из дома", {"Гостиная": {"on": False, "brightness": 0},
                                       "Спальня": {"on": False, "brightness": 0},
                                       "Климат": {"target": 15}})
    home.report()
    home.scene("Вечер")
    home.scene("Ночь")
    print("\n>>> Ручное управление")
    door = home._devices["Входная дверь"]
    door.set_state(locked=False)       # сработает охрана
    door.set_state(locked=False)       # без изменений — уведомления нет
    home._devices["Двор"].set_state(recording=False)
    home.scene("Уход из дома")
    print("\n>>> Отписка владельца от лампы «Спальня»")
    home._devices["Спальня"].unsubscribe(owner)
    home._devices["Спальня"].set_state(on=True, brightness=5)
    print("    (владелец уведомление не получил — он отписан)")
    print("\n>>> Проверка Singleton и ошибок")
    print("Один контроллер:", HomeController() is HomeController())
    for action in (lambda: home.add_device("fridge", "Холодильник"),
                   lambda: home._devices["Гостиная"].set_state(brightness=150),
                   lambda: home.scene("Праздник")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    home.report()
    print()
    HomeController().summary()
    print(f"Тревог от охраны: {len(security.alerts)}")