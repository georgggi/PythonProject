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

class Lesson(ABC):
    KIND, MAX_SCORE = "урок", 10

    def __init__(self, title, **details):
        self.title = title
        self.details = details

    def __str__(self):
        extra = ", ".join(f"{k}: {v}" for k, v in self.details.items())
        return f"{self.KIND:<9s} «{self.title}» (макс. {self.MAX_SCORE} б.){' | ' + extra if extra else ''}"

class VideoLesson(Lesson):
    KIND, MAX_SCORE = "видео", 5

class TextLesson(Lesson):
    KIND, MAX_SCORE = "текст", 5

class QuizLesson(Lesson):
    KIND, MAX_SCORE = "тест", 20

class AssignmentLesson(Lesson):
    KIND, MAX_SCORE = "задание", 30

LESSON_TYPES = {"video": VideoLesson, "text": TextLesson,
                "quiz": QuizLesson, "assignment": AssignmentLesson}

class Course(Observable):
    DIRECTION = "общее"
    PASS_PERCENT = 60

    def __init__(self, title):
        super().__init__()
        self.title = title
        self._lessons = []
        self._students = []

    @property
    def lessons(self):
        return list(self._lessons)

    def publish_lesson(self, kind, title, **details):
        creator = LESSON_TYPES.get(kind)
        if creator is None:
            raise ValueError(f"Неизвестный тип урока: {kind}")
        lesson = creator(title, **details)
        self._lessons.append(lesson)
        self._notify("LESSON_PUBLISHED",
                     {"course": self, "lesson": lesson,
                      "text": f"в курсе «{self.title}» новый урок: {lesson.KIND} «{title}»"})
        return lesson

    def enroll(self, student):
        if student in self._students:
            raise ValueError(f"{student.name} уже записан на «{self.title}»")
        self._students.append(student)
        self.subscribe(student)
        student.courses.append(self)

    def total_score(self):
        return sum(l.MAX_SCORE for l in self._lessons)

    def __str__(self):
        return f"[{self.DIRECTION}] {self.title}: уроков {len(self._lessons)}, студентов {len(self._students)}"

class ProgrammingCourse(Course):
    DIRECTION, PASS_PERCENT = "программирование", 70

class DesignCourse(Course):
    DIRECTION, PASS_PERCENT = "дизайн", 60

class DataScienceCourse(Course):
    DIRECTION, PASS_PERCENT = "data science", 75

class LanguageCourse(Course):
    DIRECTION, PASS_PERCENT = "языки", 65

class CourseFactory:
    _registry = {"программирование": ProgrammingCourse, "дизайн": DesignCourse,
                 "data science": DataScienceCourse, "языки": LanguageCourse}

    @classmethod
    def create(cls, direction, title):
        creator = cls._registry.get(direction)
        if creator is None:
            raise ValueError(f"Неизвестное направление: {direction}")
        return creator(title)

class CourseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._catalog = []
        return cls._instance

    def register(self, course):
        self._catalog.append(course)

    def find(self, direction):
        return [c for c in self._catalog if c.DIRECTION == direction]

    def show(self):
        print(f"КАТАЛОГ КУРСОВ ({len(self._catalog)}):")
        for c in self._catalog:
            print("  ", c)

class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []
        self._scores = {}
        self.inbox = []

    def update(self, event, data):
        self.inbox.append(data["text"])
        print(f"    [Студент {self.name}] {data['text']}")

    def complete(self, course, lesson_title, score):
        lesson = next((l for l in course.lessons if l.title == lesson_title), None)
        if course not in self.courses:
            raise ValueError(f"{self.name} не записан на «{course.title}»")
        if lesson is None:
            raise ValueError(f"В курсе нет урока «{lesson_title}»")
        if not 0 <= score <= lesson.MAX_SCORE:
            raise ValueError(f"Балл за «{lesson_title}» должен быть от 0 до {lesson.MAX_SCORE}")
        self._scores[(course.title, lesson_title)] = score

    def progress(self, course):
        done = sum(1 for l in course.lessons if (course.title, l.title) in self._scores)
        return done, len(course.lessons)

    def final_percent(self, course):
        total = course.total_score()
        got = sum(s for (c, _), s in self._scores.items() if c == course.title)
        return got / total * 100 if total else 0.0

    def report(self, course):
        done, total = self.progress(course)
        pct = self.final_percent(course)
        verdict = "ЗАЧЁТ" if pct >= course.PASS_PERCENT and done == total else "не зачтён"
        bar = "█" * done + "░" * (total - done)
        print(f"  {self.name:<8s} {bar} {done}/{total} уроков | итог {pct:5.1f} % "
              f"(порог {course.PASS_PERCENT} %) -> {verdict}")

if __name__ == "__main__":
    manager = CourseManager()
    py = CourseFactory.create("программирование", "Python для начинающих")
    ds = CourseFactory.create("data science", "Основы анализа данных")
    dz = CourseFactory.create("дизайн", "UX/UI с нуля")
    for c in (py, ds, dz):
        manager.register(c)
    aidar, bermet, nurlan = Student("Айдар"), Student("Бермет"), Student("Нурлан")
    print("--- Запись студентов (агрегация) и первые уроки ---")
    py.enroll(aidar)
    py.enroll(bermet)
    ds.enroll(bermet)
    py.publish_lesson("video", "Введение и установка", duration_min=12)
    py.publish_lesson("text", "Переменные и типы", pages=8)
    print("\n--- Нурлан записывается позже ---")
    py.enroll(nurlan)
    py.publish_lesson("quiz", "Тест по основам", questions=15)
    py.publish_lesson("assignment", "Мини-калькулятор", deadline="15.05")
    ds.publish_lesson("video", "Что такое данные", duration_min=20)
    print("\n--- Нурлан отписывается от уведомлений ---")
    py.unsubscribe(nurlan)
    py.publish_lesson("text", "Функции", pages=10)
    manager.show()
    print("\nУроки курса:")
    for l in py.lessons:
        print("  ", l)
    print("Курсы по направлению «программирование»:", [c.title for c in manager.find("программирование")])
    print("\n--- Прохождение курса ---")
    marks = {aidar: [5, 5, 18, 28, 5], bermet: [5, 5, 12, 20, 3], nurlan: [5, 4, 8]}
    for student, ms in marks.items():
        for lesson, mark in zip(py.lessons, ms):
            student.complete(py, lesson.title, mark)
    print("\nИтоги по курсу «Python для начинающих» (макс. {} б.):".format(py.total_score()))
    for s in (aidar, bermet, nurlan):
        s.report(py)
    print("\n--- Ошибки ---")
    for action in (lambda: aidar.complete(py, "Тест по основам", 99),
                   lambda: aidar.complete(ds, "Что такое данные", 3),
                   lambda: aidar.complete(py, "Несуществующий", 1),
                   lambda: py.enroll(aidar), lambda: py.publish_lesson("podcast", "X"),
                   lambda: CourseFactory.create("кулинария", "X")):
        try:
            action()
        except ValueError as e:
            print("  ValueError:", e)
    print("Один менеджер:", CourseManager() is CourseManager())
    print(f"Входящих у Нурлана: {len(nurlan.inbox)}, у Бермет: {len(bermet.inbox)}")