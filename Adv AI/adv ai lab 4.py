from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

y_true = [0] * 90 + [1] * 10
y_pred_a = [0] * 100
y_pred_b = [0] * 85 + [1] * 5 + [0] * 2 + [1] * 8
y_pred_b2 = [0] * 85 + [1] * 5 + [1] * 10

def evaluate_model(name, y_true, y_pred):
    print(f"\n{name}")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.2%}")
    print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.2%}")
    print(f"Recall: {recall_score(y_true, y_pred, zero_division=0):.2%}")
    print("Матрица ошибок:")
    print(confusion_matrix(y_true, y_pred))

evaluate_model("Модель A", y_true, y_pred_a)
evaluate_model("Модель B", y_true, y_pred_b)
evaluate_model("Модель B2 (доп. задание)", y_true, y_pred_b2)