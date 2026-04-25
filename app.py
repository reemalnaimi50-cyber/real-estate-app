# 🏠 اختيار نوع العقار
property_type = st.selectbox("Select Property Type", [
    "Apartment Rent",
    "Apartment Sale",
    "House Rent",
    "House Sale",
    "Land Sale",
    "Land Rent"
])

# 📊 مدخلات حسب نوع العقار

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

elif "Apartment" in property_type:
    area = st.number_input("Area (sqm)", min_value=1.0)
    city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])
    beds = st.number_input("Beds", min_value=0)
    livings = st.number_input("Living Rooms", min_value=0)
    wc = st.number_input("Bathrooms", min_value=0)
    age = st.number_input("Property Age", min_value=0)
    furnished = st.selectbox("Furnished", [0, 1])

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "beds": beds,
        "livings": livings,
        "wc": wc,
        "age": age,
        "furnished": furnished
    }])

elif "House" in property_type:
    area = st.number_input("Area (sqm)", min_value=1.0)
    city = st.selectbox("City", ["Dammam", "Khobar", "Dhahran", "Jubail", "Qatif"])
    beds = st.number_input("Beds", min_value=0)
    livings = st.number_input("Living Rooms", min_value=0)
    wc = st.number_input("Bathrooms", min_value=0)
    age = st.number_input("Property Age", min_value=0)
    street_width = st.number_input("Street Width", min_value=0)

    input_data = pd.DataFrame([{
        "area": area,
        "city": city,
        "beds": beds,
        "livings": livings,
        "wc": wc,
        "age": age,
        "street_width": street_width
    }])
