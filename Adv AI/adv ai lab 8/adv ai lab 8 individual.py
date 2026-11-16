import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

rng = np.random.default_rng(42)
n = 600

scores = np.clip(rng.normal(65, 15, n), 0, 100)
docs = np.clip(rng.normal(85, 12, n), 30, 100)
experience = np.clip(rng.gamma(2.0, 2.5, n), 0, 20)
criteria = np.clip(rng.normal(6.5, 2.0, n), 0, 10)
days_before = rng.integers(0, 31, n)

z = (0.07 * (scores - 65)
     + 0.04 * (docs - 85)
     + 0.12 * (experience - 5)
     + 0.55 * (criteria - 6.5)
     + 0.03 * (days_before - 15)
     - 0.4
     + rng.normal(0, 1.0, n))
prob = 1 / (1 + np.exp(-z))
y_cls = (rng.random(n) < prob).astype(int)

columns = ["Баллы", "Полнота_документов", "Опыт", "Соответствие_критериям", "Сроки_подачи"]
df = pd.DataFrame({
    "Баллы": scores.round(1),
    "Полнота_документов": docs.round(1),
    "Опыт": experience.round(1),
    "Соответствие_критериям": criteria.round(1),
    "Сроки_подачи": days_before,
    "Класс": y_cls
})
df.to_csv("dataset_variant25.csv", index=False, encoding="utf-8-sig")

print("Размер данных:", df.shape)
print("\nПервые строки:")
print(df.head())
print("\nКоличество объектов каждого класса:")
print(df["Класс"].value_counts())
print("\nПропущенные значения:")
print(df.isnull().sum())
print("\nОписательная статистика:")
print(df[columns].describe().round(2))

X = df[columns]
y = df["Класс"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

log_model = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=1000, random_state=42))
tree_model = DecisionTreeClassifier(max_depth=4, random_state=42)
models = {"Логистическая регрессия": log_model, "Дерево решений": tree_model}

rows = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    rows.append([name,
                 round(accuracy_score(y_test, pred), 3),
                 round(precision_score(y_test, pred), 3),
                 round(recall_score(y_test, pred), 3),
                 round(f1_score(y_test, pred), 3)])
    print("\nМодель:", name)
    print("Матрица ошибок:")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred, digits=3))

print("\nТаблица сравнения моделей:")
print(pd.DataFrame(rows, columns=["Модель", "Accuracy", "Precision", "Recall", "F1-score"]).to_string(index=False))

print("\nВажность признаков дерева:")
imp = pd.Series(tree_model.feature_importances_, index=columns).sort_values(ascending=False)
print(imp.round(3))

print("\nКоэффициенты логистической регрессии (на стандартизованных признаках):")
coef = pd.Series(log_model.named_steps["logisticregression"].coef_[0], index=columns)
print(coef.round(3))

print("\nСравнение глубины дерева:")
for depth in [2, 4, 6, 10]:
    m = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)
    pred = m.predict(X_test)
    print("Глубина:", depth,
          "| Accuracy (train):", round(accuracy_score(y_train, m.predict(X_train)), 3),
          "| Accuracy (test):", round(accuracy_score(y_test, pred), 3),
          "| F1 (test):", round(f1_score(y_test, pred), 3))