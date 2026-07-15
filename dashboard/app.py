import streamlit as st
import pandas as pd
import requests

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Manufacturing Production Planning System",
    page_icon="🏭",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# -------------------------------
# API Helper
# -------------------------------
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Unable to fetch {endpoint}\n\n{e}")
        return []


# -------------------------------
# Load Data
# -------------------------------
plans = fetch_data("/production-plans")
mrp = fetch_data("/material-requirements")
products = fetch_data("/products")
materials = fetch_data("/materials")

plans_df = pd.DataFrame(plans)
mrp_df = pd.DataFrame(mrp)

# -------------------------------
# Header
# -------------------------------
st.title("🏭 Manufacturing Production Planning System")
st.markdown("""
Welcome to the production planning control center. This system manages product forecasting, capacity planning, 
Material Requirements Planning (MRP), and machine scheduling.

Use the sidebar navigation to explore detailed views.
""")
st.markdown("---")

# -------------------------------
# KPI Cards
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

total_products = len(products)

forecast_qty = (
    plans_df["forecast_qty"].sum()
    if not plans_df.empty else 0
)

planned_qty = (
    plans_df["planned_quantity"].sum()
    if not plans_df.empty else 0
)

avg_utilization = (
    plans_df["capacity_utilization"].mean()
    if not plans_df.empty else 0
)

col1.metric("Total Products", total_products)
col2.metric("Total Forecast Qty", f"{forecast_qty:,.0f} units")
col3.metric("Total Planned Qty", f"{planned_qty:,.0f} units")
col4.metric("Avg Capacity Utilization", f"{avg_utilization:.2f}%")

st.markdown("---")

# -------------------------------
# Sub-pages Overview Grid
# -------------------------------
st.subheader("System Modules")

col_a, col_b = st.columns(2)

with col_a:
    st.info("📅 **Production Planning**\n\nCompare demand forecasts with inventory levels and scheduled production. Track status flags and capacity utilization percentages per product family.")
    
    st.success("📦 **Material Requirements (MRP)**\n\nCalculate raw material quantities, evaluate safety inventory buffers, flag shortage amounts, and track purchase requirement statuses.")

with col_b:
    st.warning("💾 **Inventory Management**\n\nMonitor current finished product stocks against safety buffer thresholds and view warehouse locations for all raw material inventories.")
    
    st.error("📊 **Advanced Capacity & Analytics**\n\nReview detailed machine scheduling allocations, daily workloads, and overall machine capacity utilization schedules.")

st.markdown("---")

# Refresh button
if st.button("🔄 Refresh System Data"):
    st.rerun()