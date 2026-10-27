
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Customer Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Sales Data Analysis")
st.write("Analyze product sales, revenue, profit and regional performance.")

# 1. Load the actual CSV file
FILE_PATH = "customer_sales_analysis.csv"

try:
    sales = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    st.error(f"CSV file not found: {FILE_PATH}")
    st.info("Keep the CSV file in the same folder as app.py.")
    st.stop()
except Exception as e:
    st.error(f"Could not read the CSV file: {e}")
    st.stop()

if sales.empty:
    st.warning("The CSV file contains no data.")
    st.stop()

# Clean column names
sales.columns = sales.columns.str.strip()

# Match common column-name variations
def find_column(possible_names):
    lookup = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in sales.columns
    }
    for name in possible_names:
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

# Required columns for product analysis
if product_col is None:
    st.error("Product column not found in the CSV.")
    st.write("Available columns:", sales.columns.tolist())
    st.stop()

sales["Product"] = sales[product_col].astype(str)

if quantity_col is not None:
    sales["Quantity"] = pd.to_numeric(
        sales[quantity_col], errors="coerce"
    ).fillna(0)
else:
    sales["Quantity"] = 0

if price_col is not None:
    sales["Unit_Price"] = pd.to_numeric(
        sales[price_col], errors="coerce"
    )
else:
    sales["Unit_Price"] = None

# Revenue: use existing column or calculate it
if revenue_col is not None:
    sales["Revenue"] = pd.to_numeric(
        sales[revenue_col], errors="coerce"
    )
elif price_col is not None and quantity_col is not None:
    sales["Revenue"] = sales["Quantity"] * sales["Unit_Price"]
else:
    sales["Revenue"] = None

# Profit: use actual profit if provided; otherwise calculate
# only when a cost column is available.
if profit_col is not None:
    sales["Profit"] = pd.to_numeric(
        sales[profit_col], errors="coerce"
    )
elif cost_col is not None and quantity_col is not None:
    sales["Unit_Cost"] = pd.to_numeric(
        sales[cost_col], errors="coerce"
    )
    sales["Profit"] = (
        sales["Revenue"] - sales["Quantity"] * sales["Unit_Cost"]
    )
else:
    sales["Profit"] = None

# Region handling
if region_col is not None:
    sales["Region"] = sales[region_col].fillna("Unknown").astype(str)
else:
    sales["Region"] = "Not provided"

# Date handling
if date_col is not None:
    sales["Order_Date"] = pd.to_datetime(
        sales[date_col], errors="coerce"
    )
    sales["Month"] = sales["Order_Date"].dt.strftime("%b")

# Sidebar filters
st.sidebar.header("🔎 Filters")

regions = ["All"] + sorted(sales["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

products = ["All"] + sorted(sales["Product"].unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", products)

filtered = sales.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_product != "All":
    filtered = filtered[filtered["Product"] == selected_product]

# Key performance indicators
st.subheader("📌 Key Performance Indicators")

c1, c2, c3 = st.columns(3)

total_revenue = filtered["Revenue"].sum()
c1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.2f}" if pd.notna(total_revenue) else "Unavailable"
)

total_profit = filtered["Profit"].sum()
c2.metric(
    "Total Profit",
    f"₹{total_profit:,.2f}" if pd.notna(total_profit) else "Unavailable"
)

c3.metric("Units Sold", f"{filtered['Quantity'].sum():,.0f}")

# Revenue by product
st.subheader("💰 Revenue by Product")

if filtered["Revenue"].notna().any():
    product_revenue = filtered.groupby("Product")["Revenue"].sum()
    st.bar_chart(product_revenue)
else:
    st.info("Revenue cannot be calculated. Check the CSV price and quantity columns.")

# Profit by product
st.subheader("📈 Profit by Product")

if filtered["Profit"].notna().any():
    product_profit = filtered.groupby("Product")["Profit"].sum()
    st.bar_chart(product_profit)
else:
    st.info("Profit is unavailable because cost or profit data is missing.")

# Monthly sales trend
st.subheader("📅 Monthly Sales Trend")

if date_col is not None and filtered["Order_Date"].notna().any():
    monthly_sales = (
        filtered.dropna(subset=["Order_Date"])
        .set_index("Order_Date")
        .resample("MS")["Revenue"]
        .sum()
    )
    st.line_chart(monthly_sales)
else:
    st.info("Monthly trend needs a valid date column in the CSV.")

# Region-wise revenue
st.subheader("🌍 Region-wise Revenue")

if region_col is not None and filtered["Revenue"].notna().any():
    region_revenue = filtered.groupby("Region")["Revenue"].sum()
    st.bar_chart(region_revenue)
else:
    st.info("Region-wise analysis needs a Region column and revenue data.")

# Sales data
st.subheader("🧾 Sales Data")
st.dataframe(filtered, use_container_width=True)

# Download filtered data
csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Sales Data as CSV",
    data=csv_data,
    file_name="sales_analysis.csv",
    mime="text/csv"
)

st.caption("Dashboard results are based on the uploaded CSV data.")
