# 📊 Cloud-Deployed Customer Analytics & Predictive Platform
## PyTorch Deep Learning, Serverless Container Deployment & Automated Campaign Triggers

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?style=flat&logo=github)](https://github.com/anuravi1604-cmd/customer-insights-dashboard)
[![Docker Containerized](https://img.shields.io/badge/Docker-Containerized-blue?style=flat&logo=docker)](Dockerfile)
[![AWS ECS Fargate](https://img.shields.io/badge/AWS-ECS%20Fargate%20Ready-orange?style=flat&logo=amazonwebservices)](cloud/aws_architecture.md)
[![Azure Container Apps](https://img.shields.io/badge/Azure-Container%20Apps-blue?style=flat&logo=microsoftazure)](cloud/azure_architecture.md)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=flat&logo=pytorch)](https://pytorch.org)
[![Cloud Certifications](https://img.shields.io/badge/Cloud%20Certs-AWS%20%7C%20Azure-purple?style=flat)](CLOUD_CERTIFICATION_GUIDE.md)

A production-grade customer intelligence platform combining **PyTorch Deep Learning**, **FastAPI microservices**, an interactive **Streamlit dashboard**, and automated **Digital Marketing Campaign Triggers** deployed across **AWS ECS Fargate** and **Microsoft Azure**.

---

## 🚀 Key Highlights & Architectural Levers

* **Cloud-Native Deployment (AWS & Azure):** Containerized multi-service architecture ready for serverless container deployment via **AWS ECS Fargate** (backed by ALB and S3 model checkpoints) or **Azure Container Apps (ACA)**. Full specifications in [AWS Architecture](cloud/aws_architecture.md) and [Azure Architecture](cloud/azure_architecture.md).
* **Automated Retention Campaign Trigger (Digital Marketing):** Audience segmentation engine that automatically flags high-value VIP customers and at-risk cohorts, immediately dispatching personalized retention offers and dynamic discount codes via **Power Automate** and webhook integrations.
* **PyTorch Deep Learning:** 2-layer Multi-Layer Perceptron (MLP) neural network (`CustomerSpendingMLP`) utilizing PyTorch `Dataset` & `DataLoader` pipelines with $L_2$ weight decay regularization for continuous spending regression.
* **Unsupervised Customer Segmentation:** K-Means clustering assigning meaningful behavioral cohorts (*High-Value VIP*, *Growth Potential*, *Conservative Spender*).
* **Cloud Certification Alignment:** Built alongside a high-yield study and interview defense roadmap for **AWS Certified Cloud Practitioner (CLF-C02)** and **Azure Fundamentals (AZ-900)**. Full guide in [CLOUD_CERTIFICATION_GUIDE.md](CLOUD_CERTIFICATION_GUIDE.md).

---

## ☁️ Cloud Architecture Blueprint (AWS ECS Fargate)

```mermaid
graph TD
    Client([Internet User / Marketing Platform]) -->|HTTPS / 443| Route53[Amazon Route 53 DNS]
    Route53 --> CloudFront[Amazon CloudFront CDN / WAF]
    CloudFront --> ALB[Application Load Balancer]

    subgraph AWS VPC [Amazon VPC - Multi-AZ Architecture]
        ALB -->|Port 8000: /api| ECS_FastAPI[AWS ECS Fargate: FastAPI Microservice]
        ALB -->|Port 8501: /| ECS_Streamlit[AWS ECS Fargate: Streamlit Dashboard]

        ECS_FastAPI --> S3[(Amazon S3: PyTorch Model Weights)]
        ECS_FastAPI --> CloudWatch[Amazon CloudWatch Monitoring]
        
        ECS_FastAPI -->|Retention Webhook| PowerAutomate[Microsoft Power Automate Flow]
        PowerAutomate --> Outlook[Automated Retention Email Dispatch]
    end
```

---

## ⚡ Automated Marketing Campaign Trigger Workflow

When customer spending and demographic signals are processed, the platform automatically evaluates campaign eligibility:

```mermaid
sequenceDiagram
    autonumber
    participant App as Streamlit / FastAPI Platform
    participant Seg as K-Means Segmentation Engine
    participant Trigger as Campaign Dispatcher
    participant Webhook as Microsoft Power Automate
    participant Customer as High-Value Customer

    App->>Seg: Ingest Customer Profile (Income, Spending, Age)
    Seg-->>App: Classified as "High-Value VIP" (AnnualIncome >= $65k & Score >= 60)
    App->>Trigger: Evaluate Retention Campaign Eligibility
    Trigger->>Webhook: Dispatches Webhook Payload (Discount Code: VIP-PLATINUM-25)
    Webhook-->>Customer: Delivers Automated Personalized Retention Email & SMS
```

---

## 🛠️ Technology Stack
* **Languages & ML:** Python 3.11, PyTorch, Scikit-learn, Pandas, NumPy
* **Backend API:** FastAPI, Uvicorn, Pydantic
* **Frontend UI:** Streamlit (Wide-screen responsive layout)
* **Cloud & DevOps:** Docker, Docker Compose, AWS ECS Fargate, Azure Container Apps, GitHub Actions CI/CD
* **Automation:** Microsoft Power Automate Webhooks, JSON Event Dispatching

---

## 🏃 Quick Start: Run Locally

### Option A: Run with Docker Compose
```bash
# Build and start all microservices
docker compose up --build

# FastAPI API: http://localhost:8000
# Streamlit Dashboard: http://localhost:8501
```

### Option B: Standard Local Setup
```bash
# 1. Clone repository
git clone https://github.com/anuravi1604-cmd/customer-insights-dashboard.git
cd customer-insights-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train PyTorch model
python3 pytorch_model.py

# 4. Start FastAPI server
uvicorn api:app --reload --port 8000

# 5. In another terminal, run Streamlit app
streamlit run app.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status and container readiness |
| `GET` | `/data` | Clustered and segmented customer records |
| `POST` | `/predict/pytorch` | Deep learning inference for spending score prediction |
| `POST` | `/campaign/trigger` | Dispatches automated retention campaign via Power Automate webhook |
| `GET` | `/campaign/audiences`| Summary of active audience segments and campaign candidate counts |

---

## 📁 Repository Structure
```
customer-insights-dashboard/
├── cloud/
│   ├── aws_architecture.md     # AWS ECS Fargate & CloudFormation specs
│   └── azure_architecture.md   # Azure Container Apps & ACR specs
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── CLOUD_CERTIFICATION_GUIDE.md # AWS CLF-C02 & Azure AZ-900 interview defense
├── api.py                      # FastAPI microservice with campaign endpoints
├── app.py                      # Interactive Streamlit analytics & trigger UI
├── model.py                    # K-Means clustering & campaign logic
├── pytorch_model.py            # PyTorch MLP neural network implementation
├── customer_model.pth          # Serialized PyTorch model checkpoint
├── scaler_params.npz           # Feature standardizer weights
├── data.csv                    # Customer demographic & spending database
├── Dockerfile                  # Container build specification
├── docker-compose.yml          # Multi-service local composition
└── README.md                   # Complete architectural documentation
```

---

## 📄 License
MIT License. Developed by Anushka.
