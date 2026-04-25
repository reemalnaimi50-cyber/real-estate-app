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

# 📦 تحميل النموذج
models = {
    "Apartment Rent": "model_apartment_rent.pkl",
    "Apartment Sale": "model_apartment_sale.pkl",
    "House Rent": "model_house_rent.pkl",
    "House Sale": "model_house_sale.pkl",
    "Land Rent": "model_land_rent.pkl",
    "Land Sale": "model_land_sale.pkl",
}

model = joblib.load(models[property_type])

# 🧠 إدخال البيانات
data = {}

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

# 🏠 فترة الإيجار
if "Rent" in property_type:
    rent_choice = st.selectbox("Rent Period", ["Monthly", "6 Months", "Yearly"])
    rent_map = {"Monthly": 1, "6 Months": 6, "Yearly": 12}
    data["rent_period_num"] = rent_map[rent_choice]

# 🚀 التنبؤ
if st.button("Predict Price"):

    df = pd.DataFrame([data])
    df = pd.get_dummies(df)

    # تحميل الأعمدة الصحيحة
columns = joblib.load(property_type + "_columns.pkl")

df = pd.get_dummies(df)

# إضافة الأعمدة الناقصة
for col in columns:
    if col not in df.columns:
        df[col] = 0

# ترتيب الأعمدة
df = df[columns]

    pred = model.predict(df)

    price = np.exp(pred[0])

    st.success(f"Predicted Price: {price:,.0f} SAR")
