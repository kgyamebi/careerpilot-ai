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
# NAME EXTRACTION
# ============================

def extract_name(text):
    """
    Extract candidate name from
    the first few lines of CV.
    """

    lines = text.split("\n")

    for line in lines[:20]:

        line = line.strip()

        if not line:
            continue

        line_lower = line.lower()

        # Skip common headings
        if any(
            phrase in line_lower
            for phrase in [
                "curriculum vitae",
                "resume",
                "department",
                "university",
                "college",
                "email",
                "mobile",
                "phone",
                "address"
            ]
        ):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:

            alphabetic_words = [

                word

                for word in words

                if word.replace(
                    ".",
                    ""
                ).isalpha()
            ]

            if len(
                alphabetic_words
            ) >= 2:

                return line.title()

    return "CareerPilot Candidate"


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
            + re.escape(
                skill.lower()
            )
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found_skills.append(
                skill
            )

    return sorted(
        list(
            set(
                found_skills
            )
        )
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
        r"University of [A-Za-z ]+"
    )

    for line in lines:

        line = line.strip()

        if not line:
            continue

        institutions_found = re.findall(
            university_pattern,
            line,
            flags=re.IGNORECASE
        )

        for institution in institutions_found:

            institution = (
                institution.strip()
            )

            institution = re.sub(
                r"\s+PhD.*",
                "",
                institution
            )

            institution = re.sub(
                r"\s+MPhil.*",
                "",
                institution
            )

            institution = re.sub(
                r"\s+B\.Ed.*",
                "",
                institution
            )

            institutions.add(
                institution.strip()
            )

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
            sorted(
                list(
                    institutions
                )
            ),

        "qualifications":
            sorted(
                list(
                    qualifications
                )
            )
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

        if any(
            word in line.lower()
            for word in [

                "award",
                "scholarship",
                "publication",
                "journal",
                "book"
            ]
        ):
            continue

        for role in roles:

            pattern = (
                r"\b"
                + re.escape(
                    role.lower()
                )
                + r"\b"
            )

            if re.search(
                pattern,
                line.lower()
            ):

                experience.add(
                    line
                )

                break

    return sorted(
        list(
            experience
        )
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

            if level in (
                qualification.lower()
            ):

                return qualification

    return "Unknown"


# ============================
# SUMMARY GENERATION
# ============================

def generate_cv_summary(
    cv_data
):

    qualifications = (
        cv_data["education"]
        ["qualifications"]
    )

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
                cv_data[
                    "experience"
                ]
            )
    }


# ============================
# FULL CV ANALYSIS
# ============================

def analyze_cv(pdf_path):

    text = extract_text(
        pdf_path
    )

    cv_data = {

        "text":
            text,

        "name":
            extract_name(
                text
            ),

        "skills":
            extract_skills(
                text
            ),

        "education":
            extract_education(
                text
            ),

        "experience":
            extract_experience(
                text
            )
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

    cv_data = analyze_cv(
        "uploads/SampleCV2.pdf"
    )

    print("\n" + "=" * 50)
    print("NAME")
    print("=" * 50)
    print(
        cv_data["name"]
    )

    print("\n" + "=" * 50)
    print("SKILLS")
    print("=" * 50)
    print(
        cv_data["skills"]
    )

    print("\n" + "=" * 50)
    print("INSTITUTIONS")
    print("=" * 50)
    print(
        cv_data["education"]
        ["institutions"]
    )

    print("\n" + "=" * 50)
    print("QUALIFICATIONS")
    print("=" * 50)
    print(
        cv_data["education"]
        ["qualifications"]
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