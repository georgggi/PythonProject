import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

digits = load_digits()
X = digits.data / 16.0
y = digits.target
print(X.shape, np.unique(y))

fig, axes = plt.subplots(1, 5, figsize=(10, 2))
for ax, img, label in zip(axes, digits.images[:5], y[:5]):
    ax.imshow(img, cmap="gray")
    ax.set_title(f"Цифра: {label}")
    ax.axis("off")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

mlp = MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu",
                    max_iter=500, random_state=42)
mlp.fit(X_train, y_train)
pred_mlp = mlp.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred_mlp))
print(classification_report(y_test, pred_mlp))

rf = RandomForestClassifier(n_estimators=150, random_state=42)
rf.fit(X_train, y_train)
pred_rf = rf.predict(X_test)
print("MLP:", accuracy_score(y_test, pred_mlp))
print("Random Forest:", accuracy_score(y_test, pred_rf))
ConfusionMatrixDisplay.from_predictions(y_test, pred_mlp)
plt.title("Матрица ошибок MLP")
plt.show()

rows = []
for arch in [(32,), (64, 32), (128, 64)]:
    for act in ["relu", "tanh"]:
        m = MLPClassifier(hidden_layer_sizes=arch, activation=act,
                          max_iter=500, random_state=42)
        m.fit(X_train, y_train)
        rows.append({"Архитектура": str(arch), "Активация": act,
                     "Accuracy": round(accuracy_score(y_test, m.predict(X_test)), 4),
                     "Итераций": m.n_iter_})
table = pd.DataFrame(rows)
print(table.to_string(index=False))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, pred_mlp)
np.fill_diagonal(cm, 0)
pairs = [(cm[i, j], i, j) for i in range(10) for j in range(10) if cm[i, j] > 0]
pairs.sort(reverse=True)
if pairs:
    for cnt, true, pr in pairs[:5]:
        print(f"Цифру {true} путали с {pr}: {cnt} раз(а)")
else:
    print("Ошибок нет: все цифры распознаны верно.")