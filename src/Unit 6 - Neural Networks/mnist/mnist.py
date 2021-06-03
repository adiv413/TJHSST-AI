from tensorflow import keras
from keras.datasets import mnist, cifar10
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np

(train_x, train_y), (test_x, test_y) = mnist.load_data()

(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
# print(str(train_images.shape), str(train_labels.shape), str(test_images.shape), str(test_labels.shape))

# Normalize pixel values so that CNN will work
train_x = train_x / 255
test_x = test_x / 255
train_x = train_x[:, :, :, np.newaxis]
test_x = test_x[:, :, :, np.newaxis]
# print(str(train_x.shape), str(train_y.shape), str(test_x.shape), str(test_y.shape))

model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D())
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(32))
model.add(layers.Dense(10))
model.summary()
model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = model.fit(train_x, train_y, epochs=10, validation_data=(test_x, test_y))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(test_x, test_y, verbose=2)
print(test_acc)

