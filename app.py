import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("Real Estate Price Prediction")

# 🏠 اختيار نوع العقار
property_type = st.selectbox("Select Property Type", [
    "Apartment Rent",
    "Apartment Sale",
    "House Rent",
    "House Sale",
    "Land Sale",
    "Land Rent"
])

# 📦 تحميل النموذج حسب النوع

if property_type == "Apartment Rent":
    model = joblib.load("model_apartment_rent.pkl")

elif property_type == "Apartment Sale":

    model_version = st.selectbox("Select Model Version", [
        "Model 1",
        "Model 2"
    ])

    if model_version == "Model 1":
        model = joblib.load("model_apartment_sale.pkl")
    else:
        model = joblib.load("model_apartment_sale2.pkl")

elif property_type == "House Rent":
    model = joblib.load("model_house_rent.pkl")

elif property_type == "House Sale":
    model = joblib.load("model_house_sale3.pkl")

elif property_type == "Land Sale":
    model = joblib.load("model_land_sale3.pkl")

elif property_type == "Land Rent":
    model = joblib.load("model_land_rent.pkl")


# 🧠 المدخلات حسب نوع العقار

# 🟢 الأراضي
if "Land" in property_type:

    area = st.number_input("Area (sqm)", min_value=1.0)
    city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])
    street_width = st.number_input("Street Width", min_value=0)
    distance_to_sea = st.number_input("Distance to Sea", min_value=0.0)

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "street_width": street_width,
        "distance_to_sea": distance_to_sea
    }])


# 🟡 الشقق
elif "Apartment" in property_type:

    area = st.number_input("Area (sqm)", min_value=1.0)
    city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])
    beds = st.number_input("Beds", min_value=0)
    livings = st.number_input("Living Rooms", min_value=0)
    wc = st.number_input("Bathrooms", min_value=0)
    furnished = st.selectbox("Furnished", [0, 1])

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "beds": beds,
        "livings": livings,
        "wc": wc,
        "furnished": furnished
    }])


# 🔵 البيوت
elif "House" in property_type:

    area = st.number_input("Area (sqm)", min_value=1.0)
    city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])
    beds = st.number_input("Beds", min_value=0)
    livings = st.number_input("Living Rooms", min_value=0)
    wc = st.number_input("Bathrooms", min_value=0)
    street_width = st.number_input("Street Width", min_value=0)

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "beds": beds,
        "livings": livings,
        "wc": wc,
        "street_width": street_width
    }])


# 🚀 زر التنبؤ
if st.button("Predict Price"):

    input_data = pd.get_dummies(input_data)

    prediction = model.predict(input_data)

    price = np.exp(prediction[0])  # إذا استخدمتي log

    st.success(f"Predicted Price: {price:,.0f} SAR")
