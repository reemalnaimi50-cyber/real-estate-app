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

# 📊 المدخلات الأساسية
area = st.number_input("Area (sqm)", min_value=1.0)
city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])

# 👇 مدخلات إضافية (لبعض الأنواع)
beds = st.number_input("Beds", min_value=0)
livings = st.number_input("Living Rooms", min_value=0)
wc = st.number_input("Bathrooms", min_value=0)
age = st.number_input("Property Age", min_value=0)
street_width = st.number_input("Street Width", min_value=0)
furnished = st.selectbox("Furnished", [0, 1])
ketchen = st.selectbox("Kitchen", [0, 1])
distance_to_sea = st.number_input("Distance to Sea", min_value=0.0)

# 📦 تحميل النموذج حسب الاختيار
if property_type == "Apartment Rent":
    model = joblib.load("model_apartment_rent.pkl")

elif property_type == "Apartment Sale":
    model = joblib.load("model_apartment_sale.pkl")

elif property_type == "House Rent":
    model = joblib.load("model_house_rent.pkl")

elif property_type == "House Sale":
    model = joblib.load("model_house_sale.pkl")

elif property_type == "Land Sale":
    model = joblib.load("model_land_sale.pkl")

elif property_type == "Land Rent":
    model = joblib.load("model_land_rent.pkl")

# 🚀 التنبؤ
if st.button("Predict Price"):

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "beds": beds,
        "livings": livings,
        "wc": wc,
        "age": age,
        "street_width": street_width,
        "furnished": furnished,
        "ketchen": ketchen,
        "distance_to_sea": distance_to_sea
    }])

    # تحويل النصوص إلى أرقام
    input_data = pd.get_dummies(input_data)

    # التنبؤ
    prediction = model.predict(input_data)

    # إذا استخدمتي log
    price = np.exp(prediction[0])

    st.success(f"Predicted Price: {price:,.0f} SAR")
