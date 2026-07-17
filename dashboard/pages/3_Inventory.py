import streamlit as st
import pandas as pd
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from helpers import fetch_data

# Header
st.title("\U0001f4be Inventory Management")
st.markdown(
    "Monitor finished product stock levels and raw material inventory "
    "against safety thresholds and reorder levels."
)

tab1, tab2 = st.tabs(["\U0001f4e6 Product Inventory", "\U0001f9f1 Material Inventory"])

# ---- Product Inventory Tab ----
with tab1:
    product_inv = fetch_data("/inventory/product")
    prod_df = pd.DataFrame(product_inv)

    if prod_df.empty:
        st.info("No product inventory data available.")
    else:
        # KPIs
        col1, col2, col3 = st.columns(3)
        total_stock = prod_df["current_stock"].sum()
        total_safety = prod_df["safety_stock"].sum()
        low_stock_count = (prod_df["current_stock"] <= prod_df["safety_stock"]).sum()

        col1.metric("Total Current Stock", f"{total_stock:,}")
        col2.metric("Total Safety Stock", f"{total_safety:,}")
        col3.metric("\U0001f6a8 Low Stock Items", low_stock_count)

        st.markdown("---")

        # Chart: Current vs Safety Stock
        st.subheader("Current Stock vs Safety Stock by Product")
        fig = px.bar(
            prod_df,
            x="product_id",
            y=["current_stock", "safety_stock"],
            barmode="group",
            labels={"value": "Quantity", "variable": "Type", "product_id": "Product"},
            color_discrete_sequence=["#636EFA", "#FFA15A"],
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Table
        st.subheader("Product Inventory — Detailed Table")
        st.dataframe(prod_df, use_container_width=True, hide_index=True)

# ---- Material Inventory Tab ----
with tab2:
    material_inv = fetch_data("/inventory/material")
    mat_df = pd.DataFrame(material_inv)

    if mat_df.empty:
        st.info("No material inventory data available.")
    else:
        # KPIs
        col1, col2, col3 = st.columns(3)
        total_available = mat_df["available_stock"].sum()
        total_reorder = mat_df["reorder_level"].sum()
        below_reorder = (mat_df["available_stock"] <= mat_df["reorder_level"]).sum()

        col1.metric("Total Available Stock", f"{total_available:,.2f}")
        col2.metric("Total Reorder Level", f"{total_reorder:,.2f}")
        col3.metric("\U0001f6a8 Below Reorder Level", below_reorder)

        st.markdown("---")

        # Chart: Available vs Reorder
        st.subheader("Available Stock vs Reorder Level by Material")
        fig = px.bar(
            mat_df,
            x="material_id",
            y=["available_stock", "reorder_level"],
            barmode="group",
            labels={"value": "Quantity", "variable": "Type", "material_id": "Material"},
            color_discrete_sequence=["#00CC96", "#EF553B"],
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Table
        st.subheader("Material Inventory — Detailed Table")
        st.dataframe(mat_df, use_container_width=True, hide_index=True)