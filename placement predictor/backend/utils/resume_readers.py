from io import BytesIO
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(BytesIO(content))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}")
    return text

def extract_text_from_docx(content: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        file_like = BytesIO(content)
        doc = docx.Document(file_like)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise RuntimeError(f"DOCX extraction failed: {e}")

def analyze_resume_text(text: str) -> dict:
    """Analyze resume text and generate skill-based improvement suggestions."""
    text_lower = text.lower()

    # Skill keywords to detect
    skills = [
        "python", "java", "c++", "html", "css", "javascript",
        "sql", "machine learning", "data analysis", "communication"
    ]

    # Map each skill to recommended learning resources
    skill_courses = {
        "python": ["Python for Everybody (Coursera)", "Google IT Automation with Python"],
        "java": ["Java Programming Masterclass (Udemy)", "Oracle Certified Associate Java SE"],
        "c++": ["C++ for Beginners (Codecademy)"],
        "html": ["HTML & CSS for Beginners (freeCodeCamp)"],
        "css": ["Responsive Web Design (freeCodeCamp)"],
        "javascript": ["JavaScript Essentials (Udemy)", "Frontend Development (Coursera)"],
        "sql": ["SQL for Data Science (Coursera)", "Database Management Basics (edX)"],
        "machine learning": ["Machine Learning by Andrew Ng (Coursera)"],
        "data analysis": ["Data Analyst Professional Certificate (Google)"],
        "communication": ["Business Communication Skills (LinkedIn Learning)"]
    }

    # Identify present and missing skills
    skills_found = [s for s in skills if s in text_lower]
    missing_skills = [s for s in skills if s not in text_lower]

    # Recommend learning resources for missing skills
    recommendations = []
    for skill in missing_skills:
        if skill in skill_courses:
            recommendations.extend(skill_courses[skill])

    return {
        "skills_found": skills_found,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
        "summary": f"Found {len(skills_found)} relevant skills. Suggested {len(recommendations)} learning items."
    }
