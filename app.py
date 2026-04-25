import streamlit as st
import pandas as pd
import numpy as np
import joblib

# تحميل النموذج
model = joblib.load("real_estate_model.pkl")

st.title("Real Estate Price Prediction")

st.write("Enter property details below:")

# المدخلات
area = st.number_input("Area (sqm)")
city = st.text_input("City")
district = st.text_input("District")

# زر التنبؤ
if st.button("Predict Price"):

    # تجهيز البيانات
    input_data = pd.DataFrame({
        "area": [area],
        "city": [city],
        "district": [district]
    })

    # تحويل البيانات
    input_data = pd.get_dummies(input_data)

    # توحيد الأعمدة مع التدريب
    input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

    # التنبؤ
    log_price = model.predict(input_data)

    price = np.exp(log_price[0])

    st.success(f"Predicted Price: {price:,.2f} SAR")
