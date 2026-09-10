# 📊 Customer Insights Dashboard
## Customer Segmentation, Spending Prediction & Analytics

An interactive customer analytics application built with **Python, Streamlit, scikit-learn, PyTorch, FastAPI, and Docker**. The project explores customer segmentation, spending-score prediction, and a rule-based campaign recommendation workflow.

> 🌐 **Live Streamlit App:** https://customer-insights-1604.streamlit.app

## Key Features

- **Customer Segmentation:** K-Means clustering groups customers into three behavioral cohorts based on annual income and spending score.
- **Spending Prediction:** Compares a scikit-learn linear regression baseline with a PyTorch MLP model for spending-score prediction.
- **Campaign Recommendations:** Applies rule-based eligibility logic to identify customers who may be suitable for retention or promotional campaigns. The current implementation generates recommendations and payload previews locally; it does **not** send real marketing messages.
- **Containerization & CI:** Docker configuration supports reproducible local execution, while GitHub Actions installs dependencies, verifies the API/model modules, and builds the Docker image.

## Current Deployment Status

**The Streamlit dashboard is deployed on Streamlit Community Cloud. The AWS and Azure files in this repository are architecture blueprints only — the application is not currently deployed to AWS ECS/Fargate or Azure Container Apps.**

The repository should therefore be described as **Dockerized and cloud-ready by design**, not cloud-deployed.

## Architecture Blueprint

The `cloud/` directory contains proposed deployment designs for AWS ECS Fargate and Azure Container Apps. These documents describe how the application could be deployed in the future; they are not evidence of an active cloud deployment.

## Technology Stack

- **Languages & ML:** Python 3.11, PyTorch, scikit-learn, Pandas, NumPy
- **Backend:** FastAPI, Uvicorn, Pydantic
- **Frontend:** Streamlit
- **DevOps:** Docker, Docker Compose, GitHub Actions
- **Analytics:** K-Means clustering, Linear Regression, PyTorch MLP

## Run Locally

### Docker Compose

```bash
docker compose up --build

# FastAPI API: http://localhost:8000
# Streamlit Dashboard: http://localhost:8501
```

### Standard Python Setup

```bash
git clone https://github.com/anuravi1604-cmd/customer-insights-dashboard.git
cd customer-insights-dashboard
pip install -r requirements.txt

python3 pytorch_model.py
uvicorn api:app --reload --port 8000

# In another terminal
streamlit run app.py
```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | API health status |
| `GET` | `/data` | Customer records with segmentation and predictions |
| `POST` | `/predict/pytorch` | PyTorch spending-score inference |
| `POST` | `/campaign/trigger` | Evaluates campaign rules and returns a recommendation/payload preview |
| `GET` | `/campaign/audiences` | Aggregated customer segment and campaign-eligibility counts |

## Repository Structure

```text
customer-insights-dashboard/
├── cloud/
│   ├── aws_architecture.md       # Proposed AWS deployment blueprint
│   └── azure_architecture.md     # Proposed Azure deployment blueprint
├── .github/workflows/
│   └── deploy.yml                # CI: dependency check, module verification & Docker build
├── api.py                         # FastAPI service
├── app.py                         # Streamlit dashboard
├── model.py                       # K-Means segmentation & campaign rules
├── pytorch_model.py               # PyTorch MLP implementation
├── customer_model.pth             # Trained PyTorch checkpoint
├── scaler_params.npz              # Model preprocessing parameters
├── data.csv                       # Customer dataset
├── Dockerfile                     # Container definition
├── docker-compose.yml              # Local multi-service setup
└── README.md
```

## License

MIT License. Developed by Anushka.
