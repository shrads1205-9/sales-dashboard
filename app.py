import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Flipkart Sales Dashboard")

# Load Data
data = pd.read_csv("flipkart_sales.csv")

# Convert Date
data["Order Date"] = pd.to_datetime(data["Order Date"])

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

category = st.sidebar.multiselect(
    "Select Category",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

payment = st.sidebar.multiselect(
    "Select Payment Method",
    options=data["Payment Method"].unique(),
    default=data["Payment Method"].unique()
)

# Apply Filters
filtered_data = data[
    (data["Category"].isin(category)) &
    (data["Payment Method"].isin(payment))
]

# KPIs
st.subheader("📌 Key Metrics")

total_sales = filtered_data["Total Sales (INR)"].sum()
total_orders = filtered_data.shape[0]
avg_rating = filtered_data["Customer Rating"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{int(total_sales)}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("⭐ Avg Rating", round(avg_rating, 2))

# Category-wise Sales
st.subheader("📊 Category-wise Sales")

cat_sales = filtered_data.groupby("Category")["Total Sales (INR)"].sum()

fig1, ax1 = plt.subplots()
cat_sales.plot(kind="bar", ax=ax1)
plt.xticks(rotation=45)
plt.xlabel("Category")
plt.ylabel("Sales")
st.pyplot(fig1)

# Monthly Trend
st.subheader("📈 Monthly Sales Trend")

filtered_data["Month"] = filtered_data["Order Date"].dt.to_period("M")
monthly_sales = filtered_data.groupby("Month")["Total Sales (INR)"].sum()

fig2, ax2 = plt.subplots()
monthly_sales.plot(ax=ax2)
plt.xlabel("Month")
plt.ylabel("Sales")
st.pyplot(fig2)

# Top Products
st.subheader("🔥 Top 10 Products")

top_products = filtered_data.groupby("Product Name")["Total Sales (INR)"].sum().nlargest(10)
st.bar_chart(top_products)

# Payment Method
st.subheader("💳 Payment Method Distribution")

payment_data = filtered_data["Payment Method"].value_counts()

fig3, ax3 = plt.subplots()
payment_data.plot(kind="pie", autopct="%1.1f%%", ax=ax3)
st.pyplot(fig3)

# Rating Distribution
st.subheader("⭐ Customer Rating Distribution")

fig4, ax4 = plt.subplots()
filtered_data["Customer Rating"].plot(kind="hist", bins=10, ax=ax4)
plt.xlabel("Rating")
st.pyplot(fig4)

# Download Button
st.download_button(
    "📥 Download Filtered Data",
    filtered_data.to_csv(index=False),
    "filtered_data.csv"
)

# Footer
st.write("✅ Made by Shraddha Shukla")