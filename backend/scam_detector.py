import joblib

# Load trained model
model = joblib.load(
    "models/scam_detector_model.pkl"
)

# Load TF-IDF vectorizer
vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


def predict_job(job_text):

    vector = vectorizer.transform(
        [job_text]
    )

    prediction = model.predict(vector)[0]

    probabilities = model.predict_proba(vector)[0]

    return prediction, probabilities


if __name__ == "__main__":

    sample_job = """
    Work from home and earn $5000 per week.

    No experience required.

    Immediate start.

    Send money before interview.

    Contact via WhatsApp only.
    """

    prediction, probabilities = predict_job(
        sample_job
    )

    legitimate_probability = probabilities[0] * 100
    fraudulent_probability = probabilities[1] * 100

    print("\n" + "=" * 50)
    print("SCAM DETECTOR")
    print("=" * 50)

    if prediction == 1:

        print("\n⚠ Likely Scam Job")

    else:

        print("\n✅ Likely Legitimate Job")

    print(
        f"\nLegitimate Probability: "
        f"{legitimate_probability:.2f}%"
    )

    print(
        f"Fraudulent Probability: "
        f"{fraudulent_probability:.2f}%"
    )