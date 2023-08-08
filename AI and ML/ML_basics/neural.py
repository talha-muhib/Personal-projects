import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

mist = tf.keras.datasets.mnist #Dataset of handwritten digits
(x_train, y_train), (x_test, y_test) = mist.load_data() #Splits the dataset into testing/training data (80/20 split)

x_train = tf.keras.utils.normalize(x_train, axis=1) #Normalizes or scales down the training data
x_test = tf.keras.utils.normalize(x_test, axis=1) 

model = tf.keras.models.Sequential() #Create a basic neural network
model.add(tf.keras.layers.Flatten(input_shape=(28,28))) #Add a flat layer (flattens a 128x128 pixel image)

#Add dense layers
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax)) #Output layer

#Compiling the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#Fit the model
model.fit(x_train, y_train, epochs=5) #Epochs just determines how many times the model sees the same data

#Evaluate the model
loss, accuracy = model.evaluate(x_test, y_test)

print(accuracy)
print(loss)

model.save('digits.model') #Saving the model so we can feed in our own handwritten digits


for i in range(1, 6):
    img = cv.imread(f'{i}.png')[:,:,0] #Using opencv to read the images we made
    img = np.invert(np.array([img])) #Inverting the array to have black on white for our images
    prediction = model.predict(img) #Predict on the image
    print(f'The result is probably {np.argmax(prediction)}')
    plt.imshow(img[0], cmap=plt.cm.binary) #Making the image colors black and white
    plt.show()