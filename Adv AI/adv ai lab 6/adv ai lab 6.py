import ast
import json
import math
import operator
import os
import re
import secrets
import string
import tempfile
from pathlib import Path
from urllib.parse import urlparse

DATA_FILE = Path(__file__).resolve().parent / "agent_data.json"

def calculate(expression):
    operations = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg, ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Эта операция не поддерживается.")
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Слишком большая степень.")

            result = operation(left, right)
            if abs(result) > 10**12:
                raise ValueError("Слишком большой результат.")
            return result

        if isinstance(node, ast.UnaryOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Операция не поддерживается.")
            return operation(evaluate(node.operand))

        raise ValueError("Введите только арифметическое выражение.")

    if len(expression) > 80:
        raise ValueError("Выражение слишком длинное.")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)

COMMON_PASSWORDS = {
    "123456", "12345678", "123456789", "password", "qwerty", "qwerty123",
    "111111", "000000", "admin", "welcome", "iloveyou", "abc123",
    "йцукен", "пароль", "123123", "1q2w3e4r", "letmein",
}

def check_password(password):
    issues = []
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[а-яё]", password, re.IGNORECASE):
        pool += 33
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^\w\s]|_", password):
        pool += 32
    entropy = len(password) * math.log2(pool) if pool else 0.0

    if password.lower() in COMMON_PASSWORDS:
        issues.append("это один из самых распространённых паролей")
        entropy = min(entropy, 10.0)
    if len(password) < 12:
        issues.append("длина меньше 12 символов")
    if not re.search(r"[a-zа-яё]", password) or \
            not re.search(r"[A-ZА-ЯЁ]", password):
        issues.append("нет сочетания строчных и заглавных букв")
    if not re.search(r"\d", password):
        issues.append("нет цифр")
    if not re.search(r"[^\w\s]|_", password):
        issues.append("нет специальных символов")
    if re.search(r"(.)\1{2,}", password):
        issues.append("есть повторяющиеся символы подряд")
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|qwer|asdf|zxcv|йцук)",
                 password.lower()):
        issues.append("есть простая последовательность символов")

    if entropy < 40:
        rating = "слабый"
    elif entropy < 60:
        rating = "средний"
    elif entropy < 80:
        rating = "хороший"
    else:
        rating = "сильный"
    return rating, entropy, issues


def generate_password(length=16):
    length = max(12, min(length, 64))
    groups = [
        string.ascii_lowercase, string.ascii_uppercase,
        string.digits, "!@#$%^&*()-_=+?",
    ]
    alphabet = "".join(groups)
    chars = [secrets.choice(group) for group in groups]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

SUSPICIOUS_WORDS = ["login", "verify", "secure", "account", "update",
                    "bank", "confirm", "password", "signin", "wallet"]
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"}
RISKY_TLDS = (".xyz", ".top", ".click", ".work", ".tk", ".gq", ".ml")

def check_url(url):
    signs = []
    normalized = url if "://" in url else "http://" + url
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()

    if parsed.scheme == "http":
        signs.append("нет защищённого соединения (http вместо https)")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        signs.append("вместо доменного имени указан IP-адрес")
    if host in SHORTENERS:
        signs.append("сокращённая ссылка скрывает настоящий адрес")
    if "@" in parsed.netloc:
        signs.append("символ @ в адресе может скрывать настоящий сайт")
    if host.startswith("xn--") or ".xn--" in host:
        signs.append("punycode-домен: возможна подмена символов")
    if host.endswith(RISKY_TLDS):
        signs.append("часто злоупотребляемая доменная зона")
    if host.count(".") >= 3:
        signs.append("слишком много поддоменов")
    if host.count("-") >= 2:
        signs.append("много дефисов в домене")
    if any(word in normalized.lower() for word in SUSPICIOUS_WORDS):
        signs.append("в адресе есть слова, типичные для фишинга "
                     "(login, verify, secure и т. п.)")
    if len(normalized) > 100:
        signs.append("очень длинный адрес")
    return signs

