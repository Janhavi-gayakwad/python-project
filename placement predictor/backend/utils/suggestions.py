def suggest_from_inputs(x):
    """
    Simple rule-based suggestions.
    x is a dict of inputs like cgpa, technical_score, soft_skill_score, etc.
    """
    suggestions = []

    # Academic checks
    if x.get("cgpa", 0) < 7:
        suggestions.append("Improve CGPA through consistent study and revision.")
    if x.get("twelfth_percentage", 0) < 70:
        suggestions.append("Revise fundamental subjects from 12th to strengthen basics.")

    # Skills checks
    if x.get("technical_score", 0) < 7:
        suggestions.append("Practice coding problems on LeetCode/HackerRank.")
    if x.get("soft_skill_score", 0) < 7:
        suggestions.append("Work on communication and presentation skills.")

    # Experience checks
    if x.get("internships", 0) == 0:
        suggestions.append("Do at least one internship to gain industry exposure.")
    if x.get("projects", 0) < 2:
        suggestions.append("Build more hands-on projects to showcase practical skills.")

    if not suggestions:
        suggestions.append("Keep up the good work! You are on track.")

    return suggestions
