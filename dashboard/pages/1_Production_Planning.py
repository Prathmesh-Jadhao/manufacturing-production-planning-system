import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import fetch_data, run_action

# Header
st.title("\U0001f4c5 Production Planning Control")
st.markdown(
    "Monitor sales forecasts against planned production and trigger planning engine runs."
)

# Operations Panel
if st.button("\U0001f680 Run Production Planning Calculation", use_container_width=True):
    with st.spinner("Executing Production Planning Engine..."):
        res = run_action("/planning/run")
        if res:
            st.success(res.get("message", "Production planning generated successfully."))
            st.cache_data.clear()

# Load Data
plans = fetch_data("/production-plans/")
plans_df = pd.DataFrame(plans)

st.markdown("---")

if plans_df.empty:
    st.info("No production plans found. Click the button above to run planning.")
else:
    # KPI Metrics
    col1, col2, col3 = st.columns(3)
    forecast_qty = plans_df["forecast_qty"].sum()
    planned_qty = plans_df["planned_quantity"].sum()
    pending_qty = plans_df["pending_quantity"].sum()

    col1.metric("Total Forecast Qty", f"{forecast_qty:,.0f} units")
    col2.metric("Total Planned Qty", f"{planned_qty:,.0f} units")
    col3.metric("Pending (Over Capacity)", f"{pending_qty:,.0f} units")

    st.markdown("---")

    # Visualizations
    left, right = st.columns(2)

    with left:
        st.subheader("Forecast vs Planned Quantity")
        fig = px.bar(
            plans_df,
            x="product_id",
            y=["forecast_qty", "planned_quantity"],
            barmode="group",
            labels={"value": "Quantity", "variable": "Type", "product_id": "Product"},
            title="Forecast vs Planned Quantity by Product",
            color_discrete_sequence=["#636EFA", "#00CC96"],
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
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Data Table
    st.subheader("Production Plans — Detailed Table")
    st.dataframe(
        plans_df[
            [
                "plan_id", "plan_month", "product_id", "forecast_qty",
                "available_stock", "production_required", "planned_quantity",
                "pending_quantity", "capacity_utilization", "status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
