import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

def load_data():
    df = pd.read_csv("data.csv")
    df = df.dropna()
    return df

def segment_customers(df):
    """
    Applies K-Means clustering and assigns strategic marketing personas:
    - High-Value VIP: High income & high spending propensity
    - Value Conscious: High income & lower spending propensity (Growth target)
    - Budget / Moderate: Baseline income & moderate spending
    """
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(df[["AnnualIncome", "SpendingScore"]])
    df["ClusterId"] = cluster_labels

    # Map cluster centroids to meaningful business segments
    cluster_means = df.groupby("ClusterId")[["AnnualIncome", "SpendingScore"]].mean()
    sorted_clusters = cluster_means.sort_values(by="SpendingScore", ascending=False).index.tolist()
    
    segment_map = {
        sorted_clusters[0]: "High-Value VIP",
        sorted_clusters[1]: "Growth Potential",
        sorted_clusters[2]: "Conservative Spender"
    }
    df["Segment"] = df["ClusterId"].map(segment_map)

    # Automated Marketing Campaign Trigger Flag
    # High-Value VIP or High Income with declining score flagged for retention email
    df["CampaignEligible"] = df.apply(
        lambda r: True if (r["Segment"] == "High-Value VIP" or (r["AnnualIncome"] > 70 and r["SpendingScore"] > 60)) else False,
        axis=1
    )
    df["SuggestedAction"] = df["Segment"].map({
        "High-Value VIP": "Retention & VIP Concierge Offer",
        "Growth Potential": "Cross-Sell Loyalty Accelerator",
        "Conservative Spender": "Promotional Discount Nudge"
    })
    return df

def predict_sales(df):
    model = LinearRegression()
    X = df[["Age", "AnnualIncome"]]
    y = df["SpendingScore"]
    model.fit(X, y)
    df["PredictedScore"] = np.round(model.predict(X), 2)
    return df

def evaluate_customer_campaign_trigger(customer_dict: dict) -> dict:
    """
    Evaluates an individual customer record against marketing automation rules:
    Auto-flags high-value or churn-risk customers for retention email dispatch via Power Automate.
    """
    age = float(customer_dict.get("Age", 35))
    income = float(customer_dict.get("AnnualIncome", 75))
    score = float(customer_dict.get("SpendingScore", 70))
    customer_id = customer_dict.get("CustomerID", "CUST-9901")

    is_high_value = (income >= 65 and score >= 60)
    is_churn_risk = (income >= 75 and score < 45)

    if is_high_value:
        campaign_name = "VIP Tier Exclusive Retention & Loyalty Reward"
        channel = "Automated Email & SMS (Power Automate)"
        subject = "Exclusive VIP Reward: 25% Off Your Next Order"
        discount_code = "VIP-PLATINUM-25"
        trigger_status = "TRIGGER_DISPATCHED"
    elif is_churn_risk:
        campaign_name = "High-Value Win-Back & Re-Engagement Campaign"
        channel = "Executive Outreach & Personalized Email"
        subject = "We Miss You: Personal Invitation & Complimentary Perks"
        discount_code = "WINBACK-SURPRISE-30"
        trigger_status = "TRIGGER_DISPATCHED"
    else:
        campaign_name = "Standard Periodic Marketing Newsletter"
        channel = "Digest Email"
        subject = "Explore Our Latest Trending Collections"
        discount_code = "WELCOME-10"
        trigger_status = "STANDARD_QUEUE"

    return {
        "customer_id": customer_id,
        "trigger_status": trigger_status,
        "campaign_name": campaign_name,
        "channel": channel,
        "email_subject": subject,
        "discount_code": discount_code,
        "payload": {
            "recipient_id": customer_id,
            "annual_income_k": income,
            "spending_score": score,
            "lifecycle_stage": "High-Value Retention" if is_high_value else "Churn Risk" if is_churn_risk else "Nurture"
        }
    }