import joblib

from sklearn.metrics.pairwise import cosine_similarity

from backend.cv_analyzer import extract_text


# Load LinkedIn job index
job_vectors = joblib.load(
    "models/job_vectors.pkl"
)

vectorizer = joblib.load(
    "models/job_vectorizer.pkl"
)

job_metadata = joblib.load(
    "models/job_metadata.pkl"
)

# Load salary lookup
salary_lookup = joblib.load(
    "models/salary_lookup.pkl"
)

# Load industry lookup
industry_lookup = joblib.load(
    "models/job_industry_lookup.pkl"
)

# Load job skills lookup
job_skill_lookup = joblib.load(
    "models/job_skill_lookup.pkl"
)


def recommend_jobs(cv_text, top_n=10):
    """
    Recommend top matching LinkedIn jobs.
    """

    cv_vector = vectorizer.transform(
        [cv_text]
    )

    similarities = cosine_similarity(
        cv_vector,
        job_vectors
    )[0]

    top_indices = similarities.argsort()[-top_n:][::-1]

    recommendations = []

    for idx in top_indices:

        row = job_metadata.iloc[idx]

        job_id = row["job_id"]

        salary_info = salary_lookup.get(
            job_id,
            {}
        )

        recommendations.append(
            {
                "job_id": job_id,

                "title": row["title"],

                "company": row["company_name"],

                "location": row["location"],

                "industry": industry_lookup.get(
                    job_id,
                    "Unknown"
                ),

                "skills": job_skill_lookup.get(
                    job_id,
                    []
                ),

                "score": round(
                    similarities[idx] * 100,
                    2
                ),

                "min_salary": salary_info.get(
                    "min_salary"
                ),

                "med_salary": salary_info.get(
                    "med_salary"
                ),

                "max_salary": salary_info.get(
                    "max_salary"
                ),

                "currency": salary_info.get(
                    "currency"
                )
            }
        )

    return recommendations


if __name__ == "__main__":

    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    recommendations = recommend_jobs(
        cv_text,
        top_n=10
    )

    print("\n" + "=" * 70)
    print("TOP LINKEDIN JOB RECOMMENDATIONS")
    print("=" * 70)

    for i, job in enumerate(
        recommendations,
        start=1
    ):

        print(f"\n{i}. {job['title']}")

        print(
            f"Company: {job['company']}"
        )

        print(
            f"Location: {job['location']}"
        )

        print(
            f"Industry: {job['industry']}"
        )

        print(
            f"Match Score: {job['score']}%"
        )

        if job["skills"]:

            print("Skills:")

            for skill in job["skills"][:5]:

                print(f"   • {skill}")

        if job["min_salary"] is not None:

            print(
                f"Salary Range: "
                f"{job['currency']} "
                f"{job['min_salary']} - "
                f"{job['max_salary']}"
            )

            print(
                f"Median Salary: "
                f"{job['currency']} "
                f"{job['med_salary']}"
            )