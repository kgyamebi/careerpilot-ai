import pdfplumber
import re


# ============================
# LOAD MASTER SKILLS DATABASE
# ============================

with open(
    "data/master_skills.txt",
    "r",
    encoding="utf-8"
) as file:

    SKILLS = [
        skill.strip()
        for skill in file.readlines()
        if skill.strip()
    ]


# ============================
# PDF TEXT EXTRACTION
# ============================

def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    return text


# ============================
# SKILLS EXTRACTION
# ============================

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if len(skill) < 3:
            continue

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(
        list(set(found_skills))
    )


# ============================
# EDUCATION EXTRACTION
# ============================

def extract_education(text):

    institutions = set()

    qualification_patterns = [

        r"\bPhD\s+[A-Za-z ]+",
        r"\bMPhil\s+[A-Za-z ]+",
        r"\bMSc\s+[A-Za-z ]+",
        r"\bMBA\s+[A-Za-z ]+",

        r"\bBSc\s+[A-Za-z ]+",
        r"\bB\.Sc\.?\s+[A-Za-z ]+",

        r"\bBEd\s+[A-Za-z ]+",
        r"\bB\.Ed\.?\s+[A-Za-z ]+",

        r"\bBA\s+[A-Za-z ]+",
        r"\bB\.A\.?\s+[A-Za-z ]+"
    ]

    qualifications = set()

    lines = text.split("\n")

    university_pattern = (
        r"(University of [A-Za-z ]+)"
    )

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # -----------------
        # Institutions
        # -----------------

        institutions_found = re.findall(
            university_pattern,
            line,
            flags=re.IGNORECASE
        )

        for institution in institutions_found:

            institutions.add(
                institution.strip()
            )

        # -----------------
        # Qualifications
        # -----------------

        for pattern in qualification_patterns:

            matches = re.findall(
                pattern,
                line,
                flags=re.IGNORECASE
            )

            for match in matches:

                qualifications.add(
                    match.strip()
                )

    return {

        "institutions":
            sorted(list(institutions)),

        "qualifications":
            sorted(list(qualifications))
    }


# ============================
# EXPERIENCE EXTRACTION
# ============================

def extract_experience(text):

    roles = [

        "Assistant Lecturer",
        "Lecturer",
        "Professor",

        "Research Officer",
        "Research Assistant",

        "Teacher",
        "Science Teacher",

        "Tutor",
        "Instructor",

        "Coordinator",
        "Manager",

        "Administrator",
        "Trainer",
        "Facilitator",

        "Consultant",
        "Engineer",

        "Analyst",
        "Technician",

        "Developer",
        "Supervisor"
    ]

    experience = set()

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if len(line) > 120:
            continue

        if (
            "award" in line.lower()
            or "scholarship" in line.lower()
            or "publication" in line.lower()
        ):
            continue

        for role in roles:

            pattern = (
                r"\b"
                + re.escape(role.lower())
                + r"\b"
            )

            if re.search(
                pattern,
                line.lower()
            ):

                experience.add(line)

                break

    return sorted(
        list(experience)
    )


# ============================
# HIGHEST QUALIFICATION
# ============================

def get_top_qualification(
    qualifications
):

    priority = [

        "phd",
        "mphil",
        "msc",
        "mba",
        "bsc",
        "b.ed",
        "ba"
    ]

    for level in priority:

        for qualification in qualifications:

            if level in qualification.lower():

                return qualification

    return "Unknown"


# ============================
# SUMMARY
# ============================

def generate_cv_summary(
    cv_data
):

    qualifications = cv_data[
        "education"
    ]["qualifications"]

    return {

        "top_qualification":
            get_top_qualification(
                qualifications
            ),

        "skills_count":
            len(
                cv_data["skills"]
            ),

        "experience_count":
            len(
                cv_data["experience"]
            )
    }


# ============================
# FULL ANALYSIS
# ============================

def analyze_cv(pdf_path):

    text = extract_text(
        pdf_path
    )

    cv_data = {

        "text": text,

        "skills":
            extract_skills(text),

        "education":
            extract_education(text),

        "experience":
            extract_experience(text)
    }

    cv_data["summary"] = (
        generate_cv_summary(
            cv_data
        )
    )

    return cv_data


# ============================
# TEST RUN
# ============================

if __name__ == "__main__":

    cv_path = "uploads/SampleCV2.pdf"

    cv_data = analyze_cv(
        cv_path
    )

    print("\n" + "=" * 50)
    print("SKILLS")
    print("=" * 50)
    print(cv_data["skills"])

    print("\n" + "=" * 50)
    print("INSTITUTIONS")
    print("=" * 50)
    print(
        cv_data["education"][
            "institutions"
        ]
    )

    print("\n" + "=" * 50)
    print("QUALIFICATIONS")
    print("=" * 50)
    print(
        cv_data["education"][
            "qualifications"
        ]
    )

    print("\n" + "=" * 50)
    print("EXPERIENCE")
    print("=" * 50)
    print(
        cv_data["experience"]
    )

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(
        cv_data["summary"]
    )