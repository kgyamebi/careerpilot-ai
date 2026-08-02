import pandas as pd

df = pd.read_csv(
    "data/linkedin/postings.csv",
    nrows=3
)

print("\nColumns:")
print(df.columns.tolist())

print("\nSample Data:")
print(df.head(3))