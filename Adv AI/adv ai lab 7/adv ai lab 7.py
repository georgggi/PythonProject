import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, confusion_matrix
)

data = {
    "absences": [2, 8, 1, 6, 3, 10, 4, 7, 0, 9, 2, 5, 1, 8, 3, 11, 4, 6, 0, 7,
                 2, 9, 5, 6, 1, 8, 3, 10, 4, 7],
    "missing":  [1, 5, 0, 4, 1, 6, 2, 5, 1, 4, 2, 3, 1, 3, 0, 7, 1, 2, 0, 4,
                 1, 5, 1, 5, 0, 6, 2, 4, 0, 3],
    "average":  [86, 55, 92, 61, 78, 48, 73, 58, 89, 52, 81, 67, 90, 63, 84, 45,
                 76, 69, 95, 60, 88, 50, 72, 57, 93, 54, 79, 56, 82, 65],
    "risk":     [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
}

df = pd.DataFrame(data)
df.index = df.index + 1
df.index.name = "№"

print("=" * 60)
print("Шаг 1. Набор данных")
print("=" * 60)
print(df)
print("\nРазмер таблицы:", df.shape)
print("Распределение классов:")
print(df["risk"].value_counts().sort_index())

X = df[["absences", "missing", "average"]]
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("\n" + "=" * 60)
print("Шаг 3. Разделение выборки")
print("=" * 60)
print("Обучающая выборка:", X_train.shape[0], "объектов")
print("Тестовая выборка: ", X_test.shape[0], "объектов")
print("Классы в тесте:", y_test.value_counts().sort_index().to_dict())

model = LogisticRegression()
model.fit(X_train, y_train)

print("\n" + "=" * 60)
print("Шаг 4. Обученная модель")
print("=" * 60)
for name, coef in zip(X.columns, model.coef_[0]):
    print(f"Коэффициент при '{name}': {coef:.4f}")
print(f"Свободный член (intercept): {model.intercept_[0]:.4f}")

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

result = X_test.copy()
result["Факт"] = y_test
result["Прогноз"] = predictions
result["P(риск)"] = probabilities.round(3)

print("\n" + "=" * 60)
print("Шаг 5. Прогнозы на тестовой выборке")
print("=" * 60)
print(result.sort_index())

print("\n" + "=" * 60)
print("Шаг 6. Метрики качества")
print("=" * 60)
print("Accuracy: ", accuracy_score(y_test, predictions))
print("Precision:", precision_score(y_test, predictions, zero_division=0))
print("Recall:   ", recall_score(y_test, predictions, zero_division=0))

cm = confusion_matrix(y_test, predictions)
print("\nМатрица ошибок (строки — факт, столбцы — прогноз):")
print(cm)
tn, fp, fn, tp = cm.ravel()
print(f"TN = {tn} (верно: риска нет)")
print(f"FP = {fp} (ложная тревога)")
print(f"FN = {fn} (пропущенный риск)")
print(f"TP = {tp} (верно: риск есть)")

new_student = pd.DataFrame(
    [[7, 4, 59]], columns=["absences", "missing", "average"]
)
probability = model.predict_proba(new_student)[0, 1]

print("\n" + "=" * 60)
print("Шаг 7. Новый студент (пропусков 7, долгов по заданиям 4, балл 59)")
print("=" * 60)
print("Вероятность риска:", round(probability, 3))
print("Прогноз:", "Есть риск" if probability >= 0.5 else "Риск не выявлен")

print("\n" + "=" * 60)
print("Шаг 8. Анализ порога")
print("=" * 60)

for t in (0.5, 0.7):
    decision = "Есть риск" if probability >= t else "Риск не выявлен"
    print(f"Новый студент, порог {t}: {decision}")

print("\nВлияние порога на тестовую выборку:")
print(f"{'Порог':>6} | {'Отнесено к риску':>16} | {'Accuracy':>8} | "
      f"{'Precision':>9} | {'Recall':>6} | {'FP':>2} | {'FN':>2}")
print("-" * 70)
for t in (0.3, 0.5, 0.7, 0.9):
    pred_t = (probabilities >= t).astype(int)
    tn_, fp_, fn_, tp_ = confusion_matrix(
        y_test, pred_t, labels=[0, 1]
    ).ravel()
    print(f"{t:>6} | {pred_t.sum():>16} | "
          f"{accuracy_score(y_test, pred_t):>8.3f} | "
          f"{precision_score(y_test, pred_t, zero_division=0):>9.3f} | "
          f"{recall_score(y_test, pred_t, zero_division=0):>6.3f} | "
          f"{fp_:>2} | {fn_:>2}")