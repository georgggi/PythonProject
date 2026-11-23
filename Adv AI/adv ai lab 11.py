# ЛАБОРАТОРНАЯ РАБОТА № 11. Определение тональности отзывов (NLP, TF-IDF)

# %% 1. Создание учебного набора данных
import pandas as pd

texts = [
"Очень хороший сервис, всё понравилось",
"Отличное качество и быстрая доставка",
"Мне понравилось обслуживание",
"Покупкой полностью доволен",
"Прекрасный товар, рекомендую",
"Всё работает отлично",
"Хорошее качество за свою цену",
"Быстро, удобно и качественно",
"Вежливый персонал, спасибо",
"Буду пользоваться снова",
"Ужасное качество, не рекомендую",
"Очень плохое обслуживание",
"Товар пришёл сломанным",
"Деньги потрачены зря",
"Доставка задержалась, я недоволен",
"Не понравилось, больше не куплю",
"Качество отвратительное",
"Сервис работает очень плохо",
"Получил не то, что заказывал",
"Разочарован покупкой",
"Отличный результат, спасибо",
"Приятный опыт, всё хорошо",
"Сотрудники помогли решить вопрос",
"Всё соответствует описанию",
"Плохой товар и долгая доставка",
"Заказ потеряли, поддержка не помогла",
"Не советую этот магазин",
"Очень разочарован качеством",
"Пользоваться неудобно",
"Возврат оформить невозможно"
]
labels = [1]*10 + [0]*10 + [1]*4 + [0]*6
df = pd.DataFrame({"text": texts, "label": labels})
print(df["label"].value_counts())

# %% 2. Разделение и обучение модели
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
)
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42))
])
model.fit(X_train, y_train)

# %% 3. Оценка качества
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred, zero_division=0))
ConfusionMatrixDisplay.from_predictions(y_test, pred)
plt.show()

# %% 4. Проверка новых отзывов
new_reviews = [
    "Очень понравилось, рекомендую всем",
    "Ужасный сервис, больше не обращусь",
    "Качество хорошее, но доставка была долгой"
]
for review, result in zip(new_reviews, model.predict(new_reviews)):
    print(review, "->", "Положительный" if result == 1 else "Отрицательный")

# %% 5. Индивидуальное исследование
# 5.1 Свои отзывы (5 положительных и 5 отрицательных)
my_texts = [
    "Отличный магазин, всё пришло вовремя",
    "Товар супер, очень доволен покупкой",
    "Курьер вежливый, спасибо за быструю доставку",
    "Качество на высоте, буду заказывать ещё",
    "Прекрасное обслуживание, рекомендую друзьям",
    "Ужасный магазин, товар бракованный",
    "Доставка очень долгая, я разочарован",
    "Качество плохое, деньги выброшены",
    "Поддержка не отвечает, не рекомендую",
    "Упаковка порвана, остался недоволен",
]
my_labels = [1]*5 + [0]*5

df2 = pd.concat([df, pd.DataFrame({"text": my_texts, "label": my_labels})],
                ignore_index=True)

X_tr, X_te, y_tr, y_te = train_test_split(
    df2["text"], df2["label"], test_size=0.25, random_state=42, stratify=df2["label"]
)

# 5.2 Сравнение ngram_range=(1,1) и (1,2)
ambiguous = ["В целом нормально, но ожидал большего",
             "Неплохо, но есть недостатки"]
models = {}
for ngr in [(1, 1), (1, 2)]:
    m = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=ngr)),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42))
    ])
    m.fit(X_tr, y_tr)
    models[ngr] = m
    p = m.predict(X_te)
    print(f"\nngram_range={ngr}  Accuracy = {accuracy_score(y_te, p):.3f}")
    print(classification_report(y_te, p, zero_division=0))

    # 5.3 Неоднозначные фразы
    for t, r in zip(ambiguous, m.predict(ambiguous)):
        proba = m.predict_proba([t])[0][1]
        print(f"  «{t}» -> {'Положительный' if r == 1 else 'Отрицательный'} (P(+)={proba:.2f})")

# 5.4 Поиск ошибок на всём наборе: показываем ошибочно классифицированные отзывы
m = models[(1, 2)]
all_pred = m.predict(X_te)
errors = [(t, a, p) for t, a, p in zip(X_te, y_te, all_pred) if a != p]
print("\nОшибки модели на тесте:")
if errors:
    for t, a, p in errors:
        print(f"  «{t}»: истинная метка {a}, предсказано {p}")
else:
    print("  Ошибок на тесте нет. Пример ошибки смотрите на неоднозначных фразах выше "
          "и на отзыве 'Качество хорошее, но доставка была долгой'.")