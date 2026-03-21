from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_vectors, jd_vector):
    similarities = cosine_similarity(resume_vectors, jd_vector)
    return similarities.flatten()