from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse  # Added for explicit response type
import joblib
import pandas as pd
import os
from typing import Dict  # Better type hints

app = FastAPI(title="AfterBurn Calorie Predictor")

# Initialize templates (no static files needed unless you add CSS/JS)
templates = Jinja2Templates(directory="templates")

# Load model with version validation
try:
    pipeline = joblib.load("pipeline_model_v2.joblib")
    # Verify model contains expected steps
    if not hasattr(pipeline, 'named_steps'):
        raise RuntimeError("Invalid model format: Pipeline steps missing")
except Exception as e:
    raise RuntimeError(f"Model loading failed: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render prediction form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    Gender: str = Form(...),
    Age: float = Form(...),
    Height: float = Form(...),
    Weight: float = Form(...),
    Duration: float = Form(...),
    Heart_Rate: float = Form(...),
    Body_Temp: float = Form(...)
) -> Dict:
    """Handle prediction request with validation"""
    try:
        # Input validation
        validations = [
            (10 <= Age <= 100, "Age must be between 10-100"),
            (100 <= Height <= 250, "Height must be between 100-250cm"),
            (30 <= Weight <= 200, "Weight must be between 30-200kg"),
            (1 <= Duration <= 180, "Duration must be between 1-180 minutes"),
            (40 <= Heart_Rate <= 200, "Heart rate must be between 40-200bpm"),
            (35 <= Body_Temp <= 41, "Body temp must be between 35-41°C")
        ]
        
        for condition, error_msg in validations:
            if not condition:
                raise ValueError(error_msg)

        # Prepare input DataFrame (preserve column order)
        sample = pd.DataFrame([[
            Gender, Age, Height, Weight, Duration, Heart_Rate, Body_Temp
        ]], columns=["Gender", "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp"])

        # Predict and format
        result = round(float(pipeline.predict(sample)[0]), 2)
        equivalent_mins = round(result / 55, 1)  # 55 cal/min for running
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "calories": result,
                "equivalent": f"≈ {equivalent_mins} mins running",
                "food_equivalent": f"≈ {result/250:.1f} slices of pizza"  # 250 cal/slice
            }
        )
    
    except ValueError as ve:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(ve)},
            status_code=400
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": "Prediction failed. Please try again."},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        workers=1,
        timeout_keep_alive=60  # Helps prevent connection drops
    )