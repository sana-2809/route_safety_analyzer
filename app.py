# app.py
import streamlit as st
from logic import calculate_safety
from osm_service import fetch_data

st.set_page_config(page_title="Area Safety Analyzer", layout="centered")

st.title("🌃 AI-based Area Safety Analyzer")
st.write("Estimate how safe a location is, especially for night-time travel.")

# User Inputs
place = st.text_input("Enter Place Name", placeholder="e.g., Downtown, New York")
time_of_day = st.radio("Select Time", ["Day", "Night"])

if st.button("Analyze"):
    if not place:
        st.warning("Please enter a place name.")
    else:
        with st.spinner("Fetching data from OpenStreetMap..."):
            counts = fetch_data(place)

        if counts is None:
            st.error("Could not find this place. Try a different name.")
        else:
            # Call scoring logic
            score, level, reasoning = calculate_safety(counts, time_of_day)

            # Display results
            st.subheader("Safety Analysis Result")
            st.metric("Safety Score", f"{score}/100")

            if level == "Safe":
                st.success(f"Level: {level}")
            elif level == "Moderate":
                st.warning(f"Level: {level}")
            else:
                st.error(f"Level: {level}")

            st.write("**Reasoning:**")
            st.write(reasoning)
