
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Sales Data Analysis")
st.write("Analyze sales, profit, products, and regional performance.")

# Load CSV data
try:
    sales = pd.read_csv("customer_sales_analysis.csv")
except FileNotFoundError:
    st.error("customer_sales_analysis.csv not found. Keep it beside app.py.")
    st.stop()
except Exception as e:
    st.error(f"Unable to load CSV: {e}")
    st.stop()

if sales.empty:
    st.warning("Your CSV file is empty.")
    st.stop()

sales.columns = sales.columns.str.strip()

# Find columns despite common naming differences
def find_column(names):
    lookup = {
        str(c).strip().lower().replace(" ", "_"): c
        for c in sales.columns
    }
    for name in names:
        key = name.lower().replace(" ", "_")
        if key in lookup:
            return lookup[key]
    return None

product_col = find_column(["Product", "Product_Name", "Item"])
quantity_col = find_column(["Quantity", "Qty", "Units_Sold"])
price_col = find_column(["Unit_Price", "Price", "Selling_Price"])
region_col = find_column(["Region", "Area", "Location"])
date_col = find_column(["Order_Date", "Date", "Sales_Date"])
revenue_col = find_column(["Revenue", "Sales", "Total_Sales"])
profit_col = find_column(["Profit", "Total_Profit"])
cost_col = find_column(["Unit_Cost", "Cost_Price"])

if product_col is None:
    st.error("Product column not found.")
    st.write("CSV columns found:", sales.columns.tolist())
    st.stop()

# Standardize fields
sales["Product"] = sales[product_col].fillna("Unknown").astype(str)

sales["Quantity"] = (
    pd.to_numeric(sales[quantity_col], errors="coerce").fillna(0)
    if quantity_col else 0
)

if revenue_col:
    sales["Revenue"] = pd.to_numeric(
        sales[revenue_col], errors="coerce"
    )
elif price_col and quantity_col:
    sales["Revenue"] = (
        sales["Quantity"] *
        pd.to_numeric(sales[price_col], errors="coerce")
    )
else:
    sales["Revenue"] = float("nan")

if profit_col:
    sales["Profit"] = pd.to_numeric(
        sales[profit_col], errors="coerce"
    )
elif cost_col and quantity_col:
    unit_cost = pd.to_numeric(sales[cost_col], errors="coerce")
    sales["Profit"] = sales["Revenue"] - sales["Quantity"] * unit_cost
else:
    sales["Profit"] = float("nan")

sales["Region"] = (
    sales[region_col].fillna("Unknown").astype(str)
    if region_col else "Not provided"
)

if date_col:
    sales["Order_Date"] = pd.to_datetime(
        sales[date_col], errors="coerce"
    )
    sales["Month"] = sales["Order_Date"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("🔎 Dashboard Filters")

regions = ["All"] + sorted(sales["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions)

products = ["All"] + sorted(sales["Product"].unique().tolist())
selected_product = st.sidebar.selectbox("Product", products)

search = st.sidebar.text_input("Search product")

filtered = sales.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_product != "All":
    filtered = filtered[filtered["Product"] == selected_product]

if search.strip():
    filtered = filtered[
        filtered["Product"].str.contains(
            search.strip(), case=False, na=False, regex=False
        )
    ]

# KPI cards update with all filters
st.subheader("📌 Key Performance Indicators")

c1, c2, c3 = st.columns(3)

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()

c1.metric("Total Revenue", f"₹{revenue:,.2f}")
c2.metric(
    "Total Profit",
    f"₹{profit:,.2f}" if filtered["Profit"].notna().any() else "Unavailable"
)
c3.metric("Units Sold", f"{filtered['Quantity'].sum():,.0f}")

# Revenue chart
st.subheader("💰 Revenue by Product")

if filtered["Revenue"].notna().any():
    st.bar_chart(filtered.groupby("Product")["Revenue"].sum())
else:
    st.info("Revenue data is unavailable.")

# Profit chart
st.subheader("📈 Profit by Product")

if filtered["Profit"].notna().any():
    st.bar_chart(filtered.groupby("Product")["Profit"].sum())
else:
    st.info("Profit data or cost information is unavailable.")

# Monthly trend
st.subheader("📅 Monthly Sales Trend")

if date_col and filtered["Order_Date"].notna().any():
    monthly = (
        filtered.dropna(subset=["Order_Date"])
        .set_index("Order_Date")
        .resample("MS")["Revenue"]
        .sum()
    )
    st.line_chart(monthly)
else:
    st.info("Add a valid order date column to show monthly trends.")

# Region comparison
st.subheader("🌍 Region-wise Revenue")

if region_col and filtered["Revenue"].notna().any():
    st.bar_chart(filtered.groupby("Region")["Revenue"].sum())
else:
    st.info("Region or revenue data is unavailable.")

# Business insights use filtered results
st.subheader("💡 Business Insights")

if not filtered.empty and filtered["Revenue"].notna().any():
    top_product = filtered.groupby("Product")["Revenue"].sum().idxmax()
    st.write(f"🏆 Highest revenue product: **{top_product}**")

    if region_col:
        top_region = filtered.groupby("Region")["Revenue"].sum().idxmax()
        st.write(f"🌍 Highest revenue region: **{top_region}**")
else:
    st.info("No sales insights available for these filters.")

# Sales table
st.subheader("🧾 Sales Data")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "⬇️ Download Filtered Sales CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="sales_analysis.csv",
    mime="text/csv"
)

st.caption("Analysis uses the CSV data. Profit is shown only when profit or cost data is available.")
