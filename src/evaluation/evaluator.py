import numpy as np
import pandas as pd
from scipy.stats import spearmanr


def precision_at_k(df, k=3, threshold=0.3):
    """
    Calculates Precision@K based on similarity score threshold
    """
    top_k = df.head(k)
    relevant = top_k[top_k["Score"] >= threshold]
    precision = len(relevant) / k
    return round(precision, 3)


def spearman_rank_correlation(scores):
    """
    Measures ranking consistency
    """
    true_rank = np.arange(len(scores), 0, -1)
    corr, _ = spearmanr(scores, true_rank)
    return round(corr, 3)


def evaluation_report(df, threshold=0.3):
    """
    Generates a full evaluation report
    """
    report = {}

    report["Average Score"] = round(df["Score"].mean(), 3)
    report["Max Score"] = round(df["Score"].max(), 3)
    report["Min Score"] = round(df["Score"].min(), 3)

    report["Precision@3"] = precision_at_k(df, k=3, threshold=threshold)
    report["Precision@5"] = precision_at_k(df, k=5, threshold=threshold)
    report["Spearman Rank Correlation"] = spearman_rank_correlation(df["Score"])

    return report


def save_evaluation(report, output_path):
    """
    Saves evaluation metrics to CSV
    """
    df = pd.DataFrame(list(report.items()), columns=["Metric", "Value"])
    df.to_csv(output_path, index=False)