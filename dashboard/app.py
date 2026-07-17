import streamlit as st
import pandas as pd

from helpers import fetch_data

# Page Configuration
st.set_page_config(
    page_title="Manufacturing Production Planning System",
    page_icon="\U0001f3ed",
    layout="wide",
)

# Header
st.title("\U0001f3ed Manufacturing Production Planning System")
st.markdown(
    "Welcome to the production planning control center. This system manages "
    "product forecasting, capacity planning, Material Requirements Planning (MRP), "
    "and machine scheduling.\n\n"
    "Use the sidebar navigation to explore detailed views."
)
st.markdown("---")

# Load Data
plans = fetch_data("/production-plans/")
products = fetch_data("/products/")

plans_df = pd.DataFrame(plans)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

total_products = len(products)
forecast_qty = plans_df["forecast_qty"].sum() if not plans_df.empty else 0
planned_qty = plans_df["planned_quantity"].sum() if not plans_df.empty else 0
avg_utilization = (
    plans_df["capacity_utilization"].mean() if not plans_df.empty else 0
)

col1.metric("Total Products", total_products)
col2.metric("Total Forecast Qty", f"{forecast_qty:,.0f} units")
col3.metric("Total Planned Qty", f"{planned_qty:,.0f} units")
col4.metric("Avg Capacity Utilization", f"{avg_utilization:.2f}%")

st.markdown("---")

# Sub-pages Overview Grid
st.subheader("System Modules")

col_a, col_b = st.columns(2)

with col_a:
    st.info(
        "\U0001f4c5 **Production Planning**\n\n"
        "Compare demand forecasts with inventory levels and scheduled production. "
        "Track status flags and capacity utilization percentages per product family."
    )
    st.success(
        "\U0001f4e6 **Material Requirements (MRP)**\n\n"
        "Calculate raw material quantities, evaluate safety inventory buffers, "
        "flag shortage amounts, and track purchase requirement statuses."
    )

with col_b:
    st.warning(
        "\U0001f4be **Inventory Management**\n\n"
        "Monitor current finished product stocks against safety buffer thresholds "
        "and view warehouse locations for all raw material inventories."
    )
    st.error(
        "\U0001f4ca **Advanced Capacity & Analytics**\n\n"
        "Review detailed machine scheduling allocations, daily workloads, "
        "and overall machine capacity utilization schedules."
    )

st.markdown("---")

# Refresh button
if st.button("\U0001f504 Refresh System Data"):
    st.cache_data.clear()
    st.rerun()