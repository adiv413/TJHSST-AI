from tensorflow import keras
from keras.datasets import mnist
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

(train_x, train_y), (test_x, test_y) = mnist.load_data()
# print(train_x.shape)

new_train_x = []
for sample in train_x:
    to_add = []

    for row in sample:
        for pixel in row:
            to_add.append(pixel)

    new_train_x.append(np.array(to_add))

train_x = np.array(new_train_x)

new_test_x = []
for sample in test_x:
    to_add = []

    for row in sample:
        for pixel in row:
            to_add.append(pixel)

    new_test_x.append(np.array(to_add))

test_x = np.array(new_test_x)

# train_x.reshape(train_x.shape[0], (train_x.shape[1]*train_x.shape[2]))
# test_x.reshape(test_x.shape[0], (test_x.shape[1]*test_x.shape[2]))
# print(train_x.shape)
# train_x = train_x.reshape(60000, -1)
# test_x = test_x.reshape(60000, -1)
# Normalize pixel values so that CNN will work
# train_x = train_x / 255
# test_x = test_x / 255

# Reshape data to add an extra dimension
# train_x = train_x[:, :, :, np.newaxis]
# test_x = test_x[:, :, :, np.newaxis]

# Create model
model = keras.Sequential()
# model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)))
# model.add(layers.MaxPooling2D())
# model.add(layers.Conv2D(32, (3, 3), activation='relu'))
# model.add(layers.Flatten())
# model.add(layers.Dense(32))
# model.add(layers.Dense(10))
model.add(keras.layers.Input(shape=train_x.shape))
# model.add(keras.layers.Flatten())
# model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(512, activation='relu'))
# model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(10, activation='softmax'))
model.summary()
model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = model.fit(train_x, train_y, epochs=20, validation_data=(test_x, test_y))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(test_x, test_y, verbose=2)
model.save("mnist")
print(test_acc)

