import ast
import math
import operator
import re
import secrets
import string
from urllib.parse import urlparse

def calculate(expression):
    operations = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.USub: operator.neg, ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                if abs(node.value) > 10**12:
                    raise ValueError("Слишком большое число.")
                return node.value
            raise ValueError("Разрешены только числа.")
        if isinstance(node, ast.BinOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Операция не поддерживается.")
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Слишком большая степень.")
            result = operation(left, right)
            if isinstance(result, (int, float)) and abs(result) > 10**15:
                raise ValueError("Результат слишком большой.")
            return result
        if isinstance(node, ast.UnaryOp):
            operation = operations.get(type(node.op))
            if operation is None:
                raise ValueError("Операция не поддерживается.")
            return operation(evaluate(node.operand))
        raise ValueError("Недопустимое выражение.")

    if len(expression) > 100:
        raise ValueError("Слишком длинное выражение.")
    return evaluate(ast.parse(expression, mode="eval").body)

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
    if not re.search(r"[a-zа-яё]", password) or not re.search(r"[A-ZА-ЯЁ]", password):
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

FORBIDDEN = [
    "взломать", "взлом ", "как взломат", "украсть пароль", "украсть данные",
    "написать вирус", "создать вирус", "написать троян", "кейлоггер",
    "обойти защиту", "слежка за", "следить за чужим", "ddos атаку",
    "провести ddos", "подобрать пароль к чужому", "hack ",
]

class CyberHelper:
    def __init__(self, name="CyberHelper",
                 role="Помощник по кибербезопасности",
                 goal="Объяснять основы информационной безопасности "
                      "и давать безопасные рекомендации"):
        self.name = name
        self.role = role
        self.goal = goal
        self.memory = []

    def show_identity(self):
        print("\n" + "=" * 45)
        print(f"Имя агента: {self.name}")
        print(f"Роль: {self.role}")
        print(f"Цель: {self.goal}")
        print("=" * 45)

    def search_knowledge(self, query):
        for keywords, answer in KNOWLEDGE:
            if any(keyword in query for keyword in keywords):
                return answer
        return None

    def respond(self, message):
        text = message.strip()
        lower = text.lower()

        if not text:
            return "Введите сообщение, пожалуйста.", text

        if lower.startswith("проверь пароль"):
            password = text[len("проверь пароль"):].strip()
            hidden = "проверь пароль " + "*" * len(password)
            if not password:
                return ("Напишите: проверь пароль <пароль>. Проверка "
                        "выполняется локально, пароль не сохраняется. "
                        "Не вводите свои реальные рабочие пароли."), hidden
            rating, entropy, issues = check_password(password)
            lines = [f"Оценка: {rating} (≈{entropy:.0f} бит энтропии)."]
            if issues:
                lines.append("Замечания: " + "; ".join(issues) + ".")
            else:
                lines.append("Замечаний нет.")
            lines.append("Не используйте этот пароль в реальных сервисах, "
                         "если вы вводили его в чате.")
            return "\n".join(lines), hidden

        if lower.startswith("сгенерируй пароль"):
            tail = lower[len("сгенерируй пароль"):].strip()
            length = int(tail) if tail.isdigit() else 16
            password = generate_password(length)
            return (f"Сгенерированный пароль: {password}\n"
                    "Сохраните его в менеджере паролей."), \
                "сгенерируй пароль [пароль скрыт]"

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
            try:
                result = calculate(text[len("посчитай "):].strip())
                return f"Результат вычисления: {result}", text
            except Exception as error:
                return f"Не удалось выполнить вычисление: {error}", text

        if any(bad in lower + " " for bad in FORBIDDEN):
            return ("Я не помогаю со взломом, кражей данных и созданием "
                    "вредоносных программ. Могу рассказать, как защитить "
                    "свои аккаунты и системы или как работает такая "
                    "угроза на уровне теории."), text

        if "чек-лист" in lower or "чеклист" in lower or \
                "как защитить" in lower or "как защититься" in lower:
            return CHECKLIST, text

        answer = self.search_knowledge(lower)
        if answer is not None:
            return answer, text

        if any(word in lower for word in
               ["привет", "здравствуй", "добрый день", "салам"]):
            return (f"Здравствуйте! Я {self.name}, ваш помощник в роли "
                    f"«{self.role}». Моя задача: {self.goal}."), text

        if "как тебя зовут" in lower:
            return f"Меня зовут {self.name}.", text

        if "твоя роль" in lower or "кто ты" in lower:
            return f"Моя роль — {self.role}. Моя цель — {self.goal}.", text

        return ("Я пока не знаю, как выполнить этот запрос.\n"
                "Попробуйте:\n"
                "- спросить про фишинг, VPN, шифрование, 2FA;\n"
                "- «проверь пароль ...» или «сгенерируй пароль»;\n"
                "- «проверь ссылку ...»;\n"
                "- «чек-лист защиты».\n"
                "Мои возможности ограничены программой."), text

    def chat(self):
        self.show_identity()
        print("Начните диалог с агентом.")
        print("Команды: история, очистить, выход\n")

        while True:
            message = input("Вы: ").strip()

            if message.lower() == "выход":
                print("Агент: До свидания! Берегите свои данные.")
                break

            if message.lower() == "история":
                if not self.memory:
                    print("История пока пуста.")
                else:
                    for item in self.memory:
                        print(f"{item['role']}: {item['text']}")
                continue

            if message.lower() == "очистить":
                self.memory.clear()
                print("История диалога очищена.")
                continue

            answer, logged = self.respond(message)
            self.memory.append({"role": "Пользователь", "text": logged})
            self.memory.append({"role": self.name, "text": answer})
            print(f"\n{self.name}: {answer}\n")

if __name__ == "__main__":
    print("СОЗДАНИЕ ПЕРСОНАЛЬНОГО ИИ-АГЕНТА")
    name = input("Введите имя агента (Enter — CyberHelper): ").strip()
    role = input("Введите его роль: ").strip()
    goal = input("Введите его цель: ").strip()

    agent = CyberHelper(
        name or "CyberHelper",
        role or "Помощник по кибербезопасности",
        goal or "Объяснять основы информационной безопасности "
                "и давать безопасные рекомендации",
    )
    agent.chat()