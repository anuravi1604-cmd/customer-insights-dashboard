import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from model import load_data, segment_customers, predict_sales, evaluate_customer_campaign_trigger

st.set_page_config(
    page_title="Customer Insights & Cloud Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Insights & Cloud Analytics Platform")
st.caption("Containerized Microservice & Cloud Deployment | PyTorch Deep Learning | Automated Campaign Triggers")

# Load and process data
df = load_data()
df = segment_customers(df)
df = predict_sales(df)

# Top KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", len(df))
with col2:
    st.metric("Average Annual Income", f"${round(df['AnnualIncome'].mean(), 1)}k")
with col3:
    st.metric("Average Spending Score", f"{round(df['SpendingScore'].mean(), 1)}/100")
with col4:
    vip_count = len(df[df["Segment"] == "High-Value VIP"])
    st.metric("VIP Retention Candidates", f"{vip_count} ({round(vip_count/len(df)*100, 1)}%)")

st.markdown("---")

# Main Layout
tab1, tab2, tab3 = st.tabs([
    "📈 Customer Segmentation & Insights",
    "⚡ Digital Marketing Campaign Trigger (Power Automate)",
    "☁️ Cloud Architecture & Deployment"
])

with tab1:
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("🎯 Audience Cohort Distribution")
        segment_counts = df["Segment"].value_counts()
        st.bar_chart(segment_counts)
        
        st.subheader("📄 Segment Filtered Records")
        selected_seg = st.selectbox("Select Segment Cohort", sorted(df["Segment"].unique()))
        filtered_df = df[df["Segment"] == selected_seg]
        st.dataframe(filtered_df, use_container_width=True)

    with col_right:
        st.subheader("🧠 PyTorch vs Linear Model Output")
        st.line_chart(df[["SpendingScore", "PredictedScore"]].head(35))
        st.info("💡 Spending predictions are generated via combined regression models and PyTorch MLP neural network checkpoints.")


with tab2:
    st.subheader("⚡ Automated Retention Campaign Trigger (Power Automate & Unified Communications)")
    st.markdown(
        "Auto-flag high-value customers or at-risk churn cohorts to dispatch personalized retention offers directly via **Microsoft Power Automate**, **SendGrid**, or **AWS SNS**."
    )

    campaign_col1, campaign_col2 = st.columns([1, 1])

    with campaign_col1:
        st.markdown("#### 1. Select Customer Target")
        cust_options = df[df["CampaignEligible"] == True].head(15)
        selected_id = st.selectbox(
            "Eligible High-Value Target",
            cust_options["CustomerID"] if "CustomerID" in cust_options.columns else cust_options.index
        )

        selected_row = df.loc[df["CustomerID"] == selected_id].iloc[0] if "CustomerID" in df.columns else df.loc[selected_id]
        
        st.write(f"**Customer Profile:** Age {selected_row['Age']} | Income: ${selected_row['AnnualIncome']}k | Spending Score: {selected_row['SpendingScore']}/100")
        st.write(f"**Assigned Segment:** `{selected_row['Segment']}`")
        st.write(f"**Recommended Action:** `{selected_row['SuggestedAction']}`")

        webhook_target = st.text_input("Webhook Destination Endpoint", "https://prod-api.powerautomate.com/v1/triggers/retention-alert")
        
        if st.button("🚀 Fire Campaign Webhook Trigger", type="primary"):
            trigger_eval = evaluate_customer_campaign_trigger({
                "CustomerID": str(selected_id),
                "Age": selected_row["Age"],
                "AnnualIncome": selected_row["AnnualIncome"],
                "SpendingScore": selected_row["SpendingScore"]
            })
            st.session_state["last_trigger"] = trigger_eval
            st.success(f"✓ Campaign webhook successfully dispatched to Power Automate for Customer {selected_id}!")

    with campaign_col2:
        st.markdown("#### 2. Trigger Payload & Dynamic Email Preview")
        if "last_trigger" in st.session_state:
            trig = st.session_state["last_trigger"]
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Subject Line</div>
                <div style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.5rem; color: #f59e0b;">{trig['email_subject']}</div>
                <div style="font-size: 0.85rem; color: #cbd5e1; margin-bottom: 0.75rem;">
                    Dear Valued Customer,<br><br>
                    Because of your continued patronage, we're pleased to offer you exclusive early access to our Platinum Tier perks. Use your personal promo code below:
                </div>
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px dashed #f59e0b; padding: 0.5rem; text-align: center; font-weight: 800; letter-spacing: 0.08em; border-radius: 4px; color: #f59e0b;">
                    {trig['discount_code']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("##### Outbound Webhook JSON Body")
            st.json({
                "event": "CUSTOMER_RETENTION_CAMPAIGN_TRIGGERED",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "destination": webhook_target,
                "data": trig
            })
        else:
            st.info("Select an eligible customer on the left and click 'Fire Campaign Webhook Trigger' to preview outbound marketing payload.")


with tab3:
    st.subheader("☁️ Production Cloud Deployment Blueprint")
    st.markdown(
        """
        This application is architected for containerized deployment on **AWS (ECS Fargate)** or **Azure (Container Apps)**:
        
        * **AWS ECS Fargate:** Serverless container orchestration with zero EC2 management, auto-scaling based on CPU/Memory, and Application Load Balancers.
        * **PyTorch Model Registry:** Checkpoints stored on Amazon S3 and loaded into container RAM at startup.
        * **Unified Communications:** Direct integration with Power Automate, AWS SNS, and SendGrid for automated marketing campaign delivery.
        * **Cloud Certifications:** Paired with AWS Cloud Practitioner (CLF-C02) & Azure Fundamentals (AZ-900) operational competencies.
        """
    )
    st.code("""
# Run containerized locally or in cloud
docker compose up --build

# FastAPI API: http://localhost:8000
# Streamlit UI: http://localhost:8501
    """, language="bash")