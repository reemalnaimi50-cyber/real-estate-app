import streamlit as st
import pandas as pd
import numpy as np
import joblib

# تحميل النموذج
model = joblib.load("real_estate_model.pkl")

# 🎨 إعداد الصفحة
st.set_page_config(page_title="Real Estate Predictor", layout="centered")

st.title("Real Estate Price Prediction System")
st.write("Enter property details to predict the estimated price")

st.markdown("---")

# 🏷️ نوع العقار
property_type = st.selectbox(
    "Property Type",
    [
        "Apartment Sale",
        "Apartment Rent",
        "House Sale",
        "House Rent",
        "Land Sale",
        "Land Rent"
    ]
)

# 🏙️ المدينة (بدون حي)
city = st.selectbox(
    "City",
    ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"]
)

# 📏 المساحة
area = st.number_input("Area (sqm)", min_value=0.0)

st.markdown("---")

# 🤖 زر التوقع
if st.button("Predict Price"):

    # تجهيز البيانات
    input_data = pd.DataFrame({
        "area": [area],
        "city": [city],
        "property_type": [property_type]
    })

    # تحويل البيانات إلى dummy variables
    input_data = pd.get_dummies(input_data)

    # توحيد الأعمدة مع النموذج
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    # التنبؤ
    prediction = model.predict(input_data)

    # إذا كنتِ مستخدمة log price
    price = np.exp(prediction[0])

    #  عرض النتيجة
    st.success(f"Estimated Price: {price:,.2f} SAR")

    st.balloons()
