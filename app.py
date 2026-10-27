
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Sales Data Analysis")
st.write("Analyze product sales, regional revenue, monthly trends and profit.")

# Sample sales data
sales = pd.DataFrame({
    "Product": [
        "Laptop", "Phone", "Tablet", "Laptop", "Phone",
        "Tablet", "Laptop", "Phone", "Tablet", "Laptop"
    ],
    "Quantity": [2, 5, 3, 1, 4, 2, 3, 6, 1, 2],
    "Unit_Price": [
        50000, 20000, 15000, 50000, 20000,
        15000, 50000, 20000, 15000, 50000
    ],
    "Region": [
        "North", "South", "East", "West", "North",
        "South", "East", "West", "North", "South"
    ],
    "Order_Date": pd.to_datetime([
        "2026-01-05", "2026-01-12",
        "2026-02-03", "2026-02-15",
        "2026-03-02", "2026-03-18",
        "2026-04-04", "2026-04-21",
        "2026-05-10", "2026-05-25"
    ])
})

# Assumed costs for this educational demo
cost_prices = {"Laptop": 35000, "Phone": 12000, "Tablet": 9000}

sales["Revenue"] = sales["Quantity"] * sales["Unit_Price"]
sales["Unit_Cost"] = sales["Product"].map(cost_prices)
sales["Total_Cost"] = sales["Quantity"] * sales["Unit_Cost"]
sales["Profit"] = sales["Revenue"] - sales["Total_Cost"]
sales["Month"] = sales["Order_Date"].dt.strftime("%b")

# Sidebar filters
st.sidebar.header("Filters")

regions = ["All"] + sorted(sales["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

products = ["All"] + sorted(sales["Product"].unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", products)

filtered = sales.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_product != "All":
    filtered = filtered[filtered["Product"] == selected_product]

# KPI cards
st.subheader("📌 Key Performance Indicators")

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"₹{filtered['Revenue'].sum():,.0f}")
c2.metric("Total Profit", f"₹{filtered['Profit'].sum():,.0f}")
c3.metric("Units Sold", int(filtered["Quantity"].sum()))

# Revenue by product
st.subheader("💰 Revenue by Product")
product_revenue = filtered.groupby("Product")["Revenue"].sum()
st.bar_chart(product_revenue)

# Profit by product
st.subheader("📈 Profit by Product")
product_profit = filtered.groupby("Product")["Profit"].sum()
st.bar_chart(product_profit)

# Monthly sales trend
st.subheader("📅 Monthly Sales Trend")
monthly_sales = (
    filtered.groupby("Month")["Revenue"]
    .sum()
    .reindex(["Jan", "Feb", "Mar", "Apr", "May"])
    .fillna(0)
)
st.line_chart(monthly_sales)

# Region-wise revenue
st.subheader("🌍 Region-wise Revenue")
region_revenue = filtered.groupby("Region")["Revenue"].sum()
st.bar_chart(region_revenue)

# Sales table
st.subheader("🧾 Sales Data")
st.dataframe(
    filtered.drop(columns=["Unit_Cost", "Month"]),
    use_container_width=True
)

# CSV download
csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Sales Data as CSV",
    data=csv_data,
    file_name="sales_analysis.csv",
    mime="text/csv"
)

st.caption(
    "Educational demo using sample sales data and assumed product costs."
)
