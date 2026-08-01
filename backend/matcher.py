from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.cv_analyzer import extract_text


def calculate_match_score(cv_text, job_text):
    """
    Calculate similarity between a CV and job description.
    """

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [cv_text, job_text]
    )

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )

    return round(similarity[0][0] * 100, 2)


if __name__ == "__main__":

    # Read CV directly from PDF
    cv_text = extract_text(
        "uploads/SampleCV2.pdf"
    )

    # Example psychology-related job
    job_description = """
    We are seeking a Research Assistant with experience in
    psychology, counselling, statistics, SPSS, data collection,
    academic research, and working with research participants.

    Responsibilities include conducting interviews, collecting data,
    performing statistical analysis, and contributing to research studies.
    """

    score = calculate_match_score(
        cv_text,
        job_description
    )

    print("\n" + "=" * 50)
    print("JOB MATCH SCORE")
    print("=" * 50)

    print(f"Match Score: {score}%")