import streamlit as st
import pandas as pd
from model import load_data, segment_customers, predict_sales

st.set_page_config(page_title="Customer Insights", layout="centered")

st.title("📊 Customer Insights Dashboard")

st.markdown(
    "This dashboard analyzes customer segments and predicts spending behavior using machine learning models."
)

# 🔥 Load and process data directly (NO API)
df = load_data()
df = segment_customers(df)
df = predict_sales(df)

# 📄 Data
st.subheader("📄 Customer Data")
st.dataframe(df)

# 📊 Insights
st.subheader("📊 Key Insights")
st.write("Average Spending Score:", round(df["SpendingScore"].mean(), 2))
st.write("Average Income:", round(df["AnnualIncome"].mean(), 2))

# 🎯 Filter
st.subheader("🎯 Filter by Segment")
segment = st.selectbox("Select Segment", sorted(df["Segment"].unique()))
filtered_df = df[df["Segment"] == segment]

st.write(f"Showing customers in Segment {segment}")
st.dataframe(filtered_df)

# 📊 Segments
st.subheader("📊 Customer Segments")
st.bar_chart(df["Segment"].value_counts())

# 📈 Predictions
st.subheader("📈 Predicted Spending")
st.line_chart(df["PredictedScore"])