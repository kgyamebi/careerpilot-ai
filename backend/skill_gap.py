from backend.cv_analyzer import (
    extract_text,
    extract_skills
)


def find_skill_gaps(cv_skills, required_skills):

    missing_skills = []

    for skill in required_skills:

        if skill not in cv_skills:
            missing_skills.append(skill)

    return missing_skills


if __name__ == "__main__":

    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    cv_skills = extract_skills(cv_text)

    required_skills = [
        "Statistics",
        "SPSS",
        "Research",
        "Python",
        "SQL"
    ]

    missing_skills = find_skill_gaps(
        cv_skills,
        required_skills
    )

    print("\nCV Skills:")
    print(cv_skills)

    print("\nRequired Skills:")
    print(required_skills)

    print("\nMissing Skills:")
    print(missing_skills)