KNOWLEDGE = [
    (("шифровальщик", "вымогател", "ransomware"),
     "Программа-вымогатель шифрует файлы и требует выкуп. Защита: "
     "регулярные резервные копии (хотя бы одна хранится отдельно от "
     "компьютера), обновления системы, осторожность с вложениями. "
     "При заражении отключите устройство от сети и не платите выкуп "
     "без консультации со специалистом."),
    (("фишинг",),
     "Фишинг — обман, при котором мошенники маскируются под банк, "
     "сервис или коллегу, чтобы получить пароли и данные. Признаки: "
     "срочность, угрозы, странный адрес отправителя, подозрительная "
     "ссылка. Не переходите по ссылкам из писем — открывайте сайт "
     "вручную. Для проверки ссылки напишите: проверь ссылку <адрес>."),
    (("социальн", "инженер"),
     "Социальная инженерия — манипуляция людьми, чтобы получить доступ "
     "к данным (звонок «из банка», письмо «от руководителя»). Защита: "
     "проверяйте личность по независимому каналу, не сообщайте коды из "
     "SMS и пароли никому, не поддавайтесь спешке."),
    (("двухфактор", "2fa", "двухэтап", "двухшаговая"),
     "Двухфакторная аутентификация (2FA) требует второй подтверждающий "
     "шаг, кроме пароля: код из приложения-аутентификатора, ключ "
     "безопасности или биометрию. Даже украденный пароль не даст "
     "доступа. Лучше использовать приложение, а не SMS."),
    (("менеджер паролей",),
     "Менеджер паролей хранит уникальные пароли в зашифрованном "
     "хранилище, поэтому нужно помнить только один мастер-пароль. "
     "Он помогает не повторять пароли на разных сайтах."),
    (("парол",),
     "Надёжный пароль: от 12–16 символов, уникальный для каждого "
     "сервиса, без личных данных и словарных слов. Хороший вариант — "
     "длинная фраза из нескольких случайных слов. Храните пароли в "
     "менеджере паролей и включайте 2FA. Могу проверить пароль "
     "(«проверь пароль ...») или сгенерировать («сгенерируй пароль»)."),
    (("ddos", "дудос"),
     "DDoS-атака перегружает сервер множеством запросов с разных "
     "устройств, и сайт становится недоступным. Защита: "
     "CDN и фильтрация трафика, ограничение числа запросов, "
     "запас пропускной способности, план реагирования."),
    (("sql-инъекц", "sql инъекц", "sql injection"),
     "SQL-инъекция — уязвимость, когда ввод пользователя попадает в "
     "SQL-запрос как команда. Защита: параметризованные запросы, "
     "проверка входных данных, минимальные права учётной записи БД."),
    (("xss", "межсайтов"),
     "XSS (межсайтовый скриптинг) — внедрение вредоносного скрипта на "
     "страницу сайта. Защита: экранирование выводимых данных, "
     "политика Content-Security-Policy, проверка ввода."),
    (("уязвимост",),
     "Уязвимость — слабое место в программе или настройках, которым "
     "можно воспользоваться. Закрывается своевременными обновлениями, "
     "правильной настройкой и проверкой кода. Информацию об "
     "известных уязвимостях публикуют в базах вроде CVE."),
    (("шифрован", "криптограф"),
     "Шифрование превращает данные в нечитаемый вид без ключа. "
     "Симметричное использует один ключ (AES), асимметричное — пару "
     "открытого и закрытого (RSA). Шифрование защищает данные на "
     "диске и при передаче по сети (HTTPS)."),
    (("хеш", "хэш"),
     "Хеш-функция превращает данные в строку фиксированной длины; "
     "обратно восстановить исходные данные нельзя. Пароли на сайтах "
     "должны храниться в виде хешей с солью (bcrypt, Argon2), а не "
     "в открытом виде."),
    (("vpn",),
     "VPN создаёт зашифрованный туннель между устройством и VPN-"
     "сервером. Он защищает трафик в публичных сетях, но не делает "
     "вас полностью анонимным и не защищает от вирусов и фишинга."),
    (("брандмауэр", "файрвол", "firewall"),
     "Брандмауэр (файрвол) фильтрует сетевой трафик по правилам и "
     "блокирует нежелательные подключения. Держите встроенный "
     "брандмауэр системы включённым."),
    (("антивирус",),
     "Антивирус обнаруживает и удаляет вредоносные программы по "
     "сигнатурам и поведению. Он нужен, но не заменяет обновления, "
     "резервные копии и осторожность."),
    (("вирус", "троян", "вредонос", "malware", "червь"),
     "Вредоносная программа (malware) — вирусы, трояны, черви, "
     "шпионское ПО. Заражение чаще идёт через вложения, "
     "пиратское ПО и поддельные сайты. Защита: установка программ "
     "только из официальных источников, обновления, антивирус."),
    (("резервн", "бэкап", "backup"),
     "Резервное копирование — основа восстановления после сбоев и "
     "атак. Правило 3-2-1: три копии, на двух разных носителях, "
     "одна из них вне основного места хранения."),
    (("wi-fi", "wifi", "вай-фай", "вайфай"),
     "Безопасный Wi-Fi: шифрование WPA2/WPA3, длинный уникальный "
     "пароль, смена пароля роутера по умолчанию, обновление "
     "прошивки. В публичных сетях не вводите важные данные без VPN."),
    (("обновлен",),
     "Обновления закрывают найденные уязвимости. Включите "
     "автоматическое обновление системы, браузера и приложений."),
    (("конфиденциальн", "персональн"),
     "Персональные данные (паспорт, номера карт, адрес, коды из SMS) "
     "нельзя передавать посторонним и загружать во внешние ИИ-сервисы "
     "без разрешения. Делитесь только необходимым минимумом."),
    (("кибербезопасност", "информационная безопасност",
      "информационной безопасност"),
     "Информационная безопасность защищает данные по трём принципам "
     "(триада CIA): конфиденциальность, целостность и доступность. "
     "Включает технические меры, правила и обучение пользователей."),
]

