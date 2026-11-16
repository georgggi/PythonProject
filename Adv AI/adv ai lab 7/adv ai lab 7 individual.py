import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, confusion_matrix
)

data = {
    "score":        [82, 45, 91, 60, 73, 38, 88, 55, 67, 95,
                     50, 78, 42, 85, 63, 70, 35, 90, 58, 76,
                     48, 80, 66, 93, 52, 72, 40, 87, 61, 69,
                     84, 46, 74, 57, 92, 64, 79, 44, 68, 86],
    "completeness": [95, 60, 100, 70, 90, 50, 98, 65, 80, 100,
                     55, 92, 58, 96, 75, 85, 45, 97, 72, 88,
                     62, 94, 78, 100, 68, 82, 52, 99, 74, 90,
                     93, 66, 86, 70, 98, 79, 91, 56, 84, 96],
    "experience":   [6, 1, 8, 2, 4, 0, 7, 1, 3, 10,
                     2, 5, 1, 6, 3, 4, 0, 9, 2, 5,
                     1, 5, 3, 9, 2, 4, 0, 7, 2, 3,
                     6, 1, 4, 3, 8, 3, 5, 1, 4, 7],
    "passed":       [1, 0, 1, 0, 1, 0, 1, 0, 1, 1,
                     0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                     0, 1, 1, 1, 0, 0, 0, 1, 1, 0,
                     1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
}

df = pd.DataFrame(data)
df.index = df.index + 1
df.index.name = "№"

print("=" * 62)
print("1. Набор данных")
print("=" * 62)
print(df)
print("\nРазмер таблицы:", df.shape)
print("Распределение классов:")
print(df["passed"].value_counts().sort_index())

X = df[["score", "completeness", "experience"]]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("\n" + "=" * 62)
print("3. Разделение выборки")
print("=" * 62)
print("Обучающая выборка:", X_train.shape[0], "объектов")
print("Тестовая выборка: ", X_test.shape[0], "объектов")

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("\n" + "=" * 62)
print("4. Обученная модель")
print("=" * 62)
for name, coef in zip(X.columns, model.coef_[0]):
    print(f"Коэффициент при '{name}': {coef:.4f}")
print(f"Свободный член (intercept): {model.intercept_[0]:.4f}")

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

result = X_test.copy()
result["Факт"] = y_test
result["Прогноз"] = predictions
result["P(прошла)"] = probabilities.round(3)

print("\n" + "=" * 62)
print("5. Прогнозы на тестовой выборке")
print("=" * 62)
print(result.sort_index())

print("\n" + "=" * 62)
print("6. Метрики качества")
print("=" * 62)
print("Accuracy: ", round(accuracy_score(y_test, predictions), 3))
print("Precision:", round(precision_score(y_test, predictions, zero_division=0), 3))
print("Recall:   ", round(recall_score(y_test, predictions, zero_division=0), 3))

cm = confusion_matrix(y_test, predictions, labels=[0, 1])
print("\nМатрица ошибок (строки — факт, столбцы — прогноз):")
print(cm)
tn, fp, fn, tp = cm.ravel()
print(f"TN = {tn} (верно: не прошла)")
print(f"FP = {fp} (ложно пропущена дальше)")
print(f"FN = {fn} (хорошая заявка отклонена)")
print(f"TP = {tp} (верно: прошла)")

new_application = pd.DataFrame(
    [[70, 85, 3]], columns=["score", "completeness", "experience"]
)
p_new = model.predict_proba(new_application)[0, 1]

print("\n" + "=" * 62)
print("7. Новая заявка (баллы 70, полнота документов 85%, опыт 3 года)")
print("=" * 62)
print("Вероятность прохождения отбора:", round(p_new, 3))
print("Прогноз:", "Пройдёт отбор" if p_new >= 0.5 else "Не пройдёт отбор")

print("\n" + "=" * 62)
print("8. Анализ порога")
print("=" * 62)

for t in (0.5, 0.7):
    decision = "Пройдёт отбор" if p_new >= t else "Не пройдёт отбор"
    print(f"Новая заявка, порог {t}: {decision}")

print("\nВлияние порога на тестовую выборку:")
print(f"{'Порог':>6} | {'Прошли отбор':>12} | {'Accuracy':>8} | "
      f"{'Precision':>9} | {'Recall':>6} | {'FP':>2} | {'FN':>2}")
print("-" * 66)
for t in (0.3, 0.5, 0.7, 0.9):
    pred_t = (probabilities >= t).astype(int)
    tn_, fp_, fn_, tp_ = confusion_matrix(
        y_test, pred_t, labels=[0, 1]
    ).ravel()
    print(f"{t:>6} | {pred_t.sum():>12} | "
          f"{accuracy_score(y_test, pred_t):>8.3f} | "
          f"{precision_score(y_test, pred_t, zero_division=0):>9.3f} | "
          f"{recall_score(y_test, pred_t, zero_division=0):>6.3f} | "
          f"{fp_:>2} | {fn_:>2}")