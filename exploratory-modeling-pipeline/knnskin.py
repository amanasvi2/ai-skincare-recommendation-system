import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def load_images_from_folder(folder):
    images = []
    labels = []
    label_dict = {'White': 0, 'Brown': 1, 'Black': 2}
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            label = label_dict[subfolder]
            for filename in os.listdir(subfolder_path):
                image_path = os.path.join(subfolder_path, filename)
                if os.path.isfile(image_path):
                    img = cv2.imread(image_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (100, 100))
                        images.append(img)
                        labels.append(label)
    return np.array(images), np.array(labels), label_dict

def preprocess_images(images):
    return (images.reshape(images.shape[0], -1)) / 255.0

def euclidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

def knn_predict(train_data, train_labels, test_image, k):
    distances = []
    for i in range(len(train_data)):
        dist = euclidean_distance(test_image, train_data[i])
        distances.append((dist, train_labels[i]))
    distances.sort()
    count = {}
    for distance, label in distances[:k]:
        if label in count:
            count[label] += 1
        else:
            count[label] = 1
    most_common = None
    max_count = 0
    for label, num in count.items():
        if num > max_count:
            most_common = label
            max_count = num
    return most_common

def knn_model(train_data, train_labels, test_data, k):
    predictions = []
    for i in range(len(test_data)):
        pred = knn_predict(train_data, train_labels, test_data[i], k)
        predictions.append(pred)
    return np.array(predictions)

train_images, train_labels, label_map = load_images_from_folder('skinTone/train')
preprocessed_images = preprocess_images(train_images)

test_images, test_labels, _ = load_images_from_folder('skinTone/valid')
preprocessed_test_images = preprocess_images(test_images)

k = 100
test_predictions = knn_model(preprocessed_images, train_labels, preprocessed_test_images, k)

acc = accuracy_score(test_labels, test_predictions)
f1 = f1_score(test_labels, test_predictions, average='weighted')
cm = confusion_matrix(test_labels, test_predictions)

st.title("Skin Tone Classification")

st.subheader("Model Evaluation (on Validation Set)")
st.write(f"**Accuracy:** {acc:.2f}")
st.write(f"**F1 Score (weighted):** {f1:.2f}")

st.write("**Confusion Matrix:**")
fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_map.keys(),
            yticklabels=label_map.keys(),
            ax=ax)
plt.xlabel("Predicted")
plt.ylabel("True")
st.pyplot(fig)

uploaded_image = st.file_uploader("Upload a high-quality image that shows only your face.", type=["jpg", "jpeg", "png"])
if uploaded_image is not None:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (100, 100))
    preprocessed_img = (img.flatten().reshape(1, -1)) / 255.0
    prediction = knn_model(preprocessed_images, train_labels, preprocessed_img, k)
    skin_tone = None
    if prediction == 0:
        skin_tone = "White"
    elif prediction == 1:
        skin_tone = "Brown"
    elif prediction == 2:
        skin_tone = "Black"
    st.subheader(f"Predicted Skin Tone: {skin_tone}")
