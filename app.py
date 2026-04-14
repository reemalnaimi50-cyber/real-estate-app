import streamlit as st

st.title("🏠 Real Estate Price Prediction")

area = st.number_input("Area (sqm)")
rooms = st.number_input("Number of Rooms")

if st.button("Predict"):
    price = 50000 + (area * 300) + (rooms * 10000)
    st.success(f"💰 Predicted Price: {price}")
