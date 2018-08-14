import os
import cv2
import numpy as np
import matplotlib.image as mpimg
from keras.models import load_model

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

n_0 = os.path.join(project_path, 'files/number_0.png')
n_1 = os.path.join(project_path, 'files/number_1.png')
n_2 = os.path.join(project_path, 'files/number_2.png')
n_3 = os.path.join(project_path, 'files/number_3.png')
n_4 = os.path.join(project_path, 'files/number_4.png')
n_5 = os.path.join(project_path, 'files/number_5.png')
n_6 = os.path.join(project_path, 'files/number_6.png')
n_7 = os.path.join(project_path, 'files/number_7.png')
n_8 = os.path.join(project_path, 'files/number_8.png')
n_9 = os.path.join(project_path, 'files/number_9.png')

numbers = [n_0, n_1, n_2, n_3, n_4, n_5, n_6, n_7, n_8, n_9]

images = []
labels = []
for i, num in enumerate(numbers):
    img = mpimg.imread(num)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = np.reshape(img, (1, -1))

    images.append(img)
    labels.append(i)

model = load_model(os.path.join(project_path, 'files/neuromatic_model.h5'))
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

num_correct = 0
for i, image in enumerate(images):
    prediction = model.predict_classes(image)[0]
    print('Label: {0} - Prediction: {1}'.format(labels[i], prediction))

    if prediction == labels[i]:
        num_correct += 1

print('\nModel accuracy: {0}'.format(num_correct / len(labels)))