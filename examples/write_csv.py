import numpy as np
import pandas as pd
from keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0

X_train = np.reshape(X_train, (60000, 784))
y_train = np.reshape(y_train, (60000, 1))
X_test = np.reshape(X_test, (10000, 784))
y_test = np.reshape(y_test, (10000, 1))

train = np.hstack((y_train, X_train))
test = np.hstack((y_test, X_test))
data = np.vstack((train, test))

columns = ['Pixel_{0}'.format(i) for i in range(784)]
columns = ['Label'] + columns
df = pd.DataFrame(data=data, columns=columns)

df.to_csv('mnist.csv', index=False)
