import joblib
import scaler
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Constants
IMAGE_SIZE_CNN = (128, 128)
SKIN_CLASS_NAMES = ['Dark', 'Medium', 'Fair']
IMAGE_SIZE_RF = (128, 128)
IMAGE_SIZE_SVM = (64, 64)
RF_MODEL_PATH = "rf_model.pkl"
SVM_MODEL_PATH = "svm_multilabel.pkl"
RF_CLASS_NAMES = ['little acne', 'moderate acne', 'severe acne', 'no_acne']
skin_conditions = []


@st.cache_resource
def load_cnn_model():
    model = tf.keras.models.load_model("skin_tone_model.h5")
    return model

@st.cache_resource
def load_rf_model():
    return joblib.load(RF_MODEL_PATH)

@st.cache_resource
def load_svm_model():
    data = joblib.load(SVM_MODEL_PATH)
    return data['model'], data['class_names'], data['scaler']

def preprocess_for_cnn(cnn_image):
    cnn_image = cnn_image.resize(IMAGE_SIZE_CNN)
    cnn_image = np.array(cnn_image) / 255.0
    cnn_image = np.expand_dims(cnn_image, axis=0)
    return cnn_image


def preprocess_for_rf(rf_image):
    rf_image = rf_image.resize(IMAGE_SIZE_RF)
    rf_image = np.array(rf_image) / 255.0
    rf_image = rf_image.flatten().reshape(1, -1)
    return rf_image

def preprocess_for_svm(svm_image):
    svm_image = svm_image.convert("RGB")
    svm_image = svm_image.resize(IMAGE_SIZE_SVM)
    svm_image_arr = np.array(svm_image).astype(np.float32) / 255.0
    svm_flat = svm_image_arr.flatten().reshape(1, -1)
    return svm_flat


cnn_model = load_cnn_model()

rf_model = load_rf_model()

svm_model, svm_class_names, svm_scaler = load_svm_model()


st.title("🧴 Skin Detection")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    cnn_image_input = preprocess_for_cnn(image)

    prediction = cnn_model.predict(cnn_image_input)
    cnn_predicted_class = SKIN_CLASS_NAMES[np.argmax(prediction)]
    skin_conditions.append(np.argmax(prediction))

    rf_image_input = preprocess_for_rf(image)
    rf_predicted_class = RF_CLASS_NAMES[rf_model.predict(rf_image_input)[0]]
    skin_conditions.append(rf_model.predict(rf_image_input)[0])

    features = preprocess_for_svm(image)
    features_scaled = svm_scaler.transform(features)

    svm_prediction = svm_model.predict(features_scaled)[0]

    st.markdown(f"### 🧠 Skin Tone: `{cnn_predicted_class}`")
    st.markdown(f"### 🔍 Acne Level: `{rf_predicted_class.upper()}`")
    st.subheader("Other Skin Conditions:")
    for label, pred in zip(svm_class_names, svm_prediction):
        if label == 'acne':
            continue
        else:
            if pred == 1:
                emoji = "✅"
                skin_conditions.append(1)
            else:
                emoji = "❌"
                skin_conditions.append(0)
            st.markdown(f"- **{label}**: {emoji}")


st.title("Personalized Skincare Product Recommender")

product_type = st.selectbox("Which product category do you want a recommendation for?",
                            ["Cleanser", "Moisturizer", "Sunscreen", "Targeted Treatment",
                             "Night Treatment"])

