import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Eeki Farms", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Data Entry")

@st.cache_resource
def get_gsheets():
    return st.connection("gsheets", type=GSheetsConnection)

conn = get_gsheets()

# TEST READ/WRITE FIRST
col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Test Read", type="secondary"):
        try:
            df = conn.read(worksheet="Sheet1", nrows=3)
            st.success("✅ CAN READ!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"READ ERROR: {e}")

with col2:
    if st.button("🧪 Test Write", type="secondary"):
        try:
            test_row = {"Test": "Hello", "Time": str(date.today())}
            existing = conn.read(worksheet="Sheet1")
            new_data = pd.concat([existing, pd.DataFrame([test_row])])
            conn.update(worksheet="Sheet1", data=new_data)
            st.success("✅ CAN WRITE!")
        except Exception as e:
            st.error(f"WRITE ERROR: {e}")

# MAIN FORM (only if tests pass)
st.subheader("📝 Data Entry Form")
col1, col2 = st.columns(2)

with col1:
    farm1 = st.text_input("Farm 1 *", placeholder="Required")
    loc1 = st.text_input("Location 1 *", placeholder="Required")
    vendor = st.text_input("Vendor *", placeholder="Required")

with col2:
    crop1 = st.text_input("Crop 1 *", placeholder="Required")
    qty1 = st.number_input("Quantity 1 (kg) *", min_value=0.01, format="%.2f")
    entry_date = st.date_input("Date", value=date.today())

if st.button("🚀 Submit Data", type="primary"):
    if all([farm1, loc1, crop1, vendor, qty1 > 0]):
        new_row = {
            "Farm": farm1, "Location1": loc1, "Crop1": crop1, "Quantity1": qty1,
            "Vendor": vendor, "Date": str(entry_date)
        }
        try:
            # APPEND PROPERLY
            existing = conn.read(worksheet="Sheet1")
            updated = pd.concat([existing, pd.DataFrame([new_row])], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated)
            st.success("✅ DATA SAVED!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Save failed: {str(e)}")
    else:
        st.error("Fill all * fields")

# SHOW DATA
if st.checkbox("📊 Show Sheet Data"):
    try:
        df = conn.read(worksheet="Sheet1")
        st.dataframe(df)
    except:
        st.warning("Can't show data")
