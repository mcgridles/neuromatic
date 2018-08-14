from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Flatten, InputLayer, Dense

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train, X_test = X_train / 255.0, X_test / 255.0

model = Sequential([
    InputLayer(input_shape=(28,28,)),
    Flatten(),
    Dense(32, activation='softmax'),
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=5)
