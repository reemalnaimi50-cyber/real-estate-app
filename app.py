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
    "Land Rent",
    "Land Sale"
])

# 📦 تحميل النموذج
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


# 🧠 المدخلات
input_data = pd.DataFrame()

# 🟢 Land
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

# 🟡 Apartment
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

# 🔵 House
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


# 🚀 التنبؤ
if st.button("Predict Price"):

    try:
        prediction = model.predict(input_data)
        price = np.exp(prediction[0])

        st.success(f"Predicted Price: {price:,.0f} SAR")

    except Exception as e:
        st.error("Error in prediction. Check model or inputs.")
        st.write(str(e))
