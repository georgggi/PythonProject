import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

X, y = make_classification(
    n_samples=600,
    n_features=5,
    n_informative=4,
    n_redundant=0,
    n_classes=2,
    weights=[0.65, 0.35],
    class_sep=1.0,
    random_state=42
)

columns = ["Показатель_1", "Показатель_2", "Показатель_3",
           "Показатель_4", "Показатель_5"]
df = pd.DataFrame(X, columns=columns)
df["Класс"] = y

df.round(6).to_csv("dataset_lab8.csv", index=False, encoding="utf-8-sig")

print("Размер данных:", df.shape)
print("\nНазвания признаков:", columns)
print("\nПервые строки:")
print(df.head())
print("\nКоличество объектов каждого класса:")
print(df["Класс"].value_counts())
print("\nПропущенные значения:")
print(df.isnull().sum())

X = df[columns]
y = df["Класс"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("\nОбучающая выборка:", X_train.shape, "| Тестовая выборка:", X_test.shape)

log_model = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000, random_state=42)
)
tree_model = DecisionTreeClassifier(max_depth=4, random_state=42)

models = {
    "Логистическая регрессия": log_model,
    "Дерево решений": tree_model
}

rows = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    acc = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred)
    rec = recall_score(y_test, pred)
    f1 = f1_score(y_test, pred)
    rows.append([name, round(acc, 3), round(prec, 3), round(rec, 3), round(f1, 3)])

    print("\nМодель:", name)
    print("Accuracy:", round(acc, 3))
    print("Precision:", round(prec, 3))
    print("Recall:", round(rec, 3))
    print("F1-score:", round(f1, 3))
    print("Матрица ошибок:")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred, digits=3))

comparison = pd.DataFrame(rows, columns=["Модель", "Accuracy", "Precision", "Recall", "F1-score"])
print("\nТаблица сравнения моделей:")
print(comparison.to_string(index=False))

print("\nВажность признаков дерева:")
importances = pd.Series(tree_model.feature_importances_, index=columns).sort_values(ascending=False)
for feature, importance in importances.items():
    print(feature, ":", round(importance, 3))
print("Два наиболее важных признака:", list(importances.index[:2]))

print("\nСравнение глубины дерева:")
for depth in [2, 4, 6, 10]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    print("Глубина:", depth,
          "| Accuracy (train):", round(train_acc, 3),
          "| Accuracy (test):", round(accuracy_score(y_test, pred), 3),
          "| F1 (test):", round(f1_score(y_test, pred), 3))

X_tr30, X_te30, y_tr30, y_te30 = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
print("\nРезультаты при test_size = 0.30:")
rows30 = []
for name, model in {
    "Логистическая регрессия": make_pipeline(StandardScaler(),
                                             LogisticRegression(max_iter=1000, random_state=42)),
    "Дерево решений": DecisionTreeClassifier(max_depth=4, random_state=42)
}.items():
    model.fit(X_tr30, y_tr30)
    pred = model.predict(X_te30)
    rows30.append([name,
                   round(accuracy_score(y_te30, pred), 3),
                   round(precision_score(y_te30, pred), 3),
                   round(recall_score(y_te30, pred), 3),
                   round(f1_score(y_te30, pred), 3)])
print(pd.DataFrame(rows30, columns=["Модель", "Accuracy", "Precision", "Recall", "F1-score"]).to_string(index=False))

print("\nРазброс признаков (std) до масштабирования:")
print(X_train.std().round(3))