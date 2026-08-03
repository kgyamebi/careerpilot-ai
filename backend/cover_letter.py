from backend.cv_analyzer import analyze_cv
from backend.matcher_v3 import recommend_jobs


def get_best_skills(
    skills,
    limit=8
):
    """
    Select the most relevant skills
    for the cover letter.
    """

    priority_skills = [

        "Research",
        "SPSS",
        "Jamovi",

        "Education",
        "Science Education",

        "Teaching",
        "Training",

        "Curriculum Development",
        "Curriculum Studies",

        "Lesson Planning",

        "Microsoft Office"
    ]

    selected = []

    for skill in priority_skills:

        if skill in skills:

            selected.append(
                skill
            )

    for skill in skills:

        if skill not in selected:

            selected.append(
                skill
            )

        if len(selected) >= limit:

            break

    return selected[:limit]


def generate_cover_letter(
    cv_data,
    job
):
    """
    Generate personalized cover letter.
    """

    qualification = cv_data[
        "summary"
    ][
        "top_qualification"
    ]

    candidate_name = cv_data.get(
        "name",
        "CareerPilot Candidate"
    )

    skills = get_best_skills(
        cv_data["skills"]
    )

    skills_text = ", ".join(
        skills
    )

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the {job['title']} position at {job['company']}.

With a background in {qualification}, along with professional experience in education, research, teaching, training, and curriculum development, I am excited about the opportunity to contribute to your organization.

Throughout my academic and professional journey, I have developed expertise in {skills_text}. These experiences have strengthened my ability to conduct research, communicate effectively, support learning outcomes, and collaborate successfully with diverse stakeholders.

I am particularly excited about this opportunity because it aligns with my passion for continuous learning, knowledge sharing, educational development, and evidence-based research.

My academic qualifications and professional experience have equipped me with the skills necessary to make meaningful contributions while continuing to grow professionally within your organization.

Thank you for taking the time to review my application. I would welcome the opportunity to discuss how my qualifications, experience, and skills align with the needs of your organization.

Sincerely,

{candidate_name}
"""

    return cover_letter.strip()


if __name__ == "__main__":

    cv_data = analyze_cv(
        "uploads/SampleCV2.pdf"
    )

    recommendations = recommend_jobs(
        cv_data,
        top_n=1
    )

    job = recommendations[0]

    cover_letter = generate_cover_letter(
        cv_data,
        job
    )

    print("\n" + "=" * 60)
    print("GENERATED COVER LETTER")
    print("=" * 60)

    print("\n")
    print(cover_letter)

    output_file = (
        "docs/generated_cover_letter.txt"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            cover_letter
        )

    print(
        f"\n\nCover letter saved to:\n{output_file}"
    )