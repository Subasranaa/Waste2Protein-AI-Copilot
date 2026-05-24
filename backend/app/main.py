from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

from app.routes.health import router as health_router
from app.routes.predict import router as predict_router
from app.routes.insights import router as insights_router
from app.routes.history import router as history_router

app = FastAPI(
    title="Waste2Protein AI Copilot API",
    description="Backend API for microbial protein yield prediction and AI-generated insights.",
    version="0.1.0",
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(insights_router, prefix="/insights", tags=["Insights"])
app.include_router(history_router, prefix="/history", tags=["History"])


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Waste2Protein AI Platform</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7f5;
                color: #1f2933;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background: white;
                padding: 40px;
                border-radius: 18px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.08);
                max-width: 700px;
                text-align: center;
            }
            h1 {
                color: #12372a;
                margin-bottom: 12px;
            }
            p {
                font-size: 18px;
                line-height: 1.6;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                padding: 14px 24px;
                background: #2f7d32;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
            }
            a:hover {
                background: #256428;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Waste2Protein AI Platform</h1>
            <p>
                Backend AI service for predicting microbial protein yield from agri-food waste streams
                and generating LLM-assisted decision-support insights.
            </p>
            <p>
                Built with FastAPI, ML model serving, Groq LLM integration, Docker, CI/CD, and cloud deployment.
            </p>
            <a href="/docs">Go to API Docs</a>
        </div>
    </body>
    </html>
    """
