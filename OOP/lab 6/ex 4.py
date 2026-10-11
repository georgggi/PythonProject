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

class Sensor(Observable, ABC):
    KIND, UNIT, LIMITS = "Датчик", "", (0, 100)

    def __init__(self, name, limits=None):
        super().__init__()
        self.name = name
        self.limits = limits or self.LIMITS
        self.value = None
        self.history = []

    def is_ok(self, value=None):
        v = self.value if value is None else value
        return v is not None and self.limits[0] <= v <= self.limits[1]

    def update_reading(self, value, time):
        if not isinstance(value, (int, float)):
            raise ValueError("Показание должно быть числом")
        self.value = value
        self.history.append((time, value))
        ok = self.is_ok()
        self._notify("READING", {"sensor": self, "value": value, "time": time, "ok": ok})
        if not ok:                                   # порог превышен
            self._notify("THRESHOLD_EXCEEDED",
                         {"sensor": self, "value": value, "time": time})

    def __str__(self):
        return f"{self.KIND} «{self.name}»"

class TemperatureSensor(Sensor):
    KIND, UNIT, LIMITS = "Температура", "°C", (-10, 35)

class HumiditySensor(Sensor):
    KIND, UNIT, LIMITS = "Влажность", "%", (30, 70)

class PressureSensor(Sensor):
    KIND, UNIT, LIMITS = "Давление", "гПа", (980, 1040)

class CO2Sensor(Sensor):
    KIND, UNIT, LIMITS = "CO2", "ppm", (0, 1000)

class NoiseSensor(Sensor):
    KIND, UNIT, LIMITS = "Шум", "дБ", (0, 70)

class SensorFactory:
    _registry = {"temperature": TemperatureSensor, "humidity": HumiditySensor,
                 "pressure": PressureSensor, "co2": CO2Sensor, "noise": NoiseSensor}

    @classmethod
    def create(cls, kind, name, limits=None):
        creator = cls._registry.get(kind)
        if creator is None:
            raise ValueError(f"Неизвестный тип датчика: {kind}")
        if limits is not None and limits[0] >= limits[1]:
            raise ValueError("Нижний порог должен быть меньше верхнего")
        return creator(name, limits)

class SensorHub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.sensors = []
            cls._instance._observers = []
        return cls._instance

    def add_observer(self, observer):
        self._observers.append(observer)
        for s in self.sensors:
            s.subscribe(observer)

    def register(self, sensor):
        self.sensors.append(sensor)
        for obs in self._observers:
            sensor.subscribe(obs)
        return sensor

    def summary(self):
        print(f"SensorHub: зарегистрировано датчиков — {len(self.sensors)}")
        for s in self.sensors:
            lo, hi = s.limits
            print(f"  {str(s):<32s} порог {lo}…{hi} {s.UNIT}")

class AlertService:
    def __init__(self):
        self.alerts = []

    def update(self, event, data):
        if event != "THRESHOLD_EXCEEDED":
            return
        s, v = data["sensor"], data["value"]
        lo, hi = s.limits
        excess = (lo - v) if v < lo else (v - hi)
        level = "КРИТИЧНО" if excess > 0.2 * (hi - lo) else "ВНИМАНИЕ"
        text = f"[{data['time']}] {level}: {s} = {v} {s.UNIT} (норма {lo}…{hi})"
        self.alerts.append(text)
        print(f"    [AlertService] {text}")

class Dashboard:
    def __init__(self, title):
        self.title = title
        self._sensors = []
        self._alert_log = []

    def add_sensor(self, sensor):
        if sensor not in self._sensors:
            self._sensors.append(sensor)
            sensor.subscribe(self)

    def update(self, event, data):
        if event == "THRESHOLD_EXCEEDED":
            self._alert_log.append((data["time"], str(data["sensor"]), data["value"]))

    def status_report(self):
        print(f"\n=== {self.title}: состояние датчиков ===")
        for s in self._sensors:
            if s.value is None:
                state = "нет данных"
            else:
                state = "НОРМА" if s.is_ok() else "ТРЕВОГА"
            val = "—" if s.value is None else f"{s.value} {s.UNIT}"
            print(f"  {str(s):<32s} {val:>12s}  {state}")
        bad = sum(1 for s in self._sensors if s.value is not None and not s.is_ok())
        print(f"  Датчиков в тревоге: {bad} из {len(self._sensors)}")

    def alert_history(self):
        print(f"\n=== {self.title}: история тревог ({len(self._alert_log)}) ===")
        for time, name, value in self._alert_log:
            print(f"  {time}  {name}  -> {value}")
        if not self._alert_log:
            print("  тревог не было")

if __name__ == "__main__":
    hub = SensorHub()
    alerts = AlertService()
    hub.add_observer(alerts)
    sensors = [hub.register(SensorFactory.create("temperature", "Серверная")),
               hub.register(SensorFactory.create("humidity", "Серверная")),
               hub.register(SensorFactory.create("pressure", "Склад")),
               hub.register(SensorFactory.create("co2", "Офис", limits=(0, 800))),
               hub.register(SensorFactory.create("noise", "Цех"))]
    hub.summary()
    board = Dashboard("Диспетчерская")
    for s in sensors:
        board.add_sensor(s)
    temp, hum, pres, co2, noise = sensors
    board.status_report()
    print("\n--- Поступают показания ---")
    readings = [(temp, 22, "09:00"), (hum, 45, "09:00"), (pres, 1013, "09:00"),
                (co2, 650, "09:00"), (noise, 55, "09:00"),
                (temp, 38, "10:00"), (co2, 950, "10:00"),
                (noise, 92, "11:00"), (hum, 25, "11:00"), (temp, 24, "12:00")]
    for sensor, value, time in readings:
        print(f"  {time} {sensor}: {value} {sensor.UNIT}")
        sensor.update_reading(value, time)
    board.status_report()
    board.alert_history()
    print(f"\nAlertService накопил: {len(alerts.alerts)} сообщений")
    print("История датчика «Температура/Серверная»:", temp.history)
    print("\n--- Отписка панели от шумового датчика ---")
    noise.unsubscribe(board)
    noise.update_reading(99, "13:00")
    print("Тревог на панели:", len(board._alert_log), "| в AlertService:", len(alerts.alerts))
    print("\n--- Ошибки ---")
    for action in (lambda: SensorFactory.create("radiation", "X"),
                   lambda: SensorFactory.create("noise", "X", limits=(80, 10)),
                   lambda: temp.update_reading("жарко", "14:00")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print("Один хаб:", SensorHub() is SensorHub())