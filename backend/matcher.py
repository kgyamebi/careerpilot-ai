import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.cv_analyzer import extract_text


def calculate_match_score(cv_text, job_text):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [cv_text, job_text]
    )

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )

    return round(
        similarity[0][0] * 100,
        2
    )


def recommend_jobs(cv_text, jobs_df):

    recommendations = []

    for _, row in jobs_df.iterrows():

        score = calculate_match_score(
            cv_text,
            row["description"]
        )

        recommendations.append(
            {
                "job_title": row["job_title"],
                "company": row["company"],
                "score": score
            }
        )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


if __name__ == "__main__":

    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    jobs_df = pd.read_csv(
        "data/jobs.csv"
    )

    matches = recommend_jobs(
        cv_text,
        jobs_df
    )

    print("\nTOP JOB MATCHES")
    print("=" * 50)

    for match in matches:

        print(
            f"{match['job_title']} "
            f"({match['company']}) "
            f"- {match['score']}%"
        )