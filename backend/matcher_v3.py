import joblib

from sklearn.metrics.pairwise import cosine_similarity

from backend.cv_analyzer import (
    extract_text,
    extract_skills
)


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

salary_lookup = joblib.load(
    "models/salary_lookup.pkl"
)

industry_lookup = joblib.load(
    "models/job_industry_lookup.pkl"
)

job_skill_lookup = joblib.load(
    "models/job_skill_lookup.pkl"
)

company_lookup = joblib.load(
    "models/company_lookup.pkl"
)


def get_missing_skills(
    cv_skills,
    job_skills
):
    """
    Find missing skills between CV and job.
    """

    cv_skill_set = {
        skill.lower()
        for skill in cv_skills
    }

    missing = []

    for skill in job_skills:

        if skill.lower() not in cv_skill_set:
            missing.append(skill)

    return missing


def recommend_jobs(
    cv_text,
    cv_skills,
    top_n=5
):
    """
    Recommend LinkedIn jobs.
    """

    cv_vector = vectorizer.transform(
        [cv_text]
    )

    similarities = cosine_similarity(
        cv_vector,
        job_vectors
    )[0]

    top_indices = (
        similarities.argsort()
        [-top_n:]
        [::-1]
    )

    recommendations = []

    for idx in top_indices:

        row = job_metadata.iloc[idx]

        job_id = row["job_id"]

        skills = job_skill_lookup.get(
            job_id,
            []
        )

        missing_skills = get_missing_skills(
            cv_skills,
            skills
        )

        salary_info = salary_lookup.get(
            job_id,
            {}
        )

        company_info = company_lookup.get(
            row["company_id"],
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

                "skills": skills,

                "missing_skills": missing_skills,

                "score": round(
                    similarities[idx] * 100,
                    2
                ),

                "company_size": company_info.get(
                    "company_size",
                    "Unknown"
                ),

                "company_description": company_info.get(
                    "description",
                    "No description available"
                ),

                "city": company_info.get(
                    "city",
                    "N/A"
                ),

                "country": company_info.get(
                    "country",
                    "N/A"
                ),

                "min_salary": salary_info.get(
                    "min_salary"
                ),

                "max_salary": salary_info.get(
                    "max_salary"
                ),

                "med_salary": salary_info.get(
                    "med_salary"
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

    cv_skills = extract_skills(
        cv_text
    )

    recommendations = recommend_jobs(
        cv_text,
        cv_skills,
        top_n=5
    )

    print("\n" + "=" * 70)
    print("CAREERPILOT AI RECOMMENDATIONS")
    print("=" * 70)

    print("\nYOUR CV SKILLS:")
    print(cv_skills)

    for i, job in enumerate(
        recommendations,
        start=1
    ):

        print("\n" + "-" * 70)

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
            f"Company Size: "
            f"{job['company_size']}"
        )

        print(
            f"Headquarters: "
            f"{job['city']}, "
            f"{job['country']}"
        )

        print(
            f"Match Score: "
            f"{job['score']}%"
        )

        if job["skills"]:

            print("\nRequired Skills:")

            for skill in job["skills"][:5]:

                print(f"  ✓ {skill}")

        if job["missing_skills"]:

            print("\nMissing Skills:")

            for skill in job["missing_skills"][:5]:

                print(f"  ✗ {skill}")

        if job["min_salary"] is not None:

            print(
                f"\nSalary Range: "
                f"{job['currency']} "
                f"{job['min_salary']} - "
                f"{job['max_salary']}"
            )

            if job["med_salary"] is not None:

                print(
                    f"Median Salary: "
                    f"{job['currency']} "
                    f"{job['med_salary']}"
                )

        print("\nCompany Description:")

        description = str(
            job["company_description"]
        )

        print(
            description[:250] + "..."
        )