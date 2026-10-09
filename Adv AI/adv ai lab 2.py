import pandas as pd, numpy as np

def category(score):
    if score >= 85:
        return 'High'
    elif score >= 70:
        return 'Middle'
    else:
        return 'Low'

data = {'Student': ['Student_1', 'Student_2', 'Student_3', 'Student_4', 'Student_5', 'Student_6',
                     'Student_7', 'Student_8', 'Student_9', 'Student_10', 'Student_10'],
        'Age': [19, 20, np.nan, 21, 250, 19, 20, np.nan, 18, 21, 21],
        'Attendance': [92, 75, 98, 65, 70, 105, 88, 79, np.nan, 72, 72],
        'Average_Score': [86, 68, 91, np.nan, 72, 95, 82, 71, 78, 150, 65],
        'Study_Hours': [8, 4, 10, 3, 5, 9, 7, 5, 6, 12, 4]
}
df = pd.DataFrame(data)
'''print(df.head())
df.info()
print(df.describe())
print(df.isna().sum())
print(df[df.isnull().any(axis=1)])'''
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Attendance'] = df['Attendance'].fillna(df['Attendance'].mean())
df['Average_Score'] = df['Average_Score'].fillna(df['Average_Score'].mean())
#print(df)
df = df.drop_duplicates()
#print(df.duplicated().sum())
'''print(df[df['Age']>100])
print(df[df['Attendance']>100])
print(df[df['Average_Score']>100])'''
df.loc[df['Age'] > 100, 'Age'] = np.nan
df.loc[df['Attendance'] > 100, 'Attendance'] = np.nan
df.loc[df['Average_Score'] > 100, 'Average_Score'] = np.nan
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Attendance'] = df['Attendance'].fillna(df['Attendance'].mean())
df['Average_Score'] = df['Average_Score'].fillna(df['Average_Score'].mean())
#print(df[['Student', 'Age', 'Attendance', 'Average_Score']])
#print(df.isna().sum(), df.describe(), sep='\n')
df['High_Score'] = np.where(df['Average_Score'] >= 70,
                            'Yes', 'No')
df['Score_Category'] = df['Average_Score'].apply(category)
#print(df[['Student', 'average_Score', 'Score_Category']])
md = df[['Student', 'Attendance', 'Average_Score', 'Study_Hours']]
#print(md[df['Attendance'] < 75], md[df['Average_Score'] < 70],
# md[(df['Attendance'] >= 80) & (df['Average_Score'] >= 80)], sep='\n')
df.to_csv('student_clean.csv', index=False)

#print(pd.read_csv('student_clean.csv'))
#print(md[df['Attendance'] < 80], md[df['Average_Score'] < 70], md[df['Study_Hours'] > 6], sep='\n')
df['Risk'] = np.where((df['Attendance'] < 75) | (df['Average_Score'] < 65),
                      'High_Risk', 'Low_Risk')
print(df[['Student', 'Attendance', 'Average_Score', 'Risk']])