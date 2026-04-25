import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Customer Insights", layout="centered")

st.title("📊 Customer Insights Dashboard (Live API)")

st.markdown("This dashboard analyzes customer segments and predicts spending behavior using machine learning models served via a FastAPI backend.")

API_URL = "http://127.0.0.1:8000/data"

try:
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

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

    else:
        st.error("API error")

except Exception as e:
    st.error("API not running or connection failed")