if len(skin_conditions) > 0:
    skin_tone = skin_conditions[0]
    acne_severity = skin_conditions[1]
    dark_circles = skin_conditions[2]
    dark_spots = skin_conditions[3]
    dry_skin = skin_conditions[4]
    normal_skin = skin_conditions[5]
    oily_skin = skin_conditions[6]
    visible_pores = skin_conditions[7]
    wrinkles = skin_conditions[8]

    def recommend_cleanser():
        recs = []
        if oily_skin == 1 or acne_severity <= 2:
            recs.append("💧 *CeraVe Renewing SA Cleanser* – Salicylic acid for oil & acne")
        if dry_skin == 1:
            recs.append("🫧 *Vanicream Gentle Cleanser* – Non-stripping for dry skin")
        if normal_skin == 1:
            recs.append("🧴 *La Roche-Posay Toleriane* – Balanced for normal skin")
        return "\n\n".join(recs)


    def recommend_moisturizer():
        recs = []
        if oily_skin == 1:
            recs.append("💦 *Neutrogena Hydro Boost Gel Cream* – Lightweight hydration")
        if dry_skin == 1:
            recs.append("🧴 *CeraVe Moisturizing Cream* – Rich with ceramides & HA")
        if wrinkles == 1:
            recs.append("🌙 *Olay Regenerist Retinol 24* – Anti-aging peptide blend")
        if not recs:
            recs.append("✨ *Aveeno Daily Moisturizer* – Light and nourishing")
        return "\n\n".join(recs)


    def recommend_sunscreen():
        recs = []
        if skin_tone == 0:
            recs.append("🕶️ *Black Girl Sunscreen SPF 30* – No white cast, great for melanin-rich skin")
        if skin_tone == 1:
            recs.append("🌤️ *EltaMD UV Clear Tinted SPF 46* – Blends well & calms acne")
        if skin_tone == 2:
            recs.append("☀️ *La Roche-Posay Anthelios SPF 60* – Lightweight broad spectrum")
        return "\n\n".join(recs)


    def recommend_target():
        recommendations = []

        if acne_severity <= 2:
            recommendations.append("🔹 *PanOxyl 10% Benzoyl Peroxide Wash* – kills acne bacteria")
            recommendations.append("🧬 *The Ordinary Niacinamide 10% + Zinc 1%* – reduces sebum & redness")

        if dark_spots == 1:
            recommendations.append("🌟 *La Roche-Posay Vitamin C Serum* – evens out tone")
            recommendations.append("🧪 *The Ordinary Azelaic Acid 10%* – fights acne & hyperpigmentation")

        if dark_circles == 1:
            recommendations.append("👁️ *The Ordinary Caffeine Solution 5%* – reduces puffiness")

        if wrinkles == 1:
            recommendations.append("🧴 *Differin Gel (Adapalene)* – gentle retinoid for aging + acne")
            recommendations.append("🌙 *Olay Retinol 24 Serum* – improves fine lines")

        if visible_pores == 1:
            recommendations.append("🫧 *Paula’s Choice BHA Exfoliant* – unclogs & smooths skin")

        if not recommendations:
            return "👍 No specific concerns matched. Try a gentle Vitamin C or Niacinamide serum."

        return "\n\n".join(recommendations)


    def recommend_night():
        recs = []
        if acne_severity <= 2 or oily_skin == 1:
            recs.append("🌙 *Differin Adapalene Gel 0.1%* – targets acne & aging")
        if wrinkles == 1 and dry_skin == 1:
            recs.append("🧴 *Olay Retinol 24 Night Moisturizer* – hydration + anti-aging")
        if dark_spots == 1:
            recs.append("✨ *The Ordinary Alpha Arbutin 2% + HA* – fades pigmentation")
        if not recs:
            recs.append("🌃 Use a night cream with hyaluronic acid & peptides.")
        return "\n\n".join(recs)


    st.subheader("✅ Recommended Product(s):")
    if product_type == "Cleanser":
        st.markdown(recommend_cleanser())
    elif product_type == "Moisturizer":
        st.markdown(recommend_moisturizer())
    elif product_type == "Sunscreen":
        st.markdown(recommend_sunscreen())
    elif product_type == "Targeted Treatment":
        st.markdown(recommend_target())
    elif product_type == "Night Treatment":
        st.markdown(recommend_night())


