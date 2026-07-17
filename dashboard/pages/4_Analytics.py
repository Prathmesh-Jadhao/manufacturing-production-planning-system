import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import fetch_data, run_action

# Header
st.title("\U0001f4ca Machine Scheduling & Analytics")
st.markdown(
    "Review machine scheduling allocations, capacity utilization, "
    "and production workload distribution."
)

# Operations Panel
if st.button("\U0001f680 Run Machine Scheduling", use_container_width=True):
    with st.spinner("Generating Machine Schedule..."):
        res = run_action("/schedule/run")
        if res:
            st.success(res.get("message", "Machine schedule generated successfully."))
            st.cache_data.clear()

# Load Data
schedules = fetch_data("/schedule/")
schedule_df = pd.DataFrame(schedules)

st.markdown("---")

if schedule_df.empty:
    st.info(
        "No machine schedules found. Run Production Planning first, then run Machine Scheduling."
    )
else:
    # KPI Metrics
    col1, col2, col3 = st.columns(3)

    total_schedules = len(schedule_df)
    total_scheduled_qty = schedule_df["scheduled_quantity"].sum()
    avg_utilization = schedule_df["utilization"].mean()

    col1.metric("Total Schedules", total_schedules)
    col2.metric("Total Scheduled Qty", f"{total_scheduled_qty:,.0f}")
    col3.metric("Avg Machine Utilization", f"{avg_utilization:.2f}%")

    st.markdown("---")

    # Visualizations
    left, right = st.columns(2)

    with left:
        st.subheader("Scheduled Quantity by Machine")
        by_machine = (
            schedule_df.groupby("machine_id")["scheduled_quantity"]
            .sum()
            .reset_index()
            .sort_values("scheduled_quantity", ascending=False)
        )
        fig = px.bar(
            by_machine,
            x="machine_id",
            y="scheduled_quantity",
            labels={"machine_id": "Machine", "scheduled_quantity": "Scheduled Qty"},
            title="Total Scheduled Quantity by Machine",
            color="scheduled_quantity",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Machine Utilization")
        util_data = (
            schedule_df.groupby("machine_id")["utilization"]
            .mean()
            .reset_index()
            .sort_values("utilization", ascending=False)
        )
        fig = px.bar(
            util_data,
            x="machine_id",
            y="utilization",
            labels={"machine_id": "Machine", "utilization": "Utilization %"},
            title="Average Utilization by Machine",
            color="utilization",
            color_continuous_scale="RdYlGn",
            range_color=[0, 100],
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Product Allocation Table
    st.subheader("Scheduled Quantity by Product")
    by_product = (
        schedule_df.groupby("product_id")["scheduled_quantity"]
        .sum()
        .reset_index()
        .sort_values("scheduled_quantity", ascending=False)
    )
    fig = px.bar(
        by_product,
        x="product_id",
        y="scheduled_quantity",
        labels={"product_id": "Product", "scheduled_quantity": "Scheduled Qty"},
        color_discrete_sequence=["#AB63FA"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed Table
    st.subheader("Machine Schedule — Detailed Table")
    st.dataframe(
        schedule_df[
            [
                "schedule_id", "plan_id", "machine_id", "product_id",
                "scheduled_quantity", "utilization", "production_date", "status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )