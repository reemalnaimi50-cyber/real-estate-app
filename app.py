import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.title("Real Estate Price Prediction")

# 🏠 اختيار النوع
property_type = st.selectbox("Select Property Type", [
    "Apartment Rent",
    "Apartment Sale",
    "House Rent",
    "House Sale",
    "Land Rent",
    "Land Sale"
])

safe_name = property_type.replace(" ", "_")

# 📦 تحميل النموذج + الأعمدة
model = joblib.load(f"model_{safe_name.lower()}.pkl")
columns = joblib.load(f"{safe_name}_columns.pkl")

# 🧠 إدخال البيانات
data = {}

# 📏 المساحة (مهم: log)
area = st.number_input("Area (sqm)", min_value=1.0)
data["log_area"] = np.log(area)

data["city"] = st.selectbox("City", ["الدمام", "الخبر", "الظهران", "الجبيل", "القطيف"])

# 🏠 شقق وبيوت
if "Apartment" in property_type or "House" in property_type:
    data["beds"] = st.number_input("Beds", min_value=0)
    data["livings"] = st.number_input("Living Rooms", min_value=0)
    data["wc"] = st.number_input("Bathrooms", min_value=0)

# 🏡 بيت
if "House" in property_type:
    data["street_width"] = st.number_input("Street Width", min_value=0)

# 🏢 شقة
if "Apartment" in property_type:
    furnished = st.selectbox("Furnished", ["No", "Yes"])
    data["furnished"] = 1 if furnished == "Yes" else 0

# 🌊 أرض
if "Land" in property_type:
    data["street_width"] = st.number_input("Street Width", min_value=0)
    data["distance_to_sea"] = st.number_input("Distance to Sea", min_value=0.0)

# 🏠 الإيجار
if "Rent" in property_type:
    rent_choice = st.selectbox("Rent Period", ["Monthly", "6 Months", "Yearly"])
    rent_map = {"Monthly": 1, "6 Months": 6, "Yearly": 12}
    data["rent_period_num"] = rent_map[rent_choice]

# 🚀 prediction
if st.button("Predict Price"):

    df = pd.DataFrame([data])
    df = pd.get_dummies(df)

    # 🔥 توحيد الأعمدة (مهم جدًا)
    for col in columns:
        if col not in df.columns:
            df[col] = 0

    df = df[columns]

    pred = model.predict(df)

    price = np.exp(pred[0])

    st.success(f"Predicted Price: {price:,.0f} SAR")
