SCAM_INDICATORS = [
    "application fee",
    "registration fee",
    "pay before interview",
    "send money",
    "wire transfer",
    "guaranteed job",
    "work from home and earn",
    "no experience needed",
    "urgent hiring",
    "immediate start",
    "contact via whatsapp only"
]


def detect_scam(job_text):
    """
    Detect potential scam indicators in a job posting.
    """

    detected_flags = []

    job_text = job_text.lower()

    for phrase in SCAM_INDICATORS:

        if phrase.lower() in job_text:
            detected_flags.append(phrase)

    return detected_flags


def calculate_risk_score(detected_flags):

    max_flags = len(SCAM_INDICATORS)

    risk_score = (
        len(detected_flags) / max_flags
    ) * 100

    return round(risk_score, 2)


if __name__ == "__main__":

    sample_job = """
    URGENT HIRING!

    Work from home and earn $5000 weekly.

    No experience needed.

    Pay a registration fee before interview.

    Contact via WhatsApp only.
    """

    flags = detect_scam(sample_job)

    risk_score = calculate_risk_score(flags)

    print("\n" + "=" * 50)
    print("SCAM DETECTOR")
    print("=" * 50)

    print(f"\nScam Risk Score: {risk_score}%")

    print("\nDetected Red Flags:")

    for flag in flags:
        print(f"⚠ {flag}")