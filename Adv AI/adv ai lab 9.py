import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, ConfusionMatrixDisplay)

np.random.seed(42)
n = 600

attendance = np.random.randint(40, 101, n)
unfinished = np.random.randint(0, 8, n)
test_score = np.random.randint(35, 101, n)
absences = np.random.randint(0, 16, n)

risk_score = ((attendance < 65).astype(int) +
              (unfinished >= 4).astype(int) +
              (test_score < 55).astype(int) +
              (absences >= 8).astype(int))

target = (risk_score >= 2).astype(int)

data = pd.DataFrame({
    "attendance": attendance,
    "unfinished_tasks": unfinished,
    "test_score": test_score,
    "absences": absences,
    "support_needed": target
})

print(data.head(10))
print("Размер таблицы:", data.shape)
print(data["support_needed"].value_counts())

X = data[["attendance", "unfinished_tasks", "test_score", "absences"]]
y = data["support_needed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
print("Обучающие объекты:", len(X_train))
print("Тестовые объекты:", len(X_test))

tree_model = DecisionTreeClassifier(max_depth=4, random_state=42)
tree_model.fit(X_train, y_train)
tree_pred = tree_model.predict(X_test)
print("Первые 15 прогнозов:", tree_pred[:15])

forest_model = RandomForestClassifier(
    n_estimators=100, max_depth=4, random_state=42)
forest_model.fit(X_train, y_train)
forest_pred = forest_model.predict(X_test)
print("Первые 15 прогнозов:", forest_pred[:15])

def evaluate_model(name, y_true, y_pred):
    print("\n" + name)
    print("Accuracy :", round(accuracy_score(y_true, y_pred), 3))
    print("Precision:", round(precision_score(y_true, y_pred, zero_division=0), 3))
    print("Recall   :", round(recall_score(y_true, y_pred, zero_division=0), 3))
    print("F1-score :", round(f1_score(y_true, y_pred, zero_division=0), 3))

evaluate_model("Дерево решений", y_test, tree_pred)
evaluate_model("Случайный лес", y_test, forest_pred)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ConfusionMatrixDisplay.from_predictions(y_test, tree_pred, ax=axes[0], colorbar=False)
axes[0].set_title("Дерево решений")
ConfusionMatrixDisplay.from_predictions(y_test, forest_pred, ax=axes[1], colorbar=False)
axes[1].set_title("Случайный лес")
plt.tight_layout()
plt.show()

plt.figure(figsize=(18, 9))
plot_tree(tree_model,
          feature_names=X.columns,
          class_names=["Поддержка не нужна", "Поддержка нужна"],
          filled=True, rounded=True, fontsize=8)
plt.show()

importance = pd.Series(
    forest_model.feature_importances_, index=X.columns
).sort_values(ascending=False)
print(importance)
importance.sort_values().plot(kind="barh")
plt.title("Важность признаков случайного леса")
plt.xlabel("Важность")
plt.show()

depths = [1, 2, 3, 4, 5, 6, 8, 10]
train_scores = []
test_scores = []

for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_scores.append(model.score(X_train, y_train))
    test_scores.append(model.score(X_test, y_test))

plt.plot(depths, train_scores, marker="o", label="Обучающая выборка")
plt.plot(depths, test_scores, marker="s", label="Тестовая выборка")
plt.xlabel("Максимальная глубина дерева")
plt.ylabel("Accuracy")
plt.title("Влияние глубины дерева на качество")
plt.legend()
plt.grid(True)
plt.show()

for d, tr, te in zip(depths, train_scores, test_scores):
    print(f"depth={d:2d}  train={tr:.3f}  test={te:.3f}")

# ---- Вариант 25: порог test_score = 50 вместо 55 ----
np.random.seed(42)
n = 600

attendance = np.random.randint(40, 101, n)
unfinished = np.random.randint(0, 8, n)
test_score = np.random.randint(35, 101, n)
absences = np.random.randint(0, 16, n)

risk_score = ((attendance < 65).astype(int) +
              (unfinished >= 4).astype(int) +
              (test_score < 50).astype(int) +
              (absences >= 8).astype(int))

target = (risk_score >= 2).astype(int)

data_v = pd.DataFrame({
    "attendance": attendance,
    "unfinished_tasks": unfinished,
    "test_score": test_score,
    "absences": absences,
    "support_needed": target})

print("Размер таблицы:", data_v.shape)
print(data_v["support_needed"].value_counts())
print("Изменилась метка у строк:", int((data_v["support_needed"] != data["support_needed"]).sum()))

X_v = data_v[["attendance", "unfinished_tasks", "test_score", "absences"]]
y_v = data_v["support_needed"]
X_train_v, X_test_v, y_train_v, y_test_v = train_test_split(
    X_v, y_v, test_size=0.25, random_state=42, stratify=y_v)

tree_v = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train_v, y_train_v)
forest_v = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42).fit(X_train_v, y_train_v)
tree_pred_v = tree_v.predict(X_test_v)
forest_pred_v = forest_v.predict(X_test_v)

def metrics_row(name, y_true, y_pred):
    return [name,
            round(accuracy_score(y_true, y_pred), 3),
            round(precision_score(y_true, y_pred, zero_division=0), 3),
            round(recall_score(y_true, y_pred, zero_division=0), 3),
            round(f1_score(y_true, y_pred, zero_division=0), 3)]

comparison = pd.DataFrame([
    metrics_row("Дерево — исходная модель", y_test, tree_pred),
    metrics_row("Случайный лес — исходная модель", y_test, forest_pred),
    metrics_row("Дерево — вариант 25", y_test_v, tree_pred_v),
    metrics_row("Случайный лес — вариант 25", y_test_v, forest_pred_v),
], columns=["Модель / эксперимент", "Accuracy", "Precision", "Recall", "F1-score"])
print()
print(comparison.to_string(index=False))

# Матрицы ошибок после изменения варианта
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ConfusionMatrixDisplay.from_predictions(y_test_v, tree_pred_v, ax=axes[0], colorbar=False)
axes[0].set_title("Дерево решений (вариант 25)")
ConfusionMatrixDisplay.from_predictions(y_test_v, forest_pred_v, ax=axes[1], colorbar=False)
axes[1].set_title("Случайный лес (вариант 25)")
plt.tight_layout()
plt.show()

# Дерево решений и важность признаков после изменения
plt.figure(figsize=(18, 9))
plot_tree(tree_v, feature_names=X_v.columns,
          class_names=["Поддержка не нужна", "Поддержка нужна"],
          filled=True, rounded=True, fontsize=8)
plt.show()

importance_v = pd.Series(
    forest_v.feature_importances_, index=X_v.columns
).sort_values(ascending=False)
print(importance_v.round(3))
importance_v.sort_values().plot(kind="barh")
plt.title("Важность признаков случайного леса (вариант 25)")
plt.xlabel("Важность")
plt.show()

# Влияние глубины дерева после изменения
train_scores_v = []
test_scores_v = []
for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train_v, y_train_v)
    train_scores_v.append(model.score(X_train_v, y_train_v))
    test_scores_v.append(model.score(X_test_v, y_test_v))

plt.plot(depths, train_scores_v, marker="o", label="Обучающая выборка")
plt.plot(depths, test_scores_v, marker="s", label="Тестовая выборка")
plt.xlabel("Максимальная глубина дерева")
plt.ylabel("Accuracy")
plt.title("Влияние глубины дерева (вариант 25)")
plt.legend()
plt.grid(True)
plt.show()

for d, tr, te in zip(depths, train_scores_v, test_scores_v):
    print(f"depth={d:2d}  train={tr:.3f}  test={te:.3f}")