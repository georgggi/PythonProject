import ast
import operator
import re

def calculate(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
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
            if isinstance(result, (int, float)):
                if abs(result) > 10**15:
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
    tree = ast.parse(expression, mode="eval")
    return evaluate(tree.body)

KNOWLEDGE = {
    "python": (
        "Python — язык программирования общего назначения. "
        "Он используется для автоматизации, анализа данных, "
        "веб-разработки и искусственного интеллекта."
    ),
    "алгоритм": (
        "Алгоритм — последовательность шагов для решения задачи. "
        "Он должен быть понятным и приводить к ожидаемому результату."
    ),
    "искусственный интеллект": (
        "Искусственный интеллект — область информатики, "
        "занимающаяся созданием систем, выполняющих задачи, "
        "для которых обычно требуются интеллектуальные способности."
    ),
    "машинное обучение": (
        "Машинное обучение — направление ИИ, в котором модели "
        "выявляют закономерности в данных и используют их для прогнозов."
    ),
    "ии-агент": (
        "ИИ-агент получает запрос, выбирает действие и использует "
        "доступные инструменты для достижения заданной цели."
    ),
    "функция": (
        "Функция в Python — именованный блок кода, который можно "
        "вызывать повторно. Функции объявляются с помощью def."
    ),
    "нейронная сеть": (
        "Нейронная сеть — математическая модель, состоящая из слоёв "
        "связанных между собой «нейронов». Она обучается на примерах, "
        "подбирая веса связей, и применяется для распознавания "
        "изображений, речи и текста."
    ),
    "нейронные сети": (
        "Нейронная сеть — математическая модель, состоящая из слоёв "
        "связанных между собой «нейронов». Она обучается на примерах, "
        "подбирая веса связей, и применяется для распознавания "
        "изображений, речи и текста."
    ),
    "компьютерное зрение": (
        "Компьютерное зрение — область ИИ, в которой компьютер учится "
        "анализировать изображения и видео: находить объекты, лица, "
        "читать текст и определять движение."
    ),
}

class PersonalAgent:
    def __init__(self, name, role, goal):
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
        query = query.lower()
        for keyword, answer in KNOWLEDGE.items():
            if keyword in query:
                return answer
        return None

    def respond(self, message):
        text = message.strip()
        lower = text.lower()

        if not text:
            return "Введите сообщение, пожалуйста."

        if lower.startswith("посчитай "):
            expression = text[len("посчитай "):].strip()
            try:
                result = calculate(expression)
                return f"Результат вычисления: {result}"
            except Exception as error:
                return f"Не удалось выполнить вычисление: {error}"

        answer = self.search_knowledge(lower)
        if answer is not None:
            return answer

        if any(word in lower for word in [
            "привет", "здравствуй", "добрый день", "салам"
        ]):
            return (
                f"Здравствуйте! Я {self.name}, "
                f"ваш помощник в роли «{self.role}». "
                f"Моя задача: {self.goal}"
            )

        if "как тебя зовут" in lower:
            return f"Меня зовут {self.name}."

        if "твоя роль" in lower or "кто ты" in lower:
            return f"Моя роль — {self.role}. Моя цель — {self.goal}"

        if any(word in lower for word in [
            "как учиться", "план учебы", "план учёбы",
            "подготовиться к экзамену"
        ]):
            return (
                "Предлагаю такой план:\n"
                "1. Определите тему и цель.\n"
                "2. Разделите материал на небольшие части.\n"
                "3. Занимайтесь по 25 минут.\n"
                "4. Решите практические задания.\n"
                "5. Проверьте себя и повторите сложные темы."
            )

        return (
            "Я пока не знаю, как выполнить этот запрос.\n"
            "Попробуйте:\n"
            "- написать «посчитай 25 * 4»;\n"
            "- спросить про Python или машинное обучение;\n"
            "- попросить план подготовки к экзамену.\n"
            "Мои возможности ограничены программой."
        )

    def chat(self):
        self.show_identity()
        print("Начните диалог с агентом.")
        print("Команды: история, очистить, выход\n")

        while True:
            message = input("Вы: ").strip()

            if message.lower() == "выход":
                print("Агент: До свидания!")
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

            self.memory.append({
                "role": "Пользователь",
                "text": message
            })

            answer = self.respond(message)

            self.memory.append({
                "role": self.name,
                "text": answer
            })

            print(f"\n{self.name}: {answer}\n")

if __name__ == "__main__":
    print("СОЗДАНИЕ ПЕРСОНАЛЬНОГО ИИ-АГЕНТА")
    name = input("Введите имя агента: ").strip()
    role = input("Введите его роль: ").strip()
    goal = input("Введите его цель: ").strip()

    name = name or "StudyMate"
    role = role or "Учебный помощник"
    goal = goal or "Помогать студенту в обучении"

    agent = PersonalAgent(name, role, goal)
    agent.chat()