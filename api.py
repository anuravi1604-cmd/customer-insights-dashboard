from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd
import numpy as np
import torch
import os
from model import load_data, segment_customers, predict_sales, evaluate_customer_campaign_trigger
from pytorch_model import CustomerSpendingMLP

app = FastAPI(
    title="Customer Insights & Deep Learning API",
    description="FastAPI service with K-Means clustering, PyTorch neural-network prediction, and rule-based campaign recommendations",
    version="2.5.1"
)

MODEL_CHECKPOINT = "customer_model.pth"
SCALER_PARAMS = "scaler_params.npz"
pytorch_model = None
scaler_mean = None
scaler_scale = None

if os.path.exists(MODEL_CHECKPOINT) and os.path.exists(SCALER_PARAMS):
    pytorch_model = CustomerSpendingMLP(input_dim=2)
    pytorch_model.load_state_dict(torch.load(MODEL_CHECKPOINT, map_location=torch.device("cpu"), weights_only=True))
    pytorch_model.eval()
    scaler_data = np.load(SCALER_PARAMS)
    scaler_mean = scaler_data["mean"]
    scaler_scale = scaler_data["scale"]

class CustomerInput(BaseModel):
    Age: float = Field(default=35.0, ge=18.0, le=100.0)
    AnnualIncome: float = Field(default=75.0, ge=10.0, le=300.0, description="Annual Income in $k")

class CampaignTriggerInput(BaseModel):
    CustomerID: Optional[str] = "CUST-1042"
    Age: float = Field(default=38.0)
    AnnualIncome: float = Field(default=85.0, description="Income in $k")
    SpendingScore: float = Field(default=78.0, description="Score 1-100")

@app.get("/")
def home():
    return {
        "message": "Customer Insights & Deep Learning API running",
        "pytorch_model_loaded": pytorch_model is not None,
        "features": ["PyTorch MLP Regression", "K-Means Audience Segmentation", "Rule-Based Campaign Recommendations"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "customer-insights-api"}

@app.get("/data")
def get_data():
    df = load_data()
    df = segment_customers(df)
    df = predict_sales(df)
    return df.to_dict(orient="records")

@app.post("/predict/pytorch")
def predict_pytorch(customer: CustomerInput):
    if pytorch_model is None:
        raise HTTPException(status_code=503, detail="PyTorch model checkpoint not found.")

    raw = np.array([[customer.Age, customer.AnnualIncome]])
    scaled = (raw - scaler_mean) / scaler_scale
    x_tensor = torch.tensor(scaled, dtype=torch.float32)

    with torch.no_grad():
        pred_score = pytorch_model(x_tensor).item()

    pred_score = max(1.0, min(100.0, pred_score))
    return {
        "input": customer.model_dump(),
        "predicted_spending_score": round(pred_score, 2),
        "model": "PyTorch CustomerSpendingMLP (2-layer neural network)"
    }

@app.post("/campaign/trigger")
def trigger_marketing_campaign(customer: CampaignTriggerInput):
    """Evaluate campaign rules and return a recommendation/payload preview.

    No external webhook or marketing message is sent by this endpoint.
    """
    return evaluate_customer_campaign_trigger(customer.model_dump())

@app.get("/campaign/audiences")
def get_audience_cohorts():
    """Return aggregated audience cohorts for campaign analysis."""
    df = load_data()
    df = segment_customers(df)

    summary = df.groupby("Segment").agg(
        Count=("CustomerID", "count") if "CustomerID" in df.columns else ("Age", "count"),
        AvgIncome=("AnnualIncome", "mean"),
        AvgSpending=("SpendingScore", "mean"),
        CampaignEligibleCount=("CampaignEligible", "sum")
    ).reset_index()

    return summary.to_dict(orient="records")
