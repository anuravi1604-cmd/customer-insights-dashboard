# ☁️ Microsoft Azure Cloud Architecture Specification
## Customer Insights & PyTorch Predictive Analytics Platform

This document details the alternative deployment architecture for running the containerized Customer Insights platform on **Microsoft Azure** using **Azure Container Apps (ACA)**.

---

## 🏛️ Azure Cloud Topology

```mermaid
graph TD
    User([End User / Marketing Lead]) -->|HTTPS| AppGateway[Azure Application Gateway / Front Door]
    AppGateway --> ACA_Env[Azure Container Apps Managed Environment]

    subgraph ACA_Env [ACA Serverless Kubernetes Environment]
        AppGateway -->|Routing /api| ACA_FastAPI[FastAPI Container App - Replicas 1-5]
        AppGateway -->|Routing /| ACA_Streamlit[Streamlit Container App - Replicas 1-3]
    end

    subgraph Azure Managed Services
        ACR[Azure Container Registry - ACR]
        BlobStorage[(Azure Blob Storage: customer_model.pth)]
        AppInsights[Azure Application Insights & Log Analytics]
        LogicApps[Azure Logic Apps / Power Automate Connector]
    end

    ACR -.->|Pulls Containers| ACA_FastAPI
    ACR -.->|Pulls Containers| ACA_Streamlit
    BlobStorage -.->|Loads Model| ACA_FastAPI
    ACA_FastAPI --> LogicApps
    LogicApps --> Outlook[Office 365 / Outlook Retention Email]
```

---

## 🛠️ Azure Component Highlights

1. **Azure Container Apps (ACA):** Built on managed Kubernetes (K8s / KEDA), automatically scales containers down to 0 replicas during idle periods (optimizing cloud consumption) and scales up to handle marketing traffic spikes.
2. **Azure Container Registry (ACR):** Private Docker registry with automated vulnerability scanning and RBAC authorization.
3. **Azure Blob Storage & Managed Identity:** Stores PyTorch checkpoint weights; accessed seamlessly via Azure Managed Identities without static API keys.
4. **Integration with Power Automate & Logic Apps:** Native Azure connectors enabling one-click dispatch of personalized retention campaigns through unified communications channels.

---

## 🚀 Azure CLI Deployment Commands

```bash
# 1. Log in to Azure
az login

# 2. Create Azure Container Registry (ACR)
az acr create --resource-group analytics-rg --name customerinsightsacr --sku Basic

# 3. Build container directly in ACR
az acr build --registry customerinsightsacr --image customer-insights-app:v2.5 .

# 4. Deploy to Azure Container Apps
az containerapp create \
  --name customer-analytics-app \
  --resource-group analytics-rg \
  --environment analytics-env \
  --image customerinsightsacr.azurecr.io/customer-insights-app:v2.5 \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 5
```
