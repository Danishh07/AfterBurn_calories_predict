# 🔥 AfterBurn Calorie Predict

A FastAPI-based machine learning app that predicts calorie burn based on user input.

## 🖼️ Preview

[![Screenshot-2025-05-11-042203.png](https://i.postimg.cc/zGCDtcvB/Screenshot-2025-05-11-042203.png)](https://postimg.cc/NK0wLb1q)


---

## 🗂️ Project Structure
```bash
AfterBurn_Calories_Predict/
├── 📂 templates/                    # Frontend templates
│   ├── 🚨 error.html                # Error page
│   ├── 🏠 index.html                # Input form
│   └── 📊 result.html               # Results display
├── 🐍 app.py                              # FastAPI backend
├── 🤖 pipeline_model_v2.joblib            # Trained ML model
├── 📜 requirements.txt                    # Dependencies
├── 🚀 render.yaml                         # Render config
├── 🐳 Dockerfile                          # Docker setup
├── 🔢 calories.csv                        # Calorie data
├── 🏋️ exercise.csv                        # Exercise data
├── 📓 Calories_Burnt_Prediction_ML.ipynb  # Notebook/script
└── 🙈 .gitignore                          # Ignored files
```


## 🚀 Features

- ✅ Calorie burn prediction via `/predict` endpoint  
- ✅ FastAPI backend with automatic docs (`/docs` or `/redoc`)  
- ✅ Deployed with CI/CD on Render  

---

## 🛠️ Tech Stack

- **Backend**: Python + FastAPI (with Jinja2 templates)  
- **Machine Learning**: XGBoost Regressor + Scikit-learn (saved as `.joblib` pipeline)  
- **Deployment**: Render (Cloud Hosting)  
- **Data Processing**: Pandas, NumPy  
- **Frontend**: HTML/CSS (static templates in `templates/`)  

---

## 🧪 Usage

### 1. 📦 Local Development

- Clone the repository ~

      git clone https://github.com/your-username/AfterBurn_calories_predict.git

- Install dependencies ~

      pip install -r requirements.txt

-  Run app ~

       python app.py


### 2. 🌐 API Endpoints

GET /
- Description: Homepage

POST /predict
- Description: Predict calories (expects JSON input)
- Example Input:
```json
{
  "age": 25,
  "gender": "male",
  "height": 175,
  "weight": 70,
  "duration": 30,
  "heart_rate": 120,
  "body_temp": 37.5
}
```

### 3. 🔴 Live Deployment

You can access the deployed app at the following link:

🔗 [https://afterburn.onrender.com](https://afterburn.onrender.com)
