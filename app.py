
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 Customer Sales Data Analysis")
st.write("Analyze product sales, regional revenue, and profitability.")

# Sample data for this dashboard
sales = pd.DataFrame({
    "Product": ["Laptop", "Phone", "Tablet", "Laptop", "Phone",
                "Tablet", "Laptop", "Phone", "Tablet", "Laptop"],
    "Quantity": [2, 5, 3, 1, 4, 2, 3, 6, 1, 2],
    "Unit_Price": [50000, 20000, 15000, 50000, 20000,
                   15000, 50000, 20000, 15000, 50000],
    "Region": ["North", "South", "East", "West", "North",
               "South", "East", "West", "North", "South"]
})

cost_prices = {"Laptop": 35000, "Phone": 12000, "Tablet": 9000}

sales["Revenue"] = sales["Quantity"] * sales["Unit_Price"]
sales["Total_Cost"] = sales["Quantity"] * sales["Product"].map(cost_prices)
sales["Profit"] = sales["Revenue"] - sales["Total_Cost"]

# Dashboard filters
region = st.selectbox(
    "Select Region",
    ["All"] + sorted(sales["Region"].unique().tolist())
)

filtered = sales if region == "All" else sales[sales["Region"] == region]

# Key metrics
c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"₹{filtered['Revenue'].sum():,.0f}")
c2.metric("Total Profit", f"₹{filtered['Profit'].sum():,.0f}")
c3.metric("Units Sold", int(filtered["Quantity"].sum()))

st.subheader("Revenue by Product")
product_revenue = filtered.groupby("Product")["Revenue"].sum()
st.bar_chart(product_revenue)

st.subheader("Profit by Product")
product_profit = filtered.groupby("Product")["Profit"].sum()
st.bar_chart(product_profit)

st.subheader("Sales Data")
st.dataframe(filtered, use_container_width=True)

st.caption("Educational demo using sample sales data and assumed product costs.")
