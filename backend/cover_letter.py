from backend.cv_analyzer import (
    extract_text,
    extract_skills
)


def generate_cover_letter(
    applicant_name,
    company_name,
    job_title,
    cv_skills
):
    """
    Generate a customized cover letter.
    """

    skills_text = ", ".join(cv_skills)

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company_name}.

I am confident that my background, skills, and experiences make me a strong candidate for this opportunity.

Through my education and professional experiences, I have developed valuable skills including {skills_text}. These experiences have strengthened my analytical thinking, communication, teamwork, research, and problem-solving abilities.

I am particularly excited about the opportunity to contribute to {company_name}, learn from experienced professionals, and continue developing my expertise in this field.

I believe my dedication, adaptability, and willingness to learn would allow me to make a meaningful contribution to your organization.

Thank you for your time and consideration. I appreciate the opportunity to apply for this position and would welcome the chance to discuss my qualifications further.

Sincerely,

{applicant_name}
"""

    return cover_letter


if __name__ == "__main__":

    # Read CV
    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    # Extract skills from CV
    cv_skills = extract_skills(
        cv_text
    )

    # Generate cover letter
    cover_letter = generate_cover_letter(
        applicant_name="John Doe",
        company_name="Health Research Institute",
        job_title="Research Assistant",
        cv_skills=cv_skills
    )

    print("\n" + "=" * 60)
    print("GENERATED COVER LETTER")
    print("=" * 60)

    print(cover_letter)

    # Save letter
    with open(
        "docs/generated_cover_letter.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(cover_letter)

    print("\nCover letter saved to:")
    print("docs/generated_cover_letter.txt")