from collections import Counter
import statistics

from backend.matcher_v3 import (
    recommend_jobs
)

from backend.cv_analyzer import (
    extract_text,
    extract_skills
)


def generate_career_insights(recommendations):

    industries = []
    missing_skills = []
    salaries = []

    for job in recommendations:

        # Industries
        if job["industry"] != "Unknown":
            industries.append(
                job["industry"]
            )

        # Missing skills
        missing_skills.extend(
            job["missing_skills"]
        )

        # Salaries
        if job["med_salary"] is not None:
            try:
                salaries.append(
                    float(job["med_salary"])
                )
            except:
                pass

        elif job["max_salary"] is not None:
            try:
                salaries.append(
                    float(job["max_salary"])
                )
            except:
                pass

    top_industries = Counter(
        industries
    ).most_common(5)

    top_missing_skills = Counter(
        missing_skills
    ).most_common(10)

    average_salary = None

    if salaries:
        average_salary = round(
            statistics.mean(salaries),
            2
        )

    return {
        "top_industries": top_industries,
        "top_missing_skills": top_missing_skills,
        "average_salary": average_salary
    }


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
        top_n=10
    )

    insights = generate_career_insights(
        recommendations
    )

    print("\n" + "=" * 70)
    print("CAREER INSIGHTS")
    print("=" * 70)

    print("\nTOP INDUSTRIES:")

    for industry, count in insights[
        "top_industries"
    ]:

        print(
            f"• {industry} ({count})"
        )

    print("\nTOP MISSING SKILLS:")

    for skill, count in insights[
        "top_missing_skills"
    ]:

        print(
            f"• {skill} ({count})"
        )

    print("\nAVERAGE RECOMMENDED SALARY:")

    if insights["average_salary"]:

        print(
            f"USD {insights['average_salary']:,.2f}"
        )

    else:

        print("Salary information unavailable")