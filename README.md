# 📊 Customer Insights & Spending Prediction Platform

A production-ready full-stack customer analytics platform combining **FastAPI**, **PyTorch Deep Learning**, and an interactive **Streamlit** dashboard with containerized **Docker** deployment.

---

## 🚀 Key Highlights
- **PyTorch Deep Learning:** Multi-Layer Perceptron (MLP) neural network with PyTorch `Dataset` & `DataLoader` for non-linear customer spending score regression.
- **Unsupervised Segmentation:** K-Means clustering for customer cohort identification.
- **High-Performance API:** FastAPI backend exposing REST endpoints for real-time model inference and customer segment filtering.
- **Docker Containerization:** Production-grade `Dockerfile` with layer caching, non-root security, automated healthchecks, and `docker-compose.yml`.

---

## 🛠️ Tech Stack
- **Languages & Frameworks:** Python, PyTorch, FastAPI, Streamlit, Scikit-learn, Pandas, NumPy
- **Containerization & DevOps:** Docker, Docker Compose, Linux, Git

---

## 🧠 Machine Learning & Deep Learning Architecture

### 1. PyTorch Multi-Layer Perceptron (`pytorch_model.py`)
- **Input Dimension:** Demographic & behavioral features (`Age`, `AnnualIncome`)
- **Network Structure:**
  - `Linear(2, 32)` $\rightarrow$ `ReLU` $\rightarrow$ `Dropout(0.1)`
  - `Linear(32, 16)` $\rightarrow$ `ReLU`
  - `Linear(16, 1)` (Continuous spending score output)
- **Loss Function:** MSE (Mean Squared Error)
- **Optimizer:** Adam with $L_2$ weight decay regularization (`lr=0.01`, `weight_decay=1e-4`)

### 2. K-Means Customer Clustering (`model.py`)
- Groups customers based on income and spending profiles to target high-value retention and growth segments.

---

## 🐳 Docker Deployment

Run both the FastAPI backend and Streamlit dashboard with a single command:

```bash
# Build and run all microservices
docker compose up --build

# API will be live at: http://localhost:8000
# Interactive Dashboard: http://localhost:8501
```

### Manual Local Setup
```bash
# 1. Clone repository
git clone https://github.com/anuravi1604-cmd/customer-insights-dashboard.git
cd customer-insights-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the PyTorch model
python3 pytorch_model.py

# 4. Start FastAPI server
uvicorn api:app --reload --port 8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status and container readiness |
| `GET` | `/data` | Clustered and segmented customer records |
| `POST` | `/predict/pytorch` | Deep learning inference for spending score prediction |

---

## 📄 License
MIT License. Developed by Anushka.
