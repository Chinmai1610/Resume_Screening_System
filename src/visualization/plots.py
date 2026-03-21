import matplotlib.pyplot as plt

def plot_scores(df):
    plt.figure()
    plt.barh(df["Candidate"], df["Score"])
    plt.xlabel("Matching Score")
    plt.ylabel("Candidate")
    plt.title("Resume Ranking")
    plt.show()