CHECKLIST = (
    "Базовый чек-лист защиты:\n"
    "1. Уникальные длинные пароли + менеджер паролей.\n"
    "2. Включите двухфакторную аутентификацию.\n"
    "3. Регулярно обновляйте систему и приложения.\n"
    "4. Делайте резервные копии по правилу 3-2-1.\n"
    "5. Не открывайте подозрительные ссылки и вложения.\n"
    "6. Устанавливайте программы только из официальных источников.\n"
    "7. Используйте VPN в публичных Wi-Fi сетях."
)

DEFAULT_RULES = [
    "Использовать уникальный длинный пароль для каждого сервиса",
    "Включить двухфакторную аутентификацию в важных аккаунтах",
    "Регулярно обновлять систему, браузер и приложения",
    "Делать резервные копии по правилу 3-2-1",
    "Не переходить по подозрительным ссылкам и не открывать "
    "неизвестные вложения",
    "Устанавливать программы только из официальных источников",
    "Использовать VPN в публичных Wi-Fi сетях",
]

FORBIDDEN = [
    "взломать", "взлом ", "как взломат", "украсть пароль", "украсть данные",
    "написать вирус", "создать вирус", "написать троян", "кейлоггер",
    "обойти защиту", "слежка за", "следить за чужим", "ddos атаку",
    "провести ddos", "подобрать пароль к чужому", "hack ",
]

def looks_like_secret(text):
    lower = text.lower()
    if re.search(r"(парол[ьяюе]?|password|passwd|pwd|pin|пин)\s*[:=]\s*\S+",
                 lower):
        return True
    if re.search(r"\b\d{13,19}\b", text.replace(" ", "").replace("-", "")):
        return True
    return False

