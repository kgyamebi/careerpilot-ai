import joblib

from sklearn.metrics.pairwise import cosine_similarity

from backend.cv_analyzer import (
    analyze_cv
)


# ==============================
# LOAD MODELS
# ==============================

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


# ==============================
# MISSING SKILLS
# ==============================

def get_missing_skills(
    cv_skills,
    job_skills
):

    cv_skill_set = {
        skill.lower()
        for skill in cv_skills
    }

    missing = []

    for skill in job_skills:

        if skill.lower() not in cv_skill_set:

            missing.append(skill)

    return missing


# ==============================
# SMART MATCHING BONUS
# ==============================

def get_job_bonus(
    cv_data,
    title,
    industry,
    skills
):

    bonus = 0

    title = str(title).lower()
    industry = str(industry).lower()

    qualifications = [

        q.lower()

        for q in cv_data[
            "education"
        ][
            "qualifications"
        ]
    ]

    experience = " ".join(
        cv_data["experience"]
    ).lower()

    skills_text = " ".join(
        skills
    ).lower()

    # -------------------------
    # PHD BONUS
    # -------------------------

    if any(
        "phd" in q
        for q in qualifications
    ):

        academic_terms = [

            "lecturer",
            "professor",
            "faculty",
            "research",
            "academic",
            "curriculum",
            "educator"
        ]

        if any(
            term in title
            for term in academic_terms
        ):

            bonus += 0.15

    # -------------------------
    # MPHIL BONUS
    # -------------------------

    if any(
        "mphil" in q
        for q in qualifications
    ):

        if (
            "research" in title
            or "education" in title
            or "curriculum" in title
        ):

            bonus += 0.08

    # -------------------------
    # LECTURER EXPERIENCE
    # -------------------------

    if (
        "lecturer"
        in experience
    ):

        if any(
            term in title
            for term in [

                "lecturer",
                "faculty",
                "professor",
                "educator"
            ]
        ):

            bonus += 0.10

    # -------------------------
    # RESEARCH EXPERIENCE
    # -------------------------

    if (
        "research officer"
        in experience
        or
        "research assistant"
        in experience
    ):

        if (
            "research"
            in title
            or
            "research"
            in skills_text
        ):

            bonus += 0.10

    # -------------------------
    # EDUCATION DOMAIN BOOST
    # -------------------------

    education_terms = [

        "education",
        "teaching",
        "training",
        "curriculum",
        "assessment",
        "learning"
    ]

    matches = sum(

        1

        for term in education_terms

        if (
            term in title
            or
            term in industry
            or
            term in skills_text
        )
    )

    bonus += (
        matches * 0.01
    )

    return bonus


# ==============================
# RECOMMENDATIONS
# ==============================

def recommend_jobs(
    cv_data,
    top_n=5
):

    cv_vector = vectorizer.transform(
        [
            cv_data["text"]
        ]
    )

    similarities = cosine_similarity(
        cv_vector,
        job_vectors
    )[0]

    recommendations = []

    for idx in range(
        len(similarities)
    ):

        row = job_metadata.iloc[idx]

        job_id = row["job_id"]

        skills = job_skill_lookup.get(
            job_id,
            []
        )

        industry = industry_lookup.get(
            job_id,
            "Unknown"
        )

        base_score = similarities[idx]

        bonus_score = get_job_bonus(

            cv_data,

            row["title"],

            industry,

            skills
        )

        final_score = (
            base_score +
            bonus_score
        )

        recommendations.append(
            {

                "idx": idx,

                "job_id": job_id,

                "score": final_score
            }
        )

    recommendations = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )[:top_n]

    results = []

    for item in recommendations:

        idx = item["idx"]

        row = job_metadata.iloc[idx]

        job_id = row["job_id"]

        skills = job_skill_lookup.get(
            job_id,
            []
        )

        salary_info = salary_lookup.get(
            job_id,
            {}
        )

        company_info = company_lookup.get(
            row["company_id"],
            {}
        )

        missing_skills = get_missing_skills(

            cv_data["skills"],

            skills
        )

        results.append(
            {

                "job_id":
                    job_id,

                "title":
                    row["title"],

                "company":
                    row["company_name"],

                "location":
                    row["location"],

                "industry":
                    industry_lookup.get(
                        job_id,
                        "Unknown"
                    ),

                "skills":
                    skills,

                "missing_skills":
                    missing_skills,

                "score":
                    round(
                        item["score"] * 100,
                        2
                    ),

                "company_size":
                    company_info.get(
                        "company_size",
                        "Unknown"
                    ),

                "company_description":
                    company_info.get(
                        "description",
                        "No description available"
                    ),

                "city":
                    company_info.get(
                        "city",
                        "N/A"
                    ),

                "country":
                    company_info.get(
                        "country",
                        "N/A"
                    ),

                "min_salary":
                    salary_info.get(
                        "min_salary"
                    ),

                "max_salary":
                    salary_info.get(
                        "max_salary"
                    ),

                "med_salary":
                    salary_info.get(
                        "med_salary"
                    ),

                "currency":
                    salary_info.get(
                        "currency"
                    )
            }
        )

    return results


# ==============================
# TEST RUN
# ==============================

if __name__ == "__main__":

    cv_data = analyze_cv(
        "uploads/SampleCV2.pdf"
    )

    recommendations = recommend_jobs(
        cv_data,
        top_n=5
    )

    print("\n" + "=" * 70)
    print("CAREERPILOT AI RECOMMENDATIONS")
    print("=" * 70)

    print("\nYOUR CV SKILLS:")
    print(
        cv_data["skills"]
    )

    for i, job in enumerate(
        recommendations,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"\n{i}. {job['title']}"
        )

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

                print(
                    f"  ✓ {skill}"
                )

        if job["missing_skills"]:

            print("\nMissing Skills:")

            for skill in job[
                "missing_skills"
            ][:5]:

                print(
                    f"  ✗ {skill}"
                )

        if (
            job["min_salary"]
            is not None
        ):

            print(
                f"\nSalary Range: "
                f"{job['currency']} "
                f"{job['min_salary']} - "
                f"{job['max_salary']}"
            )

        print(
            "\nCompany Description:"
        )

        description = str(
            job[
                "company_description"
            ]
        )

        print(
            description[:250]
            + "..."
        )