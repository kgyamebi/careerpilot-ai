import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv(
    "data/fake_job_postings.csv"
)

print("Dataset Loaded")

# Combine important text features
df["text"] = (
    df["title"].fillna("")
    + " "
    + df["description"].fillna("")
    + " "
    + df["requirements"].fillna("")
    + " "
    + df["company_profile"].fillna("")
)

# Features and target
X = df["text"]

y = df["fraudulent"]

# Convert text to vectors
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_vectors = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectors,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Model...")

# Train model
model = LogisticRegression(
    max_iter=1000
)

model.fit(
    X_train,
    y_train
)

# Predict
predictions = model.predict(
    X_test
)

# Accuracy
accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n" + "=" * 50)
print("SCAM DETECTOR RESULTS")
print("=" * 50)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

# Save model
joblib.dump(
    model,
    "models/scam_detector_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

print("\nModel Saved Successfully")