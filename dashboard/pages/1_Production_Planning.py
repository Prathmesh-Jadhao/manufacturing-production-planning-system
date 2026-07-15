import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Production Planning",
    page_icon="📅",
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


def run_action(endpoint):
    try:
        response = requests.post(f"{API_URL}{endpoint}", timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error running calculation: {e}")
        return None


# -------------------------------
# Load Data
# -------------------------------
plans = fetch_data("/production-plans")
plans_df = pd.DataFrame(plans)

# -------------------------------
# Header
# -------------------------------
st.title("📅 Production Planning Control")
st.markdown("Monitor sales forecasts against planned production and trigger planning engine runs.")

# -------------------------------
# Operations Panel
# -------------------------------
if st.button("🚀 Run Production Planning Calculation", use_container_width=True):
    with st.spinner("Executing Production Planning Engine..."):
        res = run_action("/planning/run")
        if res:
            st.success(res.get("message", "Production planning generated successfully."))
            plans = fetch_data("/production-plans")
            plans_df = pd.DataFrame(plans)

st.markdown("---")

if plans_df.empty:
    st.info("No production plans found. Click the button above to run planning.")
else:
    # -------------------------------
    # KPI metrics
    # -------------------------------
    col1, col2, col3 = st.columns(3)
    forecast_qty = plans_df["forecast_qty"].sum()
    planned_qty = plans_df["planned_quantity"].sum()
    pending_qty = plans_df["pending_quantity"].sum()

    col1.metric("Total Forecast Qty", f"{forecast_qty:,.0f} units")
    col2.metric("Total Planned Qty", f"{planned_qty:,.0f} units")
    col3.metric("Pending (Over Capacity)", f"{pending_qty:,.0f} units")

    st.markdown("---")

    # -------------------------------
    # Visualizations
    # -------------------------------
    left, right = st.columns(2)

    with left:
        st.subheader("Forecast vs Planned Quantity")
        fig = px.bar(
            plans_df,
            x="product_id",
            y=["forecast_qty", "planned_quantity"],
            barmode="group",
            labels={"value": "Quantity", "variable": "Type"},
            title="Forecast vs Planned Quantity by Product"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Production Allocation Status")
        status = plans_df["status"].value_counts().reset_index()
        status.columns = ["Status", "Count"]
        fig = px.pie(
            status,
            names="Status",
            values="Count",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # -------------------------------
    # Data Table
    # -------------------------------
    st.subheader("Production Plans Detailed Table")
    st.dataframe(
        plans_df[[
            "plan_id", "plan_month", "product_id", "forecast_qty", 
            "available_stock", "production_required", "planned_quantity", 
            "pending_quantity", "capacity_utilization", "status"
        ]],
        use_container_width=True,
        hide_index=True
    )
