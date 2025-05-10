from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # New for static files
import joblib  # Changed from pickle
import pandas as pd
import os

app = FastAPI()

# Load model safely
try:
    pipeline = joblib.load("pipeline_model.joblib")
except Exception as e:
    raise RuntimeError(f"Model loading failed: {str(e)}")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(
    request: Request,
    Gender: str = Form(...),
    Age: float = Form(...),
    Height: float = Form(...),
    Weight: float = Form(...),
    Duration: float = Form(...),
    Heart_Rate: float = Form(...),
    Body_Temp: float = Form(...)
):
    try:
        sample = pd.DataFrame({
            "Gender": [Gender],
            "Age": [Age],
            "Height": [Height],
            "Weight": [Weight],
            "Duration": [Duration],
            "Heart_Rate": [Heart_Rate],
            "Body_Temp": [Body_Temp]
        })
        
        # Validate input ranges
        if not (10 <= Age <= 100):
            raise ValueError("Age must be between 10-100")
        if not (100 <= Height <= 250):
            raise ValueError("Height must be between 100-250cm")
        # Add other validations...

        result = round(float(pipeline.predict(sample)[0]), 2)
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request, 
                "calories": result,
                "equivalent": f"≈ {result/55:.1f} mins running"  # Bonus feature
            }
        )
    
    except Exception as e:
        return templates.TemplateResponse(
            "error.html", 
            {"request": request, "error": str(e)},
            status_code=400
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),  # For Render/Railway compatibility
        workers=1  # Recommended for small deployments
    )