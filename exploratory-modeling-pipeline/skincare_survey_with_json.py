
import streamlit as st
import json

st.set_page_config(page_title="Personalized Skincare Survey", layout="centered")

st.title("Personalized Skincare Survey")
st.markdown("Help us understand your skin better so we can recommend the best products for you!")

# 1. Demographic Info
st.header("Basic Information")

age = st.slider("What is your age?", 10, 80, 25)
gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
ethnicity = st.selectbox("Ethnicity", [
    "Asian", "Black/African descent", "Hispanic/Latinx", 
    "Middle Eastern", "White/Caucasian", "Mixed", "Other"
])

# 2. Skincare Routine
st.header("Current Skincare Routine")

products_used = st.multiselect(
    "Which of the following products do you use regularly?",
    ["Cleanser", "Moisturizer", "Sunscreen", "Exfoliant", "Toner", "Face Oil", "Serum", "Spot Treatment"]
)

actives = st.multiselect(
    "Do you currently use any of the following active ingredients?",
    ["Retinol", "Vitamin C", "Niacinamide", "AHAs/BHAs", "Hyaluronic Acid", "Peptides", "None"]
)

usage_frequency = st.radio(
    "How often do you use your skincare routine?",
    ["Daily", "A few times a week", "Occasionally", "Rarely"]
)

# 3. Skin Concerns
st.header("Skin Concerns")

concerns = st.multiselect(
    "What are your top 3 skin concerns?",
    ["Acne", "Dullness", "Dark Spots", "Redness", "Dry Patches", 
     "Oily Skin", "Wrinkles/Fine Lines", "Uneven Texture", "Dark Circles"]
)

# 4. Allergies
st.header("Sensitivities and Allergies")

sensitive_to = st.multiselect(
    "Are you sensitive or allergic to any of the following?",
    ["Fragrance", "Alcohol", "Essential Oils", "Parabens", "Sulfates", "None"]
)

# 5. Environment & Lifestyle
st.header("Environment & Lifestyle")

climate = st.selectbox("What's your usual environment like?", ["Humid", "Dry", "Cold", "Moderate", "Polluted"])
makeup = st.radio("Do you wear makeup regularly?", ["Yes", "No"])
hydration = st.slider("How many cups of water do you drink per day?", 0, 12, 6)
sleep = st.slider("How many hours do you sleep per night?", 0, 12, 7)
exercise = st.radio("How often do you exercise?", ["Daily", "Few times a week", "Rarely", "Never"])

# 6. Medical Info
st.header("Medical Info")

conditions = st.multiselect(
    "Do you have any diagnosed skin conditions?",
    ["Eczema", "Rosacea", "Psoriasis", "PCOS", "None"]
)

medications = st.text_input("Are you on any medications that affect your skin?", placeholder="e.g., Accutane, birth control")

# 7. Preferences
st.header("Preferences")

budget = st.radio("What's your monthly skincare budget?", ["<$20", "$20–50", "$50–100", "$100+"])
preferences = st.multiselect("What are your product preferences?", ["Fragrance-free", "Vegan", "Cruelty-free", "Clean beauty", "Derm-recommended"])

# Submission
st.header("Ready to Submit?")
if st.button("Submit"):
    st.success("Thanks for submitting your skincare profile!")
    user_data = {
        "age": age,
        "gender": gender,
        "ethnicity": ethnicity,
        "products_used": products_used,
        "actives": actives,
        "usage_frequency": usage_frequency,
        "concerns": concerns,
        "sensitive_to": sensitive_to,
        "climate": climate,
        "makeup": makeup,
        "hydration": hydration,
        "sleep": sleep,
        "exercise": exercise,
        "conditions": conditions,
        "medications": medications,
        "budget": budget,
        "preferences": preferences
    }
    st.json(user_data)
    
    with open("user_survey_data.json", "w") as f:
        json.dump(user_data, f, indent=4)