def empty_data():
    return {"tasks": [], "rules": []}

def clean_data(raw):
    data = empty_data()
    if not isinstance(raw, dict):
        return data

    for item in raw.get("tasks", []) if isinstance(raw.get("tasks"), list) \
            else []:
        if isinstance(item, dict) and isinstance(item.get("title"), str):
            data["tasks"].append({
                "title": item["title"],
                "done": bool(item.get("done", False)),
            })

    for item in raw.get("rules", []) if isinstance(raw.get("rules"), list) \
            else []:
        if isinstance(item, dict) and isinstance(item.get("title"), str):
            data["rules"].append({"title": item["title"]})
        elif isinstance(item, str):
            data["rules"].append({"title": item})
    return data


def load_data():
    if not DATA_FILE.exists():
        return empty_data()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return clean_data(json.load(file))
    except (json.JSONDecodeError, OSError):
        print("Предупреждение: файл памяти повреждён. "
              "Создана пустая память.")
        return empty_data()


def save_data(data):
    fd, temp_name = tempfile.mkstemp(dir=DATA_FILE.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        os.replace(temp_name, DATA_FILE)
    except OSError:
        if os.path.exists(temp_name):
            os.remove(temp_name)
        raise

class PersonalAgent:
    def __init__(self, name, role, goal):
        self.name = name
        self.role = role
        self.goal = goal
        self.data = load_data()
        self.history = []   # кратковременная память (только этот запуск)

    def add_task(self, title):
        title = title.strip()
        if not title:
            return "Нельзя добавить пустую задачу."
        if looks_like_secret(title):
            return ("Похоже, в тексте пароль или номер карты. Такие данные "
                    "нельзя хранить в открытом файле. Опишите задачу без них.")

        self.data["tasks"].append({"title": title, "done": False})
        save_data(self.data)
        return f'Задача добавлена: "{title}"'

    def show_tasks(self):
        tasks = self.data["tasks"]
        if not tasks:
            return "Список задач пока пуст."

        lines = ["Ваши задачи:"]
        for number, task in enumerate(tasks, start=1):
            status = "выполнена" if task["done"] else "не выполнена"
            lines.append(f'{number}. {task["title"]} — {status}')
        return "\n".join(lines)

    def complete_task(self, number):
        tasks = self.data["tasks"]
        if number < 1 or number > len(tasks):
            return "Задачи с таким номером нет."

        tasks[number - 1]["done"] = True
        save_data(self.data)
        return (f'Задача "{tasks[number - 1]["title"]}" '
                "отмечена как выполненная.")

    def delete_task(self, number):
        tasks = self.data["tasks"]
        if number < 1 or number > len(tasks):
            return "Задачи с таким номером нет."

        removed = tasks.pop(number - 1)
        save_data(self.data)
        return f'Задача удалена: "{removed["title"]}"'

    def add_rule(self, title):
        title = title.strip()
        if not title:
            return "Нельзя добавить пустое правило."
        if looks_like_secret(title):
            return ("Похоже, в тексте пароль или номер карты. Такие данные "
                    "нельзя хранить в открытом файле.")
        if any(r["title"].lower() == title.lower()
               for r in self.data["rules"]):
            return "Такое правило уже есть в списке."

        self.data["rules"].append({"title": title})
        save_data(self.data)
        return f'Правило добавлено: "{title}"'

    def show_rules(self):
        rules = self.data["rules"]
        if not rules:
            return ("Список правил пока пуст. Добавьте правило командой "
                    "«добавь правило ...» или загрузите набор: "
                    "«загрузи базовые правила».")

        lines = ["Правила цифровой безопасности:"]
        for number, rule in enumerate(rules, start=1):
            lines.append(f'{number}. {rule["title"]}')
        return "\n".join(lines)

    def delete_rule(self, number):
        rules = self.data["rules"]
        if number < 1 or number > len(rules):
            return "Правила с таким номером нет."

        removed = rules.pop(number - 1)
        save_data(self.data)
        return f'Правило удалено: "{removed["title"]}"'

    def load_default_rules(self):
        existing = {r["title"].lower() for r in self.data["rules"]}
        added = 0
        for title in DEFAULT_RULES:
            if title.lower() not in existing:
                self.data["rules"].append({"title": title})
                added += 1
        if added:
            save_data(self.data)
        return f"Добавлено базовых правил: {added}."

    # ----- база знаний -----
    def search_knowledge(self, query):
        for keywords, answer in KNOWLEDGE:
            if any(keyword in query for keyword in keywords):
                return answer
        return None

    @staticmethod
    def parse_number(text):
        text = text.strip()
        return int(text) if text.isdigit() else None

    def respond(self, message):
        text = message.strip()
        lower = text.lower()

        if not text:
            return "Введите команду или сообщение.", text

        if lower.startswith("проверь пароль"):
            password = text[len("проверь пароль"):].strip()
            hidden = "проверь пароль " + "*" * len(password)
            if not password:
                return ("Напишите: проверь пароль <пароль>. Проверка "
                        "выполняется локально, пароль не сохраняется. "
                        "Не вводите свои реальные пароли."), hidden
            rating, entropy, issues = check_password(password)
            lines = [f"Оценка: {rating} (≈{entropy:.0f} бит энтропии)."]
            lines.append("Замечания: " + "; ".join(issues) + "."
                         if issues else "Замечаний нет.")
            lines.append("Не используйте этот пароль в реальных сервисах, "
                         "если вы вводили его в чате.")
            return "\n".join(lines), hidden

        if lower.startswith("сгенерируй пароль"):
            tail = lower[len("сгенерируй пароль"):].strip()
            length = int(tail) if tail.isdigit() else 16
            password = generate_password(length)
            return (f"Сгенерированный пароль: {password}\n"
                    "Сохраните его в менеджере паролей (не в agent_data.json)."
                    ), "сгенерируй пароль [пароль скрыт]"

        if lower.startswith("проверь ссылку"):
            url = text[len("проверь ссылку"):].strip()
            if not url:
                return "Напишите: проверь ссылку <адрес>.", text
            signs = check_url(url)
            if not signs:
                return ("Явных признаков фишинга не найдено, но это "
                        "эвристика, а не гарантия. Проверяйте адрес "
                        "сайта вручную."), text
            return ("Подозрительные признаки:\n- " + "\n- ".join(signs)
                    + "\nНе вводите на этом сайте данные, пока не "
                    "убедитесь в его подлинности."), text

        if lower.startswith("посчитай "):
            expression = text[len("посчитай "):].strip()
            try:
                return f"Результат: {calculate(expression)}", text
            except Exception as error:
                return f"Не удалось выполнить вычисление: {error}", text

        if lower.startswith("добавь задачу "):
            return self.add_task(text[len("добавь задачу "):]), text

        if lower in ("мои задачи", "список задач", "покажи задачи"):
            return self.show_tasks(), text

        if lower.startswith("выполнено"):
            number = self.parse_number(lower[len("выполнено"):])
            if number is None:
                return "Укажите номер задачи. Например: выполнено 1", text
            return self.complete_task(number), text

        if lower.startswith("удали задачу"):
            number = self.parse_number(lower[len("удали задачу"):])
            if number is None:
                return "Укажите номер задачи. Например: удали задачу 1", text
            return self.delete_task(number), text

        if lower.startswith("добавь правило "):
            return self.add_rule(text[len("добавь правило "):]), text

        if lower in ("мои правила", "список правил", "покажи правила"):
            return self.show_rules(), text

        if lower.startswith("удали правило"):
            number = self.parse_number(lower[len("удали правило"):])
            if number is None:
                return "Укажите номер правила. Например: удали правило 1", text
            return self.delete_rule(number), text

        if lower in ("загрузи базовые правила", "базовые правила"):
            return self.load_default_rules(), text

        if any(bad in lower + " " for bad in FORBIDDEN):
            return ("Я не помогаю со взломом, кражей данных и созданием "
                    "вредоносных программ. Могу рассказать, как защитить "
                    "свои аккаунты и системы или как работает такая "
                    "угроза на уровне теории."), text

        if "чек-лист" in lower or "чеклист" in lower or \
                "как защитить" in lower or "как защититься" in lower:
            return CHECKLIST, text

        if lower in ("кто ты", "твоя роль", "как тебя зовут"):
            return (f"Я {self.name}. Моя роль: {self.role}. "
                    f"Моя цель: {self.goal}"), text

        if any(word in lower for word in
               ["привет", "здравствуй", "добрый день", "салам"]):
            return (f"Здравствуйте! Я {self.name}, ваш помощник в роли "
                    f"«{self.role}». Чем могу помочь?"), text

        answer = self.search_knowledge(lower)
        if answer is not None:
            return answer, text

        return self.help_text(unknown=True), text

    def help_text(self, unknown=False):
        head = "Я не распознал команду. Попробуйте:\n" if unknown \
            else "Что я умею:\n"
        return (
            head +
            "- добавь задачу Изучить принципы работы 2FA\n"
            "- мои задачи / выполнено 1 / удали задачу 1\n"
            "- добавь правило Не использовать один пароль для всех сайтов\n"
            "- мои правила / удали правило 1 / загрузи базовые правила\n"
            "- проверь пароль ... / сгенерируй пароль\n"
            "- проверь ссылку ...\n"
            "- посчитай 25 * 4\n"
            "- вопросы про фишинг, VPN, шифрование, 2FA и т. д.\n"
            "- чек-лист защиты\n"
            "- кто ты\n"
            "- история / очистить историю / помощь / выход"
        )

    def chat(self):
        print("=" * 50)
        print(f"Агент: {self.name}")
        print(f"Роль: {self.role}")
        print(f"Цель: {self.goal}")
        print(f"Задач в памяти: {len(self.data['tasks'])}, "
              f"правил: {len(self.data['rules'])}")
        print(f"Данные сохраняются в файл: {DATA_FILE.name}")
        print("Команды: помощь, мои задачи, мои правила, история, выход")
        print("=" * 50)

        while True:
            try:
                message = input("\nВы: ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{self.name}: До свидания! Берегите свои данные.")
                break

            lower = message.lower()

            if lower == "выход":
                print(f"{self.name}: До свидания! Берегите свои данные.")
                break

            if lower == "помощь":
                print(f"{self.name}: {self.help_text()}")
                continue

            if lower == "история":
                if not self.history:
                    print("История текущего запуска пока пуста.")
                else:
                    for item in self.history:
                        print(f"Вы: {item['user']}")
                        print(f"{self.name}: {item['agent']}")
                continue

            if lower == "очистить историю":
                self.history.clear()
                print("История текущего запуска очищена "
                      "(задачи и правила не удалены).")
                continue

            try:
                answer, logged = self.respond(message)
            except OSError as error:
                answer, logged = f"Ошибка при работе с файлом памяти: {error}", message

            self.history.append({"user": logged, "agent": answer})
            print(f"{self.name}: {answer}")

if __name__ == "__main__":
    print("СОЗДАНИЕ АГЕНТА С ДОЛГОВРЕМЕННОЙ ПАМЯТЬЮ")

    name = input("Имя агента (Enter — CyberHelper): ").strip() or "CyberHelper"
    role = input("Роль агента (Enter — Помощник по кибербезопасности): "
                 ).strip() or "Помощник по кибербезопасности"
    goal = input("Цель агента (Enter — по умолчанию): ").strip() or (
        "Хранить правила цифровой безопасности и учебные задачи, "
        "объяснять основы кибербезопасности")

    agent = PersonalAgent(name, role, goal)
    agent.chat()