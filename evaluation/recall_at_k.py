import sys
import os
import pandas as pd
from collections import defaultdict

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender.retrieval import recommend_assessments

DATASET_PATH = "Gen_AI Dataset.xlsx"


def recall_at_10():
    df = pd.read_excel(DATASET_PATH)

    # Group relevant URLs by query
    ground_truth = defaultdict(set)

    for _, row in df.iterrows():
        query = row["Query"]
        url = row["Assessment_url"]
        ground_truth[query].add(url)

    recalls = []

    for query, relevant_urls in ground_truth.items():
        recommendations = recommend_assessments(query, top_k=10)
        recommended_urls = set(r["url"] for r in recommendations)

        retrieved_relevant = recommended_urls.intersection(relevant_urls)

        recall = len(retrieved_relevant) / len(relevant_urls)
        recalls.append(recall)

    mean_recall = sum(recalls) / len(recalls)

    print(f"Mean Recall@10: {mean_recall:.4f}")


if __name__ == "__main__":
    recall_at_10()
