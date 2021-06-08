from tensorflow import keras
from keras.datasets import mnist
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
f = open("weights.txt", "w")
(train_x, train_y), (test_x, test_y) = mnist.load_data()

# Flatten the training and testing data

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

# Create model
model = keras.Sequential()
model.add(keras.layers.Input(shape=train_x.shape))
model.add(keras.layers.Dense(512, activation='relu'))
model.add(keras.layers.Dense(10, activation='softmax'))
model.summary()

model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = model.fit(train_x, train_y, epochs=30, validation_data=(test_x, test_y))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(test_x, test_y, verbose=2)
model.save('mnist')
print('Testing accuracy:', test_acc)

for lay in model.layers:
    for i in lay.get_weights():
        f.write(str(i.tolist())[1:-1])
        f.write("\n")