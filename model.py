import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

def load_data():
    df = pd.read_csv("data.csv")

    # 🔥 Fix missing values
    df = df.dropna()

    return df

def segment_customers(df):
    kmeans = KMeans(n_clusters=3, random_state=42)
    df["Segment"] = kmeans.fit_predict(df[["AnnualIncome", "SpendingScore"]])
    return df

def predict_sales(df):
    model = LinearRegression()
    X = df[["Age", "AnnualIncome"]]
    y = df["SpendingScore"]
    model.fit(X, y)
    df["PredictedScore"] = model.predict(X)
    return df