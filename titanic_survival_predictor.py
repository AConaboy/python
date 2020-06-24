import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the passenger data
df = pd.read_csv('passengers.csv')
#print(df)
# Update sex column to numerical

for i in range(len(df['Sex'])):
    if df['Sex'][i] == 'male':
        df['Sex'][i] = 0
    elif df['Sex'][i] =='female':
        df['Sex'][i] = 1
#print(df['Sex'])
#Fill the nan values in the age column

#print(df['Age'].values)
numbered_ages = []
for i in range(len(df['Age'].values)):
  if np.isnan(df['Age'].values[i]) == False:
    numbered_ages.append(df['Age'].values[i])

mean_age = np.sum(numbered_ages)/len(df['Age'].values)
#print(mean_age)
for i in range(len(df['Age'].values)):
  if np.isnan(df['Age'].values[i]) == True:
    df['Age'].values[i] = mean_age
# Create a first class column
FirstClass = []
for i in range(len(df['Pclass'])):
  if df['Pclass'][i] == 1:
    FirstClass.append(1)
  else:
    FirstClass.append(0)
df['FirstClass']=FirstClass
#print(df['FirstClass'])
# Create a second class column
SecondClass = []
for i in range(len(df['Pclass'])):
  if df['Pclass'][i] == 2:
    SecondClass.append(1)
  else:
    SecondClass.append(0)
df['SecondClass']=SecondClass
#print(df['SecondClass'])

# Select the desired features
features = df[['Sex', 'Age', 'FirstClass', 'SecondClass']]
survival = df['Survived']
# Perform train, test, split
x_train, x_test, y_train, y_test = train_test_split(features, survival, test_size=0.2)

# Scale the feature data so it has mean = 0 and standard deviation = 1
scaler = StandardScaler()
train_features = scaler.fit_transform(x_train)
test_features = scaler.transform(x_test)
# Create and train the model
model = LogisticRegression()
model.fit(x_train, y_train)
# Score the model on the train data
print("Model score on training data: %.2f"%model.score(x_train, y_train))

# Score the model on the test data
print("Model score on testing data: %.2f"%model.score(x_test, y_test))

# Analyze the coefficients


# Sample passenger features
Jack = np.array([0.0,20.0,0.0,0.0])
Rose = np.array([1.0,17.0,1.0,0.0])
You = np.array([0.0,22.7,0.0,1.0])
Mum = np.array([1.0, 59.8, 0.0, 1.0])
Heather = np.array([1.0, 23.0, 0.0, 1.0])

# Combine passenger arrays
sample_passengers = np.array([Jack, Rose, You, Mum, Heather])

# Scale the sample passenger features
sample_passengers = scaler.transform(sample_passengers)

# Make survival predictions!
print(model.predict(sample_passengers))
print(model.predict_proba(sample_passengers))
