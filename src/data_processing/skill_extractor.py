SKILLS = [
    "python", "java", "sql", "machine learning",
    "deep learning", "nlp", "data analysis",
    "tensorflow", "pandas", "numpy", "scikit learn"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))