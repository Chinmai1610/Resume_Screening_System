from sklearn.feature_extraction.text import TfidfVectorizer

def get_tfidf_vectors(documents):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    return vectors, vectorizer