import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_RESUME_DIR = os.path.join(DATA_DIR, "raw", "resumes")
RAW_JD_DIR = os.path.join(DATA_DIR, "raw", "job_descriptions")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

SIMILARITY_THRESHOLD = 0.3