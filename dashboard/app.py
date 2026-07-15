import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Manufacturing Production Planning Dashboard",
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
st.title("🏭 Manufacturing Production Planning Dashboard")
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

col1.metric(
    "Products",
    total_products
)

col2.metric(
    "Forecast Quantity",
    f"{forecast_qty:,.0f}"
)

col3.metric(
    "Planned Quantity",
    f"{planned_qty:,.0f}"
)

col4.metric(
    "Avg Capacity Utilization",
    f"{avg_utilization:.2f}%"
)

st.markdown("---")

# -------------------------------
# Charts
# -------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Forecast vs Planned Quantity")

    if not plans_df.empty:

        fig = px.bar(
            plans_df,
            x="product_id",
            y=[
                "forecast_qty",
                "planned_quantity"
            ],
            barmode="group",
            title="Forecast vs Planned Production"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with right:

    st.subheader("Production Status")

    if not plans_df.empty:

        status = (
            plans_df["status"]
            .value_counts()
            .reset_index()
        )

        status.columns = [
            "Status",
            "Count"
        ]

        fig = px.pie(
            status,
            names="Status",
            values="Count",
            hole=0.45,
            title="Production Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.markdown("---")

# -------------------------------
# Capacity Utilization
# -------------------------------

st.subheader("Capacity Utilization by Product")

if not plans_df.empty:

    fig = px.bar(
        plans_df,
        x="product_id",
        y="capacity_utilization",
        color="status",
        text="capacity_utilization",
        title="Capacity Utilization (%)"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -------------------------------
# Procurement Status
# -------------------------------

st.subheader("Material Procurement Status")

if not mrp_df.empty:

    procurement = (
        mrp_df["procurement_status"]
        .value_counts()
        .reset_index()
    )

    procurement.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        procurement,
        names="Status",
        values="Count",
        hole=0.45,
        title="Procurement Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -------------------------------
# Material Shortages
# -------------------------------

st.subheader("Material Shortages")

if not mrp_df.empty:

    shortage = mrp_df[
        mrp_df["shortage_quantity"] > 0
    ]

    if not shortage.empty:

        fig = px.bar(
            shortage,
            x="material_id",
            y="shortage_quantity",
            color="procurement_status",
            title="Material Shortage"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.success("No material shortages.")

st.markdown("---")

# -------------------------------
# Production Plans
# -------------------------------

st.subheader("Production Plans")

if not plans_df.empty:

    st.dataframe(
        plans_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# -------------------------------
# Material Requirements
# -------------------------------

st.subheader("Material Requirements")

if not mrp_df.empty:

    st.dataframe(
        mrp_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

# -------------------------------
# Refresh
# -------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.rerun()