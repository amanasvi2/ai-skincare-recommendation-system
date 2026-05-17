import streamlit as st

acne = st.multiselect("Acne or No Acne", ["Acne", "No Acne"])
skin_tone = st.multiselect("Skin Tone", ["White", "Brown", "Black"])
oily = st.multiselect("Oily", ["Oily", "Not Oily"])

if "Acne" in acne and "White" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("The INKEY List Salicylic Acid Cleanser")
    st.image("images/The_INKEY_List_Salicylic_Acid_Cleanser.png", width=200)
    st.write("Glow Recipe Watermelon Pink Juice Oil-Free Moisturizer")
    st.image("images/Glow_Recipe_Watermelon_Pink_Juice_Oil-Free_Moisturizer.png", width=200)
    st.write("The Ordinary Niacinamide 10% + Zinc 1% Serum")
    st.image("images/The_Ordinary_Niacinamide_10_Zinc_1_Serum.png", width=200)

elif "Acne" in acne and "White" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Paula's Choice CLEAR Skin Starter Set")
    st.image("images/Paulas_Choice_CLEAR_Skin_Starter_Set.png", width=200)
    st.write("Tatcha The Rice Wash Skin-Softening Cleanser")
    st.image("images/Tatcha_The_Rice_Wash_Skin-Softening_Cleanser.png", width=200)
    st.write("The Ordinary Hyaluronic Acid 2% + B5 Serum")
    st.image("images/The_Ordinary_Hyaluronic_Acid_2_B5_Serum.png", width=200)

elif "Acne" in acne and "Brown" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Dr. Jart+ Teatreement Cleansing Foam")
    st.image("images/Dr_Jart_Teatreement_Cleansing_Foam.png", width=200)
    st.write("Supergoop! Unseen Sunscreen SPF 40")
    st.image("images/Supergoop_Unseen_Sunscreen_SPF_40.png", width=200)
    st.write("Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant")
    st.image("images/Paulas_Choice_Skin_Perfecting_2_BHA_Liquid_Exfoliant.png", width=200)

elif "Acne" in acne and "Brown" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Youth To The People Superfood Gentle Antioxidant Cleanser")
    st.image("images/Youth_To_The_People_Superfood_Gentle_Antioxidant_Cleanser.png", width=200)
    st.write("The INKEY List Retinol Serum")
    st.image("images/The_INKEY_List_Retinol_Serum.png", width=200)
    st.write("The INKEY List Omega Water Cream Oil-Free Moisturizer")
    st.image("images/The_INKEY_List_Omega_Water_Cream_Oil-Free_Moisturizer.png", width=200)

elif "Acne" in acne and "Black" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Clinique Charcoal Face Wash")
    st.image("images/Clinique_Charcoal_Face_Wash.png", width=200)
    st.write("Super Volcanic AHA Pore Clearing Clay Mask")
    st.image("images/Super_Volcanic_AHA_Pore_Clearing_Clay_Mask.png", width=200)
    st.write("Caudalie Vinosun Very High Protection Lightweight Cream SPF 50+")
    st.image("images/Caudalie_Vinosun_Very_High_Protection_Lightweight_Cream_SPF_50.png", width=200)

elif "Acne" in acne and "Black" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("The INKEY List Salicylic Acid Cleanser")
    st.image("images/The_INKEY_List_Salicylic_Acid_Cleanser.png", width=200)
    st.write("The INKEY List Omega Water Cream Oil-Free Moisturizer")
    st.image("images/The_INKEY_List_Omega_Water_Cream_Oil-Free_Moisturizer.png", width=200)
    st.write("The Ordinary Niacinamide 10% + Zinc 1% Serum")
    st.image("images/The_Ordinary_Niacinamide_10_Zinc_1_Serum.png", width=200)

elif "No Acne" in acne and "White" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Tatcha The Deep Cleanse Gentle Exfoliating Cleanser")
    st.image("images/Tatcha_The_Deep_Cleanse_Gentle_Exfoliating_Cleanser.png", width=200)
    st.write("Dr. Jart+ Teatreement Moisturizer")
    st.image("images/Dr_Jart_Teatreement_Moisturizer.png", width=200)
    st.write("Supergoop! Unseen Sunscreen SPF 40")
    st.image("images/Supergoop_Unseen_Sunscreen_SPF_40.png", width=200)

elif "No Acne" in acne and "White" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("First Aid Beauty Pure Skin Face Cleanser")
    st.image("images/First_Aid_Beauty_Pure_Skin_Face_Cleanser.png", width=200)
    st.write("First Aid Beauty Ultra Repair Cream Intense Hydration")
    st.image("images/First_Aid_Beauty_Ultra_Repair_Cream_Intense_Hydration.png", width=200)
    st.write("The Ordinary Vitamin C Suspension 23% + HA Spheres 2%")
    st.image("images/The_Ordinary_Vitamin_C_Suspension_23_HA_Spheres_2.png", width=200)

elif "No Acne" in acne and "Brown" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Youth To The People Superfood Gentle Antioxidant Cleanser")
    st.image("images/Youth_To_The_People_Superfood_Gentle_Antioxidant_Cleanser.png", width=200)
    st.write("The INKEY List Niacinamide Oil Control Serum")
    st.image("images/The_INKEY_List_Niacinamide_Oil_Control_Serum.png", width=200)

elif "No Acne" in acne and "Brown" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("First Aid Beauty Face Cleanser")
    st.image("images/First_Aid_Beauty_Pure_Skin_Face_Cleanser.png", width=200)
    st.write("Glow Recipe Plum Plump Hyaluronic Cream")
    st.image("images/Glow_Recipe_Plum_Plump_Hyaluronic_Cream.png", width=200)
    st.write("The Ordinary Ascorbyl Glucoside Solution 12%")
    st.image("images/The_Ordinary_Ascorbyl_Glucoside_Solution_12.png", width=200)

elif "No Acne" in acne and "Black" in skin_tone and "Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("Youth To The People Superfood Cleanser")
    st.image("images/Youth_To_The_People_Superfood_Gentle_Antioxidant_Cleanser.png", width=200)
    st.write("The INKEY List Niacinamide Oil Control Serum")
    st.image("images/The_INKEY_List_Niacinamide_Oil_Control_Serum.png", width=200)
    st.write("Supergoop! Unseen Sunscreen SPF 40")
    st.image("images/Supergoop_Unseen_Sunscreen_SPF_40.png", width=200)

elif "No Acne" in acne and "Black" in skin_tone and "Not Oily" in oily:
    st.write("**Recommended Products:**")
    st.write("First Aid Beauty Pure Skin Face Cleanser")
    st.image("images/First_Aid_Beauty_Pure_Skin_Face_Cleanser.png", width=200)
    st.write("First Aid Beauty Ultra Repair Cream Intense Hydration")
    st.image("images/First_Aid_Beauty_Ultra_Repair_Cream_Intense_Hydration.png", width=200)
    st.write("The Ordinary Vitamin C Suspension 23% + HA Spheres 2%")
    st.image("images/The_Ordinary_Vitamin_C_Suspension_23_HA_Spheres_2.png", width=200)
