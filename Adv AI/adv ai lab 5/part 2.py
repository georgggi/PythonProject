import json
import urllib.request
import urllib.error

class OllamaAgent:
    def __init__(self, name, role, goal, model="qwen2.5:3b"):
        self.name = name
        self.role = role
        self.goal = goal
        self.model = model
        self.system_prompt = (
            f"Тебя зовут {self.name}. "
            f"Твоя роль: {self.role}. "
            f"Твоя цель: {self.goal}. "
            "Отвечай на русском языке, если пользователь "
            "не попросил другой язык. "
            "Объясняй сложные понятия простыми словами. "
            "Для учебных вопросов приводи примеры. "
            "Не выдумывай факты, если не знаешь ответа. "
            "Помни, что ты учебный помощник, а не "
            "официальный источник информации."
        )
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]

    def ask_model(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

        payload = {
            "model": self.model,
            "messages": self.messages,
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(
                request, timeout=180
            ) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            answer = result["message"]["content"]
            self.messages.append({
                "role": "assistant",
                "content": answer
            })

            if len(self.messages) > 21:
                self.messages = [
                    self.messages[0]
                ] + self.messages[-20:]

            return answer

        except urllib.error.URLError as error:
            if (
                self.messages
                and self.messages[-1]["role"] == "user"
            ):
                self.messages.pop()
            return (
                "Не удалось подключиться к Ollama. "
                "Проверьте, что Ollama запущена, "
                "модель загружена и порт 11434 доступен. "
                f"Подробности: {error}"
            )

        except (KeyError, ValueError, TimeoutError) as error:
            if (
                self.messages
                and self.messages[-1]["role"] == "user"
            ):
                self.messages.pop()
            return f"Ошибка обработки ответа модели: {error}"

    def chat(self):
        print("\n" + "=" * 45)
        print(f"Персональный ИИ-агент: {self.name}")
        print(f"Роль: {self.role}")
        print(f"Цель: {self.goal}")
        print(f"Модель: {self.model}")
        print("=" * 45)
        print("Команды: история, очистить, выход\n")

        while True:
            message = input("Вы: ").strip()

            if message.lower() == "выход":
                print("Агент: До свидания!")
                break

            if message.lower() == "история":
                for item in self.messages:
                    if item["role"] == "system":
                        continue
                    label = (
                        "Вы"
                        if item["role"] == "user"
                        else self.name
                    )
                    print(f"{label}: {item['content']}")
                continue

            if message.lower() == "очистить":
                self.messages = [
                    {"role": "system", "content": self.system_prompt}
                ]
                print("История диалога очищена.\n")
                continue

            if not message:
                continue

            answer = self.ask_model(message)
            print(f"\n{self.name}: {answer}\n")


if __name__ == "__main__":
    print("СОЗДАНИЕ ПЕРСОНАЛЬНОГО ИИ-АГЕНТА")
    name = input("Введите имя агента: ").strip()
    role = input("Введите роль агента: ").strip()
    goal = input("Введите цель агента: ").strip()

    name = name or "StudyMate"
    role = role or "Учебный помощник"
    goal = goal or "Помогать студенту в обучении"

    agent = OllamaAgent(name, role, goal)
    agent.chat()