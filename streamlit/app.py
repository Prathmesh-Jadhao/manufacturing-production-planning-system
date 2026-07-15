import requests
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Manufacturing Production Planning",
    page_icon="🏭",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("Manufacturing Production Planning System")

# -------------------------------
# Helper function
# -------------------------------
def get_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

# -------------------------------
# Load Data
# -------------------------------
products = get_data("products")
materials = get_data("materials")
plans = get_data("production-plans")
requirements = get_data("material-requirements")

# -------------------------------
# KPI Cards
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Products", len(products))
col2.metric("Materials", len(materials))
col3.metric("Production Plans", len(plans))
col4.metric("Material Requirements", len(requirements))

st.divider()

st.subheader("Operations")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run Production Planning", use_container_width=True):
        try:
            response = requests.post(f"{API_URL}/planning/run")
            response.raise_for_status()
            st.success(response.json()["message"])
            st.rerun()
        except Exception as e:
            st.error(e)

with col2:
    if st.button("📦 Run Material Requirement Planning", use_container_width=True):
        try:
            response = requests.post(f"{API_URL}/mrp/run")
            response.raise_for_status()
            st.success(response.json()["message"])
            st.rerun()
        except Exception as e:
            st.error(e)

st.divider()

st.subheader("Production Plans")

plans = get_data("production-plans")

if plans:
    df = pd.DataFrame(plans)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No production plans available.")

st.divider()

st.subheader("Material Requirements")

requirements = get_data("material-requirements")

if requirements:
    df = pd.DataFrame(requirements)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No material requirements available.")