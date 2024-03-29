from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout, Flatten, MaxPooling2D, Conv2D
from keras.utils import np_utils
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing import image
import cv2
from glob import glob
import sys
from IPython.display import display
from PIL import Image
import matplotlib.pyplot as plt

# load (downloaded if needed) the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape((X_train.shape[0],28,28,1)).astype('float32')
X_test = X_test.reshape((X_test.shape[0],28,28,1)).astype('float32')
X_train = X_train / 255
X_test = X_test / 255

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

def larger_model():
	model = Sequential()
	model.add(Conv2D(30, (5, 5), input_shape=(28, 28,1), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(15, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
model=larger_model()

model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)
model.save('model.h5')

# Final evaluation of the models
scores = model.evaluate(X_test, y_test, verbose=0)
print("Error: %.2f%%" % (100-scores[1]*100))

print(model.predict(X_test))

image_index = 2444
plt.imshow(X_test[image_index].reshape(28, 28),cmap='Greys')
pred = model.predict(X_test[image_index].reshape(1, 28, 28, 1))
print(pred.argmax())