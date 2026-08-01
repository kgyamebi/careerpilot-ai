import pdfplumber

# Skills database
SKILLS = [
    "Python",
    "Java",
    "SQL",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Machine Learning",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Flask",
    "Streamlit",
    "Statistics",
    "Research Methods",
    "Counselling",
    "Research",
    "Excel",
    "SPSS"
]


def extract_text(pdf_path):
    """
    Extract text from a PDF CV.
    """

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_skills(text):
    """
    Extract skills from CV text.
    """

    found_skills = []

    text = text.lower().replace("\n", " ")

    for skill in SKILLS:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def extract_education(text):
    """
    Extract education-related information.
    """

    education_keywords = [
        "University",
        "College",
        "Institute",
        "Bachelor",
        "Master",
        "Diploma",
        "Degree"
    ]

    education = []

    lines = text.split("\n")

    for line in lines:

        for keyword in education_keywords:

            if keyword.lower() in line.lower():

                education.append(line.strip())

                break

    return education


def extract_experience(text):
    """
    Extract experience-related information.
    """

    experience_keywords = [
        "Assistant",
        "Coordinator",
        "Manager",
        "Facilitator",
        "Representative",
        "Mentor",
        "President",
        "Vice-President",
        "Intern"
    ]

    experience = []

    lines = text.split("\n")

    for line in lines:

        for keyword in experience_keywords:

            if keyword.lower() in line.lower():

                experience.append(line.strip())

                break

    return experience


if __name__ == "__main__":

    cv_path = "uploads/SampleCV2.pdf"

    # Extract CV text
    cv_text = extract_text(cv_path)

    print("\n" + "=" * 50)
    print("CV TEXT")
    print("=" * 50)

    print(cv_text)

    # Extract skills
    skills = extract_skills(cv_text)

    print("\n" + "=" * 50)
    print("DETECTED SKILLS")
    print("=" * 50)

    print(skills)

    # Extract education
    education = extract_education(cv_text)

    print("\n" + "=" * 50)
    print("EDUCATION")
    print("=" * 50)

    for item in education:
        print(item)

    # Extract experience
    experience = extract_experience(cv_text)

    print("\n" + "=" * 50)
    print("EXPERIENCE")
    print("=" * 50)

    for item in experience:
        print(item)