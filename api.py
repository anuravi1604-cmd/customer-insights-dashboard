from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import torch
import os
from model import load_data, segment_customers, predict_sales
from pytorch_model import CustomerSpendingMLP

app = FastAPI(
    title="Customer Insights & Deep Learning API",
    description="FastAPI service with K-Means clustering, Linear Regression, and PyTorch Neural Network prediction",
    version="2.0.0"
)

# Load PyTorch model if checkpoint exists
MODEL_CHECKPOINT = "customer_model.pth"
SCALER_PARAMS = "scaler_params.npz"
pytorch_model = None
scaler_mean = None
scaler_scale = None

if os.path.exists(MODEL_CHECKPOINT) and os.path.exists(SCALER_PARAMS):
    pytorch_model = CustomerSpendingMLP(input_dim=2)
    pytorch_model.load_state_dict(torch.load(MODEL_CHECKPOINT, map_location=torch.device('cpu'), weights_only=True))
    pytorch_model.eval()
    
    scaler_data = np.load(SCALER_PARAMS)
    scaler_mean = scaler_data["mean"]
    scaler_scale = scaler_data["scale"]

class CustomerInput(BaseModel):
    Age: float
    AnnualIncome: float

@app.get("/")
def home():
    return {
        "message": "Customer Insights & Deep Learning API running",
        "pytorch_model_loaded": pytorch_model is not None
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
        "input": customer.dict(),
        "predicted_spending_score": round(pred_score, 2),
        "model": "PyTorch CustomerSpendingMLP (2-layer neural network)"
    }
