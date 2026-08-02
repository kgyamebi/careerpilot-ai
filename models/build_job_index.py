import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading LinkedIn postings...")

# Load useful columns
df = pd.read_csv(
    "data/linkedin/postings.csv",
    usecols=[
        "job_id",
        "company_id",
        "company_name",
        "title",
        "description",
        "location"
    ]
)

print(f"Jobs Loaded: {len(df)}")

# Handle missing values
df["title"] = df["title"].fillna("")
df["description"] = df["description"].fillna("")
df["location"] = df["location"].fillna("")
df["company_name"] = df["company_name"].fillna("")
df["company_id"] = df["company_id"].fillna(-1)

# Create searchable text field
df["search_text"] = (
    df["title"]
    + " "
    + df["description"]
    + " "
    + df["location"]
)

print("Building TF-IDF vectors...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

job_vectors = vectorizer.fit_transform(
    df["search_text"]
)

print("Saving index...")

joblib.dump(
    job_vectors,
    "models/job_vectors.pkl"
)

joblib.dump(
    vectorizer,
    "models/job_vectorizer.pkl"
)

joblib.dump(
    df,
    "models/job_metadata.pkl"
)

print("\nIndex Built Successfully")
print(f"Indexed Jobs: {len(df)}")

print("\nSaved Files:")
print("- models/job_vectors.pkl")
print("- models/job_vectorizer.pkl")
print("- models/job_metadata.pkl")