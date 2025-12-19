import pandas as pd
from recommender.retrieval import recommend_assessments

INPUT_PATH = "Gen_AI Dataset.xlsx"
OUTPUT_PATH = "predictions.csv"

df = pd.read_excel(INPUT_PATH)

rows = []

for query in df["Query"].unique():
    recommendations = recommend_assessments(query, top_k=10)

    for r in recommendations:
        rows.append({
            "Query": query,
            "Assessment_url": r["url"]
        })

out_df = pd.DataFrame(rows)
out_df.to_csv(OUTPUT_PATH, index=False)

print("predictions.csv generated successfully")
