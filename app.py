import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("Real Estate Price Prediction")

# 🏠 نوع العقار
property_type = st.selectbox("Select Property Type", [
    "Apartment Rent",
    "Apartment Sale",
    "House Rent",
    "House Sale",
    "Land Rent",
    "Land Sale"
])

# 📦 تحميل النموذج
try:
    if property_type == "Apartment Rent":
        model = joblib.load("model_apartment_rent.pkl")

    elif property_type == "Apartment Sale":
        model = joblib.load("model_apartment_sale2.pkl")

    elif property_type == "House Rent":
        model = joblib.load("model_house_rent.pkl")

    elif property_type == "House Sale":
        model = joblib.load("model_house_sale3.pkl")

    elif property_type == "Land Rent":
        model = joblib.load("model_land_rent.pkl")

    elif property_type == "Land Sale":
        model = joblib.load("model_land_sale3.pkl")

except:
    st.error("Model file not found. Check GitHub upload.")
    st.stop()


# 🧠 إدخال البيانات
input_dict = {}

# 🟢 Land
if "Land" in property_type:
    input_dict["area"] = st.number_input("Area (sqm)", min_value=1.0)
    input_dict["city"] = st.selectbox("City", ["الدمام", "الخبر", "الظهران", "الجبيل", "القطيف"])
    input_dict["street_width"] = st.number_input("Street Width", min_value=0)
    input_dict["distance_to_sea"] = st.number_input("Distance to Sea", min_value=0.0)

# 🟡 Apartment
elif "Apartment" in property_type:
    input_dict["area"] = st.number_input("Area (sqm)", min_value=1.0)
    input_dict["city"] = st.selectbox("City", ["الدمام", "الخبر", "الظهران", "الجبيل", "القطيف"])
    input_dict["beds"] = st.number_input("Beds", min_value=0)
    input_dict["livings"] = st.number_input("Living Rooms", min_value=0)
    input_dict["wc"] = st.number_input("Bathrooms", min_value=0)

    furnished = st.selectbox("Furnishing", ["Not Furnished", "Furnished"])
    input_dict["furnished"] = 1 if furnished == "Furnished" else 0

    if "Rent" in property_type:
        input_dict["rent_period"] = st.selectbox("Rent Period", ["Monthly", "Quarterly", "Yearly"])

# 🔵 House
elif "House" in property_type:
    input_dict["area"] = st.number_input("Area (sqm)", min_value=1.0)
    input_dict["city"] = st.selectbox("City", ["الدمام", "الخبر", "الظهران", "الجبيل", "القطيف"])
    input_dict["beds"] = st.number_input("Beds", min_value=0)
    input_dict["livings"] = st.number_input("Living Rooms", min_value=0)
    input_dict["wc"] = st.number_input("Bathrooms", min_value=0)
    input_dict["street_width"] = st.number_input("Street Width", min_value=0)


# 🚀 التنبؤ
if st.button("Predict Price"):

    try:
        input_data = pd.DataFrame([input_dict])

        # One-hot encoding
        input_data = pd.get_dummies(input_data)

        # 🔥 أهم خطوة لحل مشكلة الأعمدة
        input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

        prediction = model.predict(input_data)

        price = np.exp(prediction[0])

        st.success(f"Predicted Price: {price:,.0f} SAR")

    except Exception as e:
        st.error("Prediction error")
        st.write(str(e))
