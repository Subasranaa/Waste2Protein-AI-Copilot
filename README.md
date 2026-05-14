# Waste2Protein AI Platform

An AI-powered backend platform for predicting microbial protein yield from agri-food waste streams and generating LLM-assisted decision-support insights.

This project was designed as a production-oriented AI platform prototype focused on backend architecture, API engineering, cloud deployment, ML inference, and LLM integration.

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