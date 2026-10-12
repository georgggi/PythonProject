import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('student_clean.csv')

print(df.describe())

print(df[['Attendance', 'Average_Score', 'Study_Hours']].mean())

plt.figure(figsize=(8, 5))
plt.hist(df['Average_Score'], bins=5)
plt.title('Распределение среднего балла')
plt.xlabel('Средний балл')
plt.ylabel('Количество студентов')
plt.show()

df['Score_Category'].value_counts().plot(kind='bar')
plt.title('Количество студентов по категориям успеваемости')
plt.xlabel('Категория')
plt.ylabel('Количество студентов')
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(
    df['Attendance'],
    df['Average_Score']
)
plt.title('Зависимость среднего балла от посещаемости')
plt.xlabel('Посещаемость (%)')
plt.ylabel('Средний балл')
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(
    df['Study_Hours'],
    df['Average_Score']
)
plt.title('Зависимость среднего балла от часов обучения')
plt.xlabel('Часы обучения в неделю')
plt.ylabel('Средний балл')
plt.show()

df['Attendance'].corr(df['Average_Score'])
df['Study_Hours'].corr(df['Average_Score'])

df[df['Study_Hours'] > 6]['Average_Score'].mean()
df[df['Study_Hours'] <= 6]['Average_Score'].mean()

df.groupby('Score_Category')[
    ['Average_Score', 'Attendance', 'Study_Hours']
].mean()

print(df[df['Attendance'] < 75])

print(df[df['Average_Score'] < 70])

print(df[
    (df['Attendance'] < 75) &
    (df['Average_Score'] < 70)])

print(df[
    (df['Attendance'] < 75) &
    (df['Average_Score'] < 70)
][['Student', 'Attendance', 'Study_Hours', 'Average_Score']])

df['Risk'] = np.where(
    (df['Attendance'] < 75) |
    (df['Average_Score'] < 65),
    'Высокий риск',
    'Низкий риск'
)
print(df[['Student', 'Attendance', 'Average_Score', 'Risk']])

print(df['Risk'].value_counts())

df['Risk'].value_counts().plot(kind='bar')
plt.title('Распределение студентов по уровню риска')
plt.xlabel('Уровень риска')
plt.ylabel('Количество студентов')
plt.show()

print(f'Студент с макс средним баллом: {df.loc[df['Average_Score'].idxmax()]}')

print(f'Студент с мин посещаемостью: {df.loc[df['Attendance'].idxmin()]}')

print(f'Студенты, занимающиеся больше 6 ч.: {df[df['Study_Hours'] > 6]}')

plt.figure(figsize=(8, 5))
plt.scatter(df['Study_Hours'], df['Average_Score'])
plt.title('Зависимость среднего балла от часов обучения')
plt.xlabel('Часы обучения в неделю')
plt.ylabel('Средний балл')
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df['Attendance'], df['Average_Score'])
plt.title('Зависимость среднего балла от посещаемости')
plt.xlabel('Посещаемость (%)')
plt.ylabel('Средний балл')
plt.show()

df[['Attendance', 'Study_Hours', 'Average_Score']].corr()

fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)

for a, (x, label) in zip(ax, [('Attendance', 'Посещаемость (%)'),
                              ('Study_Hours', 'Часы обучения в неделю')]):
    a.scatter(df[x], df['Average_Score'])
    k, b = np.polyfit(df[x], df['Average_Score'], 1)   # линия тренда
    xs = np.linspace(df[x].min(), df[x].max(), 50)
    a.plot(xs, k * xs + b, '--', color='gray')
    a.set_xlabel(label)

ax[0].set_ylabel('Средний балл')
fig.suptitle('Что связано со средним баллом: посещаемость и часы обучения')
plt.show()