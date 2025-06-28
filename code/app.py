import pandas as pd
import datetime as dt
import streamlit as st
import mysql.connector
import plotly.express as px
from PIL import Image
import time

import warnings
warnings.filterwarnings('ignore')

from insights import generate_insights


# Page config
st.set_page_config(
    page_icon="🚗",
    page_title="Car Sales Dashboard",
    layout="wide"
)
st.title("📊 Casr Sales Dashboard")
st.write("⌚ Auto-refresh every 5 minutes. To refresh manually, click the below button")

image = Image.open("carsales_logo.jpg")

st.image(image, width=100)

# Refresh button
if st.button("🔃 Refresh"):
    st.rerun()

# MySQL connection
def get_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="car_sales_dashboard"
    )
    query = "SELECT * FROM carsales_data"
    return pd.read_sql(query, conn)

# Load and display data
df = get_data()

# Display insights
st.subheader("Quick Insights")
st.markdown(generate_insights(df))

st.divider()

table_col, chart_model = st.columns([0.50, 0.50])
with table_col:
    expander = st.expander("Sales Data")
    data = df
    expander.write(data.style.background_gradient(cmap="Greens"))

with chart_model:
    st.subheader("Sales by Model")
    fig_model = px.bar(df, x="model", y="total_sales", color="city", title="Total Sales by City")
    st.plotly_chart(fig_model, use_container_width=True)

st.divider()

table_city, chart_city = st.columns([0.45, 0.45])
with table_city:
    data = df.groupby("city")["total_sales"].sum()
    expander = st.expander("Sales by City")
    expander.write(data)

with chart_city:
    st.subheader("Sales by City")
    fig_city = px.bar(df, x="city", y="total_sales", title="Total Sales by City")
    st.plotly_chart(fig_city, use_container_width=True)

st.divider()

st.subheader("Overall View")
fig_treemap = px.treemap(
    df, path=["city", "model"],
    values="total_sales",
    hover_data="total_sales",
    color="model"
)
fig_treemap.update_layout(width=800, height=600)
st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()

# Time series analysis
df["month_year"] = df["sale_date"].dt.to_period("M")
st.subheader("Show Sales over Months")

month_df = pd.DataFrame(
    df.groupby(
        df["month_year"].dt.strftime("%Y-%b"))["total_sales"].sum()).reset_index()
fig_month = px.line(
    month_df, x="month_year", y="total_sales", labels={"total_sales": "Amount"},
    height=500, width=1000, template="gridon"
    )
st.plotly_chart(fig_month, use_container_width=True)






