import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Создание синтетического датасета (500 наблюдений)
rng = np.random.default_rng(25)
n = 500
day = rng.integers(0, 7, n)
month = rng.integers(1, 13, n)
is_weekend = (day >= 5).astype(int)
weather = rng.choice([0, 1, 2], size=n, p=[0.35, 0.40, 0.25])
is_holiday = rng.binomial(1, 0.10, n)

weekday_effect = np.array([18, 24, 28, 26, 20, -8, -18])[day]
season_effect = 12 * np.sin((month - 1) / 12 * 2 * np.pi - np.pi / 2) + \
                5 * np.cos((month - 1) / 12 * 2 * np.pi)
weather_effect = np.select(
    [weather == 0, weather == 1, weather == 2], [8, 0, -13])
noise = rng.normal(0, 9, n)
visitors = 72 + weekday_effect + season_effect + weather_effect \
           - 20 * is_holiday + noise
visitors = np.clip(np.rint(visitors), 5, None).astype(int)

df = pd.DataFrame({
    "day_of_week": day,
    "month": month,
    "is_weekend": is_weekend,
    "weather": weather,
    "is_holiday": is_holiday,
    "visitors": visitors
})

# 2. Проверка и очистка данных
print("Пропуски до очистки:", df.isna().sum().sum())
print("Дубликаты до очистки:", df.duplicated().sum())
df = df.drop_duplicates().dropna()

# 3. Признаки и целевая переменная
X = df[["day_of_week", "month", "is_weekend", "weather", "is_holiday"]]
y = df["visitors"]

# 4. Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# 5. Обучение двух моделей
models = {
    "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Random Forest": RandomForestRegressor(
        n_estimators=150, max_depth=8, random_state=42)}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    print(f"\\n{name}")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2:", round(r2, 3))

# 6. Проверка на пяти новых примерах
new_data = pd.DataFrame([
    [0, 3, 0, 0, 0],
    [2, 6, 0, 1, 0],
    [5, 7, 1, 2, 0],
    [6, 1, 1, 0, 1],
    [4, 9, 0, 1, 0]
], columns=X.columns)

best_model = models["Random Forest"]
predictions = best_model.predict(new_data)

for i, value in enumerate(predictions, start=1):
    print(f"Пример {i}: прогноз — {round(value)} посетителей")

# 7. Демонстрация ввода произвольных признаков
demo = pd.DataFrame([{
    "day_of_week": 2,
    "month": 10,
    "is_weekend": 0,
    "weather": 1,
    "is_holiday": 0}])
print("Демонстрационный прогноз:",
      round(best_model.predict(demo)[0]), "посетителей")