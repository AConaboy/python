import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets

digits = datasets.load_digits()
# print(digits.target)
# plt.gray()
# plt.matshow(digits.images[100])
# plt.show()

from sklearn.cluster import KMeans

model = KMeans(n_clusters = 10, random_state=69)
model.fit(digits.data)

fig = plt.figure(figsize=(10,5))
fig.suptitle('Cluster center images', fontsize=14, fontweight='bold')

for i in range(10):
  ax = fig.add_subplot(2, 5, 1+i)
  ax.imshow(model.cluster_centers_[i].reshape((8, 8)), cmap=plt.cm.binary)
plt.show()

new_samples = np.array([

[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,2.13,3.81,2.73,0.45,0.00,0.00,2.97,5.93,7.62,7.39,7.62,6.32,1.21,0.00,5.86,6.32,3.49,0.45,3.42,7.62,3.04,0.00,0.00,0.00,0.00,0.07,2.20,7.62,3.58,0.00,0.00,0.68,3.57,6.24,7.62,7.23,1.28,0.00,2.88,7.62,7.62,7.62,6.77,2.50,1.51,0.00,1.37,4.57,5.10,5.94,7.32,7.62,6.47],

[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,1.59,4.11,0.08,0.00,0.00,0.00,0.00,0.60,7.30,6.86,7.46,4.94,0.07,0.60,4.41,7.55,7.39,1.59,4.54,7.62,3.48,7.08,7.62,5.02,1.36,0.00,0.15,6.54,5.33,7.62,3.95,1.07,0.00,0.00,0.00,6.85,4.56,7.62,7.62,7.16,4.27,3.96,5.33,7.62,4.10],

[0.00,0.45,3.50,3.81,3.81,3.12,1.14,0.00,0.61,6.69,7.55,6.86,7.01,7.62,7.62,5.63,1.51,6.55,1.74,0.00,0.00,1.29,4.39,7.62,0.00,0.00,0.08,2.43,5.41,6.10,6.93,7.39,0.00,0.83,5.62,7.62,6.86,4.80,4.57,1.67,0.00,7.30,7.62,7.39,4.72,3.81,3.81,1.83,0.00,5.47,5.41,6.02,6.86,6.86,6.86,3.81,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00],

[0.00,0.00,0.00,0.00,0.00,0.15,0.60,0.00,0.00,0.60,3.73,5.63,7.62,7.62,7.62,6.16,0.00,4.03,7.55,6.86,4.72,3.05,4.48,7.62,0.00,4.56,6.85,0.00,0.00,0.00,0.45,6.62,0.00,4.57,6.85,0.00,0.00,0.00,0.45,6.62,0.00,4.18,7.54,0.45,0.00,1.59,6.17,7.47,0.00,2.20,7.55,6.78,6.17,7.47,7.00,2.35,0.00,0.00,2.27,5.02,5.18,3.88,0.45,0.00]

])

new_labels = model.predict(new_samples)
print(new_labels)
