import os

import numpy as np
import sns
import tensorflow as tf
from sklearn.model_selection import cross_val_score, KFold
from tensorflow import keras
from tensorflow.keras import layers
from keras import optimizers
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score, classification_report

DATASET_PATH = "skinTone"
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 10
EPOCHS = 10

'''
    Load data from dataset
    This kaggle dataset already has train, validation, and test dataset split
'''


def convert_dataset_nparray(dataset):
    images = []
    labels = []
    for image, label in dataset:
        images.append(image.numpy())
        labels.append(label.numpy())
    return np.concatenate(images), np.concatenate(labels)


skin_tone_train = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/train",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)
skin_tone_val = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/valid",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)
skin_tone_test = tf.keras.utils.image_dataset_from_directory(
    f"{DATASET_PATH}/test",
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

class_names = skin_tone_train.class_names

'''
    Preprocess the data
    1. Normalize the data/pixel values
'''

normalization_layer = layers.Rescaling(1. / 255)
skin_tone_train = skin_tone_train.map(lambda x, y: (normalization_layer(x), y))
skin_tone_val = skin_tone_val.map(lambda x, y: (normalization_layer(x), y))
skin_tone_test = skin_tone_test.map(lambda x, y: (normalization_layer(x), y))

'''
    Create the CNN for skin tone classification
'''


def create_cnn(input_shape=IMAGE_SIZE + (3,), num_classes=len(class_names)):
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=input_shape),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(128, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(256, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax")
    ])
    lr_scheduler = keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate=0.001,
        decay_steps=1000,
        decay_rate=0.9
    )
    optimizer = optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
    model.compile(optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


skin_cnn_model = create_cnn()
history = skin_cnn_model.fit(skin_tone_train, validation_data=skin_tone_val, epochs=EPOCHS)

'''
    Plot Training Results
'''
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

'''
    Evaulate the model
'''

# Evaluate the model on the test dataset
test_loss, test_accuracy = skin_cnn_model.evaluate(skin_tone_test)

print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

skin_x_test, skin_y_test = convert_dataset_nparray(skin_tone_test)
y_prob = skin_cnn_model.predict(skin_x_test)
y_pred = np.argmax(y_prob, axis = 1)
cm = confusion_matrix(skin_y_test, y_pred)

plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.colorbar()
plt.show()

f1 = f1_score(skin_y_test, y_pred, average="weighted")  # Weighted F1-score
print(f"F1 Score (Weighted): {f1:.4f}")

print("\nClassification Report:\n", classification_report(skin_y_test, y_pred, target_names=class_names))

