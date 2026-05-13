from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.predict import router as predict_router

app = FastAPI(
    title="Waste2Protein AI Copilot API",
    description="Backend API for microbial protein yield prediction and AI-generated insights.",
    version="0.1.0",
    )

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    return {
        "message": "Waste2Protein AI Copilot API is running",
        "version": "0.1.0"
        }
