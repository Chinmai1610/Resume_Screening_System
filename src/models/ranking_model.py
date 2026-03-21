import pandas as pd

def rank_candidates(names, scores, skills, required_skills):
    results = []

    for name, score, skill in zip(names, scores, skills):
        missing_skills = list(set(required_skills) - set(skill))
        results.append({
            "Candidate": name,
            "Score": round(score, 3),
            "Skills": ", ".join(skill),
            "Missing Skills": ", ".join(missing_skills)
        })

    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False)
    return df