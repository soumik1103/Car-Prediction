import streamlit as st
import requests

# set_page_config() is used to configure the Streamlit page
# page_title -> browser tab title
# page_icon -> emoji/icon shown in tab
# layout="centered" -> keeps content centered on page
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

# IMPORTANT:
# This must be your FastAPI backend URL (Render API URL)
# NOT your Streamlit frontend URL
API_URL = "https://car-prediction-u2a6.onrender.com/predict"

# App heading
st.title("🚗 Car Price Prediction")

# Small description under title
st.caption(
    "This UI sends data to your FastAPI backend and shows predicted selling price."
)

# ---------------------------------------------------
# USER INPUTS
# These fields should match your ML model dataset columns
# ---------------------------------------------------

# Text input for car name
car_name = st.text_input(
    "Car_Name (e.g. swift, ritz, sx4)",
    value="swift"
)

# Number input for manufacturing year
year = st.number_input(
    "Year",
    min_value=1990,
    max_value=2026,
    value=2014,
    step=1
)

# Present price of car
present_price = st.number_input(
    "Present_Price (in lakhs)",
    min_value=0.0,
    value=5.59,
    step=0.1
)

# Total kilometers driven
kms_driven = st.number_input(
    "Kms_Driven",
    min_value=0,
    value=40000,
    step=1000
)

# Dropdown for fuel type
fuel_type = st.selectbox(
    "Fuel_Type",
    ["Petrol", "Diesel", "CNG"]
)

# Dropdown for seller type
seller_type = st.selectbox(
    "Seller_Type",
    ["Dealer", "Individual"]
)

# Dropdown for transmission type
transmission = st.selectbox(
    "Transmission",
    ["Manual", "Automatic"]
)

# Owner is numeric in dataset
# We show readable labels to user
owner_label = st.selectbox(
    "Owner",
    [
        "0 (First Owner)",
        "1 (Second Owner)",
        "3 (Third Owner)"
    ]
)

# Extract numeric owner value from selected text
# Example:
# "1 (Second Owner)" -> 1
owner = int(owner_label.split()[0])

# ---------------------------------------------------
# JSON PAYLOAD
# This data will be sent to FastAPI backend
# ---------------------------------------------------

payload = {
    "Car_Name": str(car_name),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

# Show payload on UI for debugging/testing
st.write("### Payload being sent:")
st.json(payload)

# ---------------------------------------------------
# PREDICT BUTTON
# ---------------------------------------------------

if st.button("Predict Price 💰"):

    try:
        # Sending POST request to FastAPI backend
        # json=payload automatically converts dict to JSON
        # timeout=20 means wait max 20 seconds
        res = requests.post(
            API_URL,
            json=payload,
            timeout=20
        )

        # If API call successful
        if res.status_code == 200:

            # Convert response JSON into Python dictionary
            data = res.json()

            # Get prediction value from API response
            # Your FastAPI returns:
            # {
            #   "prediction_price": 3.80
            # }
            pred = data.get("prediction_price")

            # If prediction key missing
            if pred is None:

                st.warning(
                    "API responded but prediction key not found."
                )

                st.write("Full API Response:")
                st.json(data)

            else:
                # Show prediction nicely
                st.success(
                    f"✅ Predicted Selling Price: ₹ {pred:.2f} lakhs"
                )

        else:
            # If API gives error response
            st.error(f"❌ API Error {res.status_code}")

            # Show full backend response
            st.code(res.text)

    except requests.exceptions.RequestException as e:

        # Handles:
        # timeout
        # connection errors
        # network issues
        st.error(
            "❌ Could not connect to FastAPI backend."
        )

        st.code(str(e))