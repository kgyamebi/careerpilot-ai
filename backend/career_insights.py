from collections import Counter
import statistics
import pandas as pd

from backend.cv_analyzer import analyze_cv
from backend.matcher_v3 import recommend_jobs


# ==================================
# TOP INDUSTRIES
# ==================================

def get_top_industries(recommendations):

    industries = []

    for job in recommendations:

        industry = job.get(
            "industry",
            "Unknown"
        )

        if industry:

            industries.append(
                industry
            )

    return Counter(
        industries
    ).most_common(5)


# ==================================
# MISSING SKILLS
# ==================================

def get_most_common_missing_skills(
    recommendations
):

    missing_skills = []

    for job in recommendations:

        missing_skills.extend(
            job.get(
                "missing_skills",
                []
            )
        )

    return Counter(
        missing_skills
    ).most_common(10)


# ==================================
# SALARY INSIGHTS
# ==================================

def get_salary_insights(
    recommendations
):

    salaries = []

    currency = "USD"

    for job in recommendations:

        min_salary = job.get(
            "min_salary"
        )

        max_salary = job.get(
            "max_salary"
        )

        med_salary = job.get(
            "med_salary"
        )

        salary = None

        # -------------------------
        # First choice:
        # Median salary
        # -------------------------

        if pd.notna(
            med_salary
        ):

            salary = float(
                med_salary
            )

        # -------------------------
        # Fallback:
        # Midpoint
        # -------------------------

        elif (

            pd.notna(
                min_salary
            )

            and

            pd.notna(
                max_salary
            )

        ):

            salary = (

                float(
                    min_salary
                )

                +

                float(
                    max_salary
                )

            ) / 2

        if salary is not None:

            salaries.append(
                salary
            )

            if job.get(
                "currency"
            ):

                currency = job[
                    "currency"
                ]

    if not salaries:

        return {

            "currency":
                currency,

            "average":
                None,

            "minimum":
                None,

            "maximum":
                None,

            "salary_records":
                0
        }

    return {

        "currency":
            currency,

        "average":
            round(
                statistics.mean(
                    salaries
                ),
                2
            ),

        "minimum":
            round(
                min(salaries),
                2
            ),

        "maximum":
            round(
                max(salaries),
                2
            ),

        "salary_records":
            len(salaries)
    }


# ==================================
# INSIGHT GENERATOR
# ==================================

def generate_career_insights(
    cv_data,
    top_n=10
):

    recommendations = recommend_jobs(
        cv_data,
        top_n=top_n
    )

    industries = get_top_industries(
        recommendations
    )

    missing_skills = (
        get_most_common_missing_skills(
            recommendations
        )
    )

    salary_info = get_salary_insights(
        recommendations
    )

    return {

        "industries":
            industries,

        "missing_skills":
            missing_skills,

        "salary":
            salary_info,

        "recommendations":
            recommendations
    }


# ==================================
# TEST RUN
# ==================================

if __name__ == "__main__":

    cv_data = analyze_cv(
        "uploads/SampleCV2.pdf"
    )

    insights = generate_career_insights(
        cv_data,
        top_n=10
    )

    print("\n" + "=" * 60)
    print("CAREER INSIGHTS")
    print("=" * 60)

    print("\nTOP INDUSTRIES")

    for industry, count in (
        insights["industries"]
    ):

        print(
            f"- {industry} ({count})"
        )

    print(
        "\nTOP MISSING SKILLS"
    )

    for skill, count in (
        insights["missing_skills"]
    ):

        print(
            f"- {skill} ({count})"
        )

    salary = insights["salary"]

    print(
        "\nSALARY INSIGHTS"
    )

    if salary["average"] is None:

        print(
            "No salary data available."
        )

    else:

        print(
            f"Average Salary: "
            f"{salary['currency']} "
            f"{salary['average']}"
        )

        print(
            f"Minimum Salary: "
            f"{salary['currency']} "
            f"{salary['minimum']}"
        )

        print(
            f"Maximum Salary: "
            f"{salary['currency']} "
            f"{salary['maximum']}"
        )

        print(
            f"Based on "
            f"{salary['salary_records']} "
            f" salary record(s)."
        )