# python-project
#  Student Placement Predictor & Resume Analyzer

An end-to-end **Machine Learning + Flask** project that predicts a student’s placement probability and analyzes their resume to recommend missing skills and courses.

This project helps students understand:
- Their chances of getting placed  
- What skills they lack  
- What they should improve  
- Resume-based improvement suggestions  

---

## Features

### **1. Placement Prediction (ML Model)**
Uses Random Forest classifier to predict placement likelihood based on:

- CGPA  
- Technical Skills  
- Soft Skills  
- Internships  
- Projects  
- Backlogs  
- 12th Percentage  
- Branch  

Returns:
- Placement probability (0–100%)  
- Final decision label  
- Personalized suggestions  

---

###  **2. Resume Analysis (PDF/DOCX)**

Uploads a resume → Extracts text → Analyzes skills.

Finds:
- Skills present  
- Missing skills  
- Recommended courses  
- Important summary  

Technologies used:
- PyPDF2  
- python-docx  
- NLP-based keyword matching  

---

### **3. Skill-Based Suggestions Engine**
A rule-based recommendation system that suggests improvements like:
- Coding practice  
- Soft skill improvement  
- Doing internships  
- Building projects  
- Branch-specific advice  

---

## Tech Stack

### **Backend**
- Python  
- Flask  
- Flask-CORS  
- Joblib  
- Pandas  

### **Machine Learning**
- Random Forest Classifier  
- Scikit-Learn  
- OneHotEncoding (branch)  
- Custom preprocessing pipeline  

### **Resume Processing**
- PyPDF2  
- python-docx  
- Regex / Keyword Matching  

---

## Project Structure
placement-predictor/
│
├── backend/                                  # Flask backend (API + ML)
│   │
│   ├── app.py                                # Main backend application (Flask API)
│   ├── requirements.txt                       # Python dependencies
│   │
│   ├── data/                                  # Dataset storage
│   │   └── placements.csv                     # Training dataset for ML model
│   │
│   ├── ml/                                    # Machine learning model & training
│   │   ├── model.joblib                       # Saved Random Forest model
│   │   └── train.py                           # Script to train/update the ML model
│   │
│   └── utils/                                 # Utility and helper functions
│       ├── resume_readers.py                  # Extract & analyze resume (PDF/DOCX)
│       └── suggestions.py                     # Rule-based skill improvement suggestions
│
│
├── frontend/                                  # Frontend UI (HTML, CSS, JS)
│   │
│   ├── index.html                             # Main landing page
│   ├── home.html                              # Placement prediction form UI
│   │
│   ├── style.css                              # General stylesheet for UI
│   ├── home.css                               # Styles for home.html
│   │
│   ├── script.js                              # Connects frontend ↔ backend API
│   └── background.jpg                         # Images
│
│
├── README.md                                  # Project documentation
└── .gitignore                                 # Ignore venv, cache, pyc files etc.

---

## API Endpoints

### 1.Placement Prediction**
POST /api/predict
Request JSON:
```json
{
  "cgpa": 8.0,
  "technical_skills": 7,
  "soft_skills": 6,
  "internships": 1,
  "projects": 2,
  "backlogs": 0,
  "twelfth_percentage": 75,
  "branch": "CSE"
}
Response:
{
  "probability": 82.5,
  "label": "You have a good chance of being placed",
  "suggestions": [...]
}
### 2.Resume Analyzer
POST /api/analyze_resume


Supports:
.pdf
.docx

Response:
{
  "skills_found": [...],
  "missing_skills": [...],
  "recommendations": [...],
  "summary": "Found 5 relevant skills..."
}

## How to Run Locally
1. Install dependencies
pip install -r requirements.txt
2. Train the model (optional)
python train.py
3. Run the backend
python app.py
Backend will start on:
http://127.0.0.1:5000

---

## 🖼 Screenshots
https://github.com/Janhavi-gayakwad/python-project/tree/main/placement%20predictor/screenshot

## 📎 GitHub Repository
[student placement predictor](https://github.com/Janhavi-gayakwad/python-project/tree/main/placement%20predictor)

