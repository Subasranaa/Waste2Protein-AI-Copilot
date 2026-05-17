# Waste2Protein AI Platform

An AI-powered backend platform for predicting microbial protein yield from agri-food waste streams and generating LLM-assisted decision-support insights.

This project was designed as a production-oriented AI platform prototype focused on backend architecture, API engineering, cloud deployment, ML inference, and LLM integration.

Live Demo: https://waste2protein-backend.onrender.com

---

# Overview

Millions of tonnes of nutrient-rich agri-food waste are generated globally every day. These waste streams may be upcycled into sustainable microbial protein through fermentation processes.

This platform enables users to:

- Predict microbial protein yield from waste-stream composition
- Generate AI-assisted decision-support insights
- Receive microbial candidate recommendations
- Identify limiting fermentation factors
- Generate R&D roadmap suggestions
- Estimate early-stage economic feasibility

---

# Key Features

## Machine Learning Inference

- Trained Random Forest regression model
- Protein yield prediction
- Uncertainty estimation
- Structured prediction responses

## LLM-Assisted Decision Support

Integrated Groq-hosted LLM for:

- Microbial candidate recommendations
- Limiting factor identification
- Fermentation recommendations
- R&D roadmap generation
- Scientific decision-support summaries

## Backend Engineering

- FastAPI backend architecture
- Modular service-based design
- Pydantic request validation
- OpenAPI / Swagger documentation
- Dockerized deployment
- Public cloud deployment on Render

## Reliability & Engineering Features

- Environment-based configuration
- Request caching layer
- Graceful LLM fallback handling
- CI/CD workflow with GitHub Actions
- API testing with Pytest
- Cost-aware inference tracking

---

# System Architecture

```text
Frontend / Client
        ↓
FastAPI Backend API
        ↓
Prediction Service (ML Model)
        ↓
LLM Insight Service (Groq)
        ↓
Economic Feasibility Service
        ↓
Caching + Cost Tracking
```
---

# Repository Structure

```text
waste2protein-ai-copilot/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── predict.py
│   │   │   └── insights.py
│   │   ├── services/
│   │   │   ├── prediction_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── cost_tracker.py
│   │   │   ├── cache_service.py
│   │   │   └── economics_service.py
│   │   └── model/
│   │       └── protein_model.pkl
│   │
│   ├── tests/
│       ├── test_api.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pytest.ini
│
├── ml/
│   ├── generate_synthetic_data.py
│   ├── train_model.py
│   └── sample_protein_data.csv
│
├── .github/
│   └── workflows/
│       └── backend-ci.yml
│
├── README.md
└── .gitignore

```
---
# Run Locally

## 1. Clone Repository

```bash
git clone https://github.com/Subasranaa/waste2protein-ai-copilot.git
cd waste2protein-ai-copilot
```

---

## 2. Backend Setup

Move into backend directory:

```bash
cd backend
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate virtual environment:

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the `backend/` directory:

```text
backend/.env
```

Add the following variables:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

---

## 5. Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Landing page:

```text
http://127.0.0.1:8000
```

---

## 6. Run Tests

Open another terminal.

Activate virtual environment again:

```bash
cd backend
source venv/bin/activate
```

Run tests:

```bash
pytest
```

---

# Docker Usage

## Build Docker Image

```bash
docker build -t waste2protein-backend ./backend
```

## Run Docker Container

```bash
docker run -p 8000:8000 --env-file backend/.env waste2protein-backend
```

Open:

```text
http://127.0.0.1:8000/docs
```
---

# CI/CD

GitHub Actions is configured to run backend tests automatically on push and pull requests.

Workflow file:

```bash
.github/workflows/backend-ci.yml
```

The pipeline:
- Checks out repository
- Sets up Python
- Installs dependencies
- Runs Pytest test suite

# Limitations

This is an early-stage prototype.

- The training dataset is synthetic.
- Protein yield predictions are for demonstration only.
- Economic estimates are scenario-based and simplified.
- Microbial recommendations require laboratory validation.
- This system should not be used as a substitute for experimental fermentation studies.

# Future Improvements

- Replace synthetic data with real experimental fermentation and waste-composition datasets
- Add database-backed request logging and experiment tracking
- Add persistent Redis caching for repeated LLM requests
- Add model monitoring, drift detection, and retraining workflows
- Add authentication, rate limiting, and usage quotas for public API access
- Add stakeholder-facing dashboard for food producers and researchers
- Improve optimisation using Bayesian optimisation or simulation-based search
- Add uncertainty quantification beyond Random Forest tree variance
- Add support for multiple LLM providers with provider routing and fallback logic
- Deploy to AWS ECS, Elastic Beanstalk, or Azure Container Apps for production-scale hosting
