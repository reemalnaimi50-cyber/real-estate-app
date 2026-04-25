import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("Real Estate Price Prediction")

property_type = st.selectbox("Select Property Type", [
    "Apartment Rent",
    "Apartment Sale",
    "House Rent",
    "House Sale",
    "Land Rent",
    "Land Sale"
])

safe = property_type.replace(" ", "_")

# تحميل الملفات
model = joblib.load(f"model_{safe.lower()}.pkl")
columns = joblib.load(f"{safe}_columns.pkl")

data = {}

# 🔥 أهم شيء: log_area
area = st.number_input("Area (sqm)", min_value=1.0)
data["log_area"] = np.log(area)

data["city"] = st.selectbox("City", ["الدمام", "الخبر", "الظهران", "الجبيل", "القطيف"])

if "Apartment" in property_type or "House" in property_type:
    data["beds"] = st.number_input("Beds", 0)
    data["livings"] = st.number_input("Living Rooms", 0)
    data["wc"] = st.number_input("Bathrooms", 0)

if "House" in property_type:
    data["street_width"] = st.number_input("Street Width", 0)

if "Apartment" in property_type:
    data["furnished"] = st.selectbox("Furnished", ["No", "Yes"])
    data["furnished"] = 1 if data["furnished"] == "Yes" else 0

if "Land" in property_type:
    data["street_width"] = st.number_input("Street Width", 0)
    data["distance_to_sea"] = st.number_input("Distance to Sea", 0.0)

if "Rent" in property_type:
    rent = st.selectbox("Rent Period", ["Monthly", "6 Months", "Yearly"])
    data["rent_period_num"] = {"Monthly": 1, "6 Months": 6, "Yearly": 12}[rent]

# 🚀 prediction
if st.button("Predict Price"):

    df = pd.DataFrame([data])
    df = pd.get_dummies(df)

    # 🔥 توحيد الأعمدة (الحل النهائي لمشكلتك)
    for col in columns:
        if col not in df.columns:
            df[col] = 0

    df = df[columns]

    pred = model.predict(df)
    price = np.exp(pred[0])

    st.success(f"Predicted Price: {price:,.0f} SAR")
