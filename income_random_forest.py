def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import numpy as np

df = pd.read_csv('income.csv', header=0, delimiter=', ')
#print(df.iloc[0])
#print(df['workclass'].value_counts())
df['workclass-int'] = df['workclass'].apply(lambda row: 0 if row == 'Private' else 1)
df['sex-int'] = df['sex'].apply(lambda row: 0 if row == 'Male' else 1)
labels = df[['income']]
df['race-int'] = df['race'].apply(lambda row: 0 if row == 'White' else 1)
df['country-int'] = df['native-country'].apply(lambda row: 0 if row == 'United States' else 1)
data = df[['age', 'capital-gain', 'capital-loss', 'hours-per-week', 'sex-int', 'country-int', 'race-int', 'education-num']]

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, random_state=1)
trees_in_forest = np.arange(1000,8000,1000)
accuracy = []
for i in range(1,8):
    forest = RandomForestClassifier(n_estimators=i*1000, random_state=1)
    forest.fit(train_data, train_labels)
    score = forest.score(test_data, test_labels)
    print("accuracy: %.2f" %score)
    accuracy.append(score)

import matplotlib.pyplot as plt

plt.plot(trees_in_forest, accuracy)
plt.xlabel('trees in forest')
plt.ylabel('accuracy')
plt.title('Accuracy of random forest as a function of trees in forest')
plt.show()
