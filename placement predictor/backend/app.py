from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from pathlib import Path

from utils.suggestions import suggest_from_inputs
from utils.resume_readers import extract_text_from_pdf, extract_text_from_docx, analyze_resume_text

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load trained model
MODEL_PATH = Path(__file__).resolve().parent / "ml" / "model.joblib"
MODEL_BUNDLE = joblib.load(MODEL_PATH)
PIPE = MODEL_BUNDLE["pipeline"]
FEATURES = MODEL_BUNDLE["features"]

def _validate_numeric(payload, name, default=None, min_val=0, max_val=100):
    """Validate numeric input and clamp range."""
    if name not in payload:
        if default is not None:
            value = float(default)
        else:
            raise ValueError(f"Missing field: {name}")
    else:
        try:
            value = float(payload[name])
        except:
            raise ValueError(f"Invalid value for {name}")
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} must be between {min_val} and {max_val}")
    return value

# Health check
@app.get("/api/health")
def health():
    return jsonify({"ok": True, "model_loaded": True})

# Placement Prediction  #
@app.post("/api/predict")
def predict():
    try:
        data = request.get_json(force=True)

        # Map HTML form names to backend field names
        x = {
            "cgpa": _validate_numeric(data, "cgpa", min_val=1, max_val=10),
            "technical_score": _validate_numeric(data, "technical_skills", min_val=1, max_val=10),
            "soft_skill_score": _validate_numeric(data, "soft_skills", min_val=1, max_val=10),
            "internships": _validate_numeric(data, "internships", min_val=0, max_val=10),
            "projects": _validate_numeric(data, "projects", min_val=0, max_val=10),
            "backlogs": _validate_numeric(data, "backlogs", min_val=0, max_val=10),
            "twelfth_percentage": _validate_numeric(data, "twelfth_percentage", min_val=0, max_val=100),
            "branch": str(data.get("branch", "")).upper().strip()
        }

        # Align DataFrame columns
        df = pd.DataFrame([x])
        for col in FEATURES:
            if col not in df.columns:
                df[col] = 0 if col != "branch" else ""
        df = df[FEATURES]

        # Predict placement probability
        proba = PIPE.predict_proba(df)[0][1]
        probability_percent = round(proba * 100, 2)
        label = "You have a good chance of being placed" if proba >= 0.5 else "Improve your communication or skills for better chance"

        # General suggestions
        suggestions = suggest_from_inputs(x)
        if x["branch"].lower() in ["mech", "civil", "eee", "ece"]:
            suggestions.append("Highlight core domain projects & learn one software/tool relevant to your branch.")
        if x["branch"].lower() in ["cse", "it"]:
            suggestions.append("Strengthen coding profiles (LeetCode, HackerRank, etc.).")

        return jsonify({
            "probability": probability_percent,
            "label": label,
            "inputs": x,
            "suggestions": suggestions
        })

    except Exception as e:
        app.logger.exception("Prediction failed")
        return jsonify({"error": str(e)}), 500


# ---------------- Resume Analysis ---------------- #
@app.post("/api/analyze_resume")
def analyze_resume():
    """Analyze uploaded resume and suggest skills/courses."""
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No resume file uploaded"}), 400

        file = request.files["resume"]
        content = file.read()

        # Detect file type
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith(".docx"):
            text = extract_text_from_docx(content)
        else:
            return jsonify({"error": "Unsupported file type (use .pdf or .docx)"}), 400

        # Analyze the text
        analysis = analyze_resume_text(text)

        return jsonify({
            "skills_found": analysis["skills_found"],
            "missing_skills": analysis["missing_skills"],
            "recommendations": analysis["recommendations"],
            "summary": analysis["summary"]
        })

    except Exception as e:
        app.logger.exception("Resume analysis failed")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
