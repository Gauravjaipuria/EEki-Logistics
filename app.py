import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Eeki Farms Data Entry", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Customer Data Entry")

# Form columns
col1, col2 = st.columns(2)
with col1:
    st.subheader("Farms & Locations")
    farm1 = st.text_input("Farm 1", placeholder="Enter Farm 1 name")
    farm2 = st.text_input("Farm 2")
    farm3 = st.text_input("Farm 3")
    farm4 = st.text_input("Farm 4")
    farm5 = st.text_input("Farm 5")
    loc1 = st.text_input("Location 1")
    loc2 = st.text_input("Location 2")

with col2:
    st.subheader("Crops & Quantities")
    crop1 = st.text_input("Crop 1")
    qty1 = st.number_input("Quantity Crop 1 (kg)", min_value=0.0, format="%.2f")
    crop2 = st.text_input("Crop 2")
    qty2 = st.number_input("Quantity Crop 2 (kg)", min_value=0.0, format="%.2f")

col3, col4, col5 = st.columns(3)
with col3:
    vendor = st.text_input("Vendor")
with col4:
    transport_cost = st.number_input("Transportation Cost (₹)", min_value=0.0, format="%.2f")
with col5:
    running_km = st.number_input("Running Km", min_value=0, step=1)

entry_date = st.date_input("Date", value=date.today())

if st.button("🚀 Submit to Google Sheets", type="primary"):
    if all([farm1, loc1, crop1, qty1 > 0, vendor]):  # Basic validation
        conn = st.connection("gsheets", type=GSheetsConnection)
        new_row = {
            "Farm": farm1, "Farm2": farm2, "Farm3": farm3, "Farm4": farm4, "Farm5": farm5,
            "Location1": loc1, "Location2": loc2,
            "Crop1": crop1, "Quantity1": qty1, "Crop2": crop2, "Quantity2": qty2,
            "Vendor": vendor, "Transportation_Cost": transport_cost, "Running_Km": running_km, "Date": entry_date
        }
        # Append row (use update for overwrite if needed)
        conn.update(worksheet="Sheet1", data=[new_row])  # Assumes first worksheet[web:23]
        st.success("✅ Data submitted to Google Sheet!")
        st.rerun()
    else:
        st.error("⚠️ Fill required fields: Farm1, Location1, Crop1+Qty, Vendor")

# View recent data (optional)
if st.checkbox("Show Recent Entries"):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Sheet1", nrows=10)
    st.dataframe(df, use_container_width=True)
