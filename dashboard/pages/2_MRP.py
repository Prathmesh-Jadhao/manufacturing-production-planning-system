import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import fetch_data, run_action

# Header
st.title("\U0001f4e6 Material Requirements Planning (MRP)")
st.markdown(
    "Calculate raw material requirements, evaluate inventory buffers, "
    "and track procurement status for all materials."
)

# Operations Panel
if st.button("\U0001f680 Run MRP Calculation", use_container_width=True):
    with st.spinner("Executing MRP Engine..."):
        res = run_action("/mrp/run")
        if res:
            st.success(res.get("message", "MRP generated successfully."))
            st.cache_data.clear()

# Load Data
requirements = fetch_data("/material-requirements/")
req_df = pd.DataFrame(requirements)

st.markdown("---")

if req_df.empty:
    st.info(
        "No material requirements found. Run Production Planning first, then run MRP."
    )
else:
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_reqs = len(req_df)
    total_required = req_df["required_quantity"].sum()
    total_shortage = req_df["shortage_quantity"].sum()
    ok_count = (req_df["procurement_status"] == "OK").sum()
    procurement_count = (req_df["procurement_status"] == "PROCUREMENT_REQUIRED").sum()

    col1.metric("Total Requirements", total_reqs)
    col2.metric("Total Required Qty", f"{total_required:,.2f}")
    col3.metric("Total Shortage", f"{total_shortage:,.2f}")
    col4.metric("Procurement Needed", procurement_count)

    st.markdown("---")

    # Visualizations
    left, right = st.columns(2)

    with left:
        st.subheader("Material Shortage by Material")
        shortage_by_material = (
            req_df.groupby("material_id")["shortage_quantity"]
            .sum()
            .reset_index()
            .sort_values("shortage_quantity", ascending=False)
        )
        fig = px.bar(
            shortage_by_material,
            x="material_id",
            y="shortage_quantity",
            labels={"material_id": "Material", "shortage_quantity": "Shortage Qty"},
            title="Total Shortage by Material",
            color="shortage_quantity",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Procurement Status Distribution")
        status_counts = req_df["procurement_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig = px.pie(
            status_counts,
            names="Status",
            values="Count",
            hole=0.4,
            color_discrete_map={
                "OK": "#00CC96",
                "PROCUREMENT_REQUIRED": "#EF553B",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Detailed Table
    st.subheader("Material Requirements — Detailed Table")
    st.dataframe(
        req_df[
            [
                "requirement_id", "product_id", "material_id",
                "required_quantity", "available_stock", "shortage_quantity",
                "procurement_required", "procurement_status", "unit", "status",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )