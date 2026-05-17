import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
import mediapipe as mp

# === Mediapipe Setup ===
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)
drawing_utils = mp.solutions.drawing_utils
drawing_spec = drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

# === Utility Functions ===
def apply_clahe_rgb(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

def normalize_color(image):
    return cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# === Extract Color Features from Carefully Selected Face Skin Landmarks ===
def extract_skin_color_features(image):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if not results.multi_face_landmarks:
        return np.zeros(6), None

    h, w, _ = image.shape
    face_landmarks = results.multi_face_landmarks[0]

    skin_ids = [10, 152, 234, 454, 93, 132, 361, 288, 127, 356, 162, 389]
    skin_pixels = []
    debug_image = image.copy()

    for idx in skin_ids:
        lm = face_landmarks.landmark[idx]
        x, y = int(lm.x * w), int(lm.y * h)
        if 0 <= x < w and 0 <= y < h:
            patch = image[max(y-1,0):min(y+2,h), max(x-1,0):min(x+2,w)]
            for px in patch.reshape(-1, 3):
                skin_pixels.append(px)
            cv2.circle(debug_image, (x, y), 2, (0, 255, 0), -1)

    if not skin_pixels:
        return np.zeros(6), debug_image

    pixels = np.array(skin_pixels)
    lab = cv2.cvtColor(pixels.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_BGR2LAB).reshape(-1, 3)
    l_vals, a_vals, b_vals = lab[:, 0], lab[:, 1], lab[:, 2]

    return np.array([
        np.median(l_vals), np.median(a_vals), np.median(b_vals),
        np.std(l_vals), np.std(a_vals), np.std(b_vals)
    ]), debug_image

# === Dataset Loading ===
def load_images_from_folder(folder):
    features, labels = [], []
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
                        img = cv2.resize(img, (100, 100))
                        img = apply_clahe_rgb(img)
                        img = normalize_color(img)
                        feature, _ = extract_skin_color_features(img)
                        features.append(feature)
                        labels.append(label)
    return np.array(features), np.array(labels), label_dict

# === Model Training ===
train_features, train_labels, label_map = load_images_from_folder('skinTone/train')

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95)),
    ('clf', RandomForestClassifier(random_state=42))
])

param_grid = {
    'clf__n_estimators': [100, 200, 300, 400],
    'clf__max_depth': [None, 10, 20, 30, 50],
    'clf__min_samples_split': [2, 3, 4, 5]
}

grid = GridSearchCV(pipeline, param_grid, cv=10, scoring='accuracy')
grid.fit(train_features, train_labels)
model = grid.best_estimator_

cv_accuracy = cross_val_score(model, train_features, train_labels, cv=10).mean()

# === Streamlit UI ===
st.title("\U0001F308 Skin Tone Classification App")
st.write(f"\U0001F4CA Model Accuracy (cross-validated): **{cv_accuracy:.2f}**")

uploaded_image = st.file_uploader("\U0001F4F8 Upload a clear image of your face (no filters or heavy makeup).", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    img = Image.open(uploaded_image)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    resized = cv2.resize(img, (100, 100))
    resized = apply_clahe_rgb(resized)
    resized = normalize_color(resized)

    features, debug_image = extract_skin_color_features(resized)
    probs = model.predict_proba(features.reshape(1, -1))[0]
    prediction = np.argmax(probs)

    sorted_indices = np.argsort(probs)[::-1]
    top_idx, second_idx = sorted_indices[0], sorted_indices[1]
    if probs[top_idx] < 0.6 and probs[second_idx] > 0.3:
        prediction = second_idx

    tone_map = {0: "Fair", 1: "Medium", 2: "Dark"}
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Uploaded Image", use_container_width=True)
    if debug_image is not None:
        st.image(cv2.cvtColor(debug_image, cv2.COLOR_BGR2RGB), caption="Skin Landmark Points Used", use_container_width=True)

    st.write(f"\U0001F9D1‍⚕️ Predicted Skin Tone: **{tone_map[prediction]}**")

    st.write("\U0001F522 Confidence for each class:")
    for tone, idx in label_map.items():
        st.write(f" {tone}: {probs[idx]*100:.2f}%")

    if probs[prediction] < 0.6:
        st.warning("⚠️ Low confidence prediction — result may be between tones.")

    st.write(f"Raw prediction index: {prediction}")
    st.write(f"Label map: {label_map}")
