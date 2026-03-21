import os
import pandas as pd

from src.config.config import RAW_RESUME_DIR, RAW_JD_DIR, OUTPUT_DIR
from src.data_processing.resume_parser import parse_resume
from src.data_processing.text_cleaner import clean_text
from src.data_processing.skill_extractor import extract_skills
from src.features.vectorizer import get_tfidf_vectors
from src.models.similarity_model import calculate_similarity
from src.models.ranking_model import rank_candidates
from src.visualization.plots import plot_scores
from src.evaluation.evaluator import evaluation_report, save_evaluation

# --------------------------------------------------
# Create output directory if not exists
# --------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Load Job Description
# --------------------------------------------------
jd_files = os.listdir(RAW_JD_DIR)
if len(jd_files) == 0:
    raise FileNotFoundError("❌ No job description found")

jd_path = os.path.join(RAW_JD_DIR, jd_files[0])
jd_text = parse_resume(jd_path)
jd_clean = clean_text(jd_text)
required_skills = extract_skills(jd_clean)

# --------------------------------------------------
# Load Resumes
# --------------------------------------------------
resume_texts = []
resume_names = []
resume_skills = []

resume_files = os.listdir(RAW_RESUME_DIR)
if len(resume_files) == 0:
    raise FileNotFoundError("❌ No resumes found")

for file in resume_files:
    file_path = os.path.join(RAW_RESUME_DIR, file)
    text = parse_resume(file_path)
    clean = clean_text(text)

    resume_texts.append(clean)
    resume_names.append(file)
    resume_skills.append(extract_skills(clean))

# --------------------------------------------------
# Vectorization (Resumes + Job Description)
# --------------------------------------------------
documents = resume_texts + [jd_clean]
vectors, _ = get_tfidf_vectors(documents)

resume_vectors = vectors[:-1]
jd_vector = vectors[-1]

# --------------------------------------------------
# Similarity Calculation
# --------------------------------------------------
scores = calculate_similarity(resume_vectors, jd_vector)

# --------------------------------------------------
# Ranking Candidates
# --------------------------------------------------
df = rank_candidates(
    resume_names,
    scores,
    resume_skills,
    required_skills
)

# --------------------------------------------------
# Save Ranking Output
# --------------------------------------------------
ranking_path = os.path.join(OUTPUT_DIR, "ranked_candidates.csv")
df.to_csv(ranking_path, index=False)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------
evaluation = evaluation_report(df)

evaluation_path = os.path.join(OUTPUT_DIR, "evaluation_report.csv")
save_evaluation(evaluation, evaluation_path)

# --------------------------------------------------
# Visualization
# --------------------------------------------------
plot_scores(df)

# --------------------------------------------------
# Console Output
# --------------------------------------------------
print("\n✅ Resume Screening Completed Successfully\n")

print("📄 Ranked Candidates saved at:")
print(ranking_path)

print("\n📊 Evaluation Metrics:")
for metric, value in evaluation.items():
    print(f"{metric}: {value}")

print("\n📄 Evaluation Report saved at:")
print(evaluation_path)