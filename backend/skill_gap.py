from backend.cv_analyzer import (
    extract_text,
    extract_skills
)


LEARNING_RESOURCES = {
    "Python": "Python for Everybody",
    "SQL": "SQLBolt",
    "Docker": "Docker Official Tutorial",
    "AWS": "AWS Cloud Practitioner Essentials",
    "Machine Learning": "Google Machine Learning Crash Course",
    "Git": "GitHub Skills",
    "Statistics": "Khan Academy Statistics"
}


def find_skill_gaps(cv_skills, required_skills):
    """
    Find skills required for a job that are missing from the CV.
    """

    missing_skills = []

    for skill in required_skills:

        if skill not in cv_skills:
            missing_skills.append(skill)

    return missing_skills


def calculate_skill_match(cv_skills, required_skills):
    """
    Calculate percentage match between CV skills
    and required job skills.
    """

    matched = 0

    for skill in required_skills:

        if skill in cv_skills:
            matched += 1

    return round(
        (matched / len(required_skills)) * 100,
        2
    )


def recommend_learning_resources(missing_skills):
    """
    Recommend learning resources for missing skills.
    """

    recommendations = {}

    for skill in missing_skills:

        if skill in LEARNING_RESOURCES:
            recommendations[skill] = LEARNING_RESOURCES[skill]

    return recommendations


if __name__ == "__main__":

    # Extract skills from CV
    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    cv_skills = extract_skills(
        cv_text
    )

    # Example job requirements
    required_skills = [
        "Statistics",
        "SPSS",
        "Research",
        "Python",
        "SQL",
        "Machine Learning",
        "Git"
    ]

    # Calculate skill gap
    missing_skills = find_skill_gaps(
        cv_skills,
        required_skills
    )

    # Calculate match %
    skill_match = calculate_skill_match(
        cv_skills,
        required_skills
    )

    # Learning recommendations
    recommendations = recommend_learning_resources(
        missing_skills
    )

    print("\n" + "=" * 50)
    print("SKILL GAP ANALYSIS")
    print("=" * 50)

    print(f"\nSkill Match Score: {skill_match}%")

    print("\nSkills Found In CV:")

    for skill in cv_skills:
        print(f"✓ {skill}")

    print("\nMissing Skills:")

    for skill in missing_skills:
        print(f"✗ {skill}")

    print("\nRecommended Learning Resources:")

    for skill, course in recommendations.items():
        print(f"{skill} → {course}")