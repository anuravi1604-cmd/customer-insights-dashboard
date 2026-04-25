from fastapi import FastAPI
from model import load_data, segment_customers, predict_sales

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Customer Insights API running"}

@app.get("/data")
def get_data():
    df = load_data()
    df = segment_customers(df)
    df = predict_sales(df)
    return df.to_dict(orient="records")