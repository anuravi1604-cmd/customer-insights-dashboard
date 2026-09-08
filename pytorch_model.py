import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

# 1. Dataset Class
class CustomerDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# 2. PyTorch Neural Network Architecture (MLP)
class CustomerSpendingMLP(nn.Module):
    def __init__(self, input_dim=2):
        super(CustomerSpendingMLP, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Dropout(p=0.1),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.net(x)

# 3. Model Trainer
def train_pytorch_model(csv_path="data.csv", epochs=60):
    df = pd.read_csv(csv_path).dropna()
    X = df[["Age", "AnnualIncome"]].values
    y = df["SpendingScore"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    train_ds = CustomerDataset(X_train, y_train)
    test_ds = CustomerDataset(X_test, y_test)

    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=16, shuffle=False)

    model = CustomerSpendingMLP(input_dim=2)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)

    for epoch in range(1, epochs + 1):
        model.train()
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            preds = model(batch_x)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()

    # Evaluation
    model.eval()
    with torch.no_grad():
        test_preds = []
        actuals = []
        for batch_x, batch_y in test_loader:
            preds = model(batch_x)
            test_preds.extend(preds.squeeze().tolist())
            actuals.extend(batch_y.squeeze().tolist())

    test_preds = np.array(test_preds)
    actuals = np.array(actuals)
    mae = np.mean(np.abs(test_preds - actuals))
    rmse = np.sqrt(np.mean((test_preds - actuals)**2))

    print(f"PyTorch Training Complete | Test MAE: {mae:.2f} | Test RMSE: {rmse:.2f}")

    # Save state dict and scaler stats
    torch.save(model.state_dict(), "customer_model.pth")
    np.savez("scaler_params.npz", mean=scaler.mean_, scale=scaler.scale_)
    print("Saved customer_model.pth and scaler_params.npz")
    return model, scaler

if __name__ == "__main__":
    train_pytorch_model()
