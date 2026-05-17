import os
import pickle

import numpy as np
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
from tensorflow.keras.utils import image_dataset_from_directory
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Constants
DATASET_PATH = "acne_split"
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32

train_ds = image_dataset_from_directory(f"{DATASET_PATH}/train", image_size=IMAGE_SIZE, batch_size=BATCH_SIZE, shuffle=False)
val_ds = image_dataset_from_directory(f"{DATASET_PATH}/val", image_size=IMAGE_SIZE, batch_size=BATCH_SIZE, shuffle=False)
test_ds = image_dataset_from_directory(f"{DATASET_PATH}/test", image_size=IMAGE_SIZE, batch_size=BATCH_SIZE, shuffle=False)

class_names = train_ds.class_names
print("Class Names:", class_names)

def convert_dataset_nparray(dataset):
    images = []
    labels = []
    for image, label in dataset:
        images.append(image.numpy())
        labels.append(label.numpy())
    return np.concatenate(images), np.concatenate(labels)

# pre-processing method
def flatten_dataset(dataset):
    images = []
    labels = []
    for img_batch, label_batch in dataset:
        img_batch = img_batch.numpy() / 255.0
        labels.extend(label_batch.numpy())
        images.extend(img_batch)
    images = np.array(images)
    images_flat = images.reshape(images.shape[0], -1)
    return images_flat, np.array(labels)

X_train, y_train = flatten_dataset(train_ds)
X_val, y_val = flatten_dataset(val_ds)
X_test, y_test = flatten_dataset(test_ds)

X_combined = np.concatenate([X_train, X_val])
y_combined = np.concatenate([y_train, y_val])

#{'max_depth': 19, 'n_estimators': 429}

rf_model = RandomForestClassifier(n_estimators=429, max_depth=19)
rf_model.fit(X_combined, y_combined)
pickle.dump(rf_model, open("rf_model.pkl", "wb"))


# Predict on test
y_pred = rf_model.predict(X_test)

# Evaluation
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=class_names))
print("F1 Score (weighted):", f1_score(y_test, y_pred, average="weighted"))
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)