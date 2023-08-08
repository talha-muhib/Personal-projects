import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import tensorflow as tf
from tensorflow.python.keras import models, layers

#Grabbing the cifar10 dataset from the keras library
cifar10 = tf.keras.datasets.cifar10

#Return testing and training data from th cifar10 dataset
(training_images, training_labels), (testing_images, testing_labels) = cifar10.load_data()

#Normalize the training and testing images (Pixels are activiated between 0 to 255)
training_images, testing_images = training_images / 255, testing_images / 255

#Assigning names to our labels (Since the labels in the dataset are just numbers)
class_names = ['Plane', 'Car', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']

#Now we're going to visualize 16 of our images
for i in range(16):
    plt.subplot(4, 4, i + 1) #Create a 4x4 grid and fill each slot

    #This is for not including coordinates since we don't care about that here
    plt.xticks([])
    plt.yticks([])

    #Show the i-th image in binary colormap (black and white)
    plt.imshow(training_images[i], cmap=plt.cm.binary)

    #Below each image we'll have a label of the corresponding image
    plt.xlabel(class_names[training_labels[i][0]])

#Show our plot
plt.show()

#Reduce the number of training images and labels we feed into our neural network (20,000)
training_images = training_images[:20000]
training_labels = training_labels[:20000]

#Reduce the number of testing images and labels we feed into our neural network (4,000)
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]

"""
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))

loss, accuracy = model.evaluate(testing_images, testing_labels)
print(f"Loss: {loss}")
print(f"Accuracy: {accuracy}")

model.save('image_classifier.model')
"""