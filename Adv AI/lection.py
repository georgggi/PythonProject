import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

base = [(68, 93), (70, 135), (58, 88), (64, 93), (48, 85), (57, 89), (51, 49.5),
        (60, 82.5), (56, 85), (59, 105), (62, 90), (70, 155), (76, 107), (48, 82),
        (58, 74), (68, 88.9), (52, 98), (56, 78.5), (52, 85), (85, 152), (51, 91),
        (85, 119), (50, 86), (56, 92.5), (76, 83.5), (65, 94), (50, 89.5),
        (77, 104), (65, 100.7), (72, 125), (62, 97), (88, 118.5), (70, 80)]
new = [(80, 103), (41, 68)]

df = pd.DataFrame(base + new, columns=["area", "price"])
df["new"] = [0] * len(base) + [1] * len(new)
print(df.head().to_string(index=False))

X, y = df[["area"]], df["price"]
model = LinearRegression().fit(X, y)
pred = model.predict(X)

print(f"\nЦена = {model.coef_[0]:.2f} * площадь + {model.intercept_:.2f}")
print(f"MAE = {mean_absolute_error(y, pred):.2f} тыс. $")
print(f"R²  = {r2_score(y, pred):.3f}")

for a in (65, 100):
    p = model.predict(pd.DataFrame({"area": [a]}))[0]
    print(f"Прогноз для {a} м²: {p:.1f} тыс. $")

old, nw = df[df.new == 0], df[df.new == 1]
m2 = LinearRegression().fit(old[["area"]], old["price"])
print(f"MAE на 2 новых: {mean_absolute_error(nw['price'], m2.predict(nw[['area']])):.2f}")

plt.scatter(old.area, old.price, label="Lalafo")
plt.scatter(nw.area, nw.price, c="r", label="новые 2")
xs = pd.DataFrame({"area": range(38, 92)})
plt.plot(xs.area, model.predict(xs), "k--", label="модель")
plt.xlabel("Площадь, м²")
plt.ylabel("Цена, тыс. USD")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("chart_lalafo.png", dpi=120, bbox_inches="tight")
plt.show()