import pandas as pd
import joblib

print("Loading salary data...")

salary_df = pd.read_csv(
    "data/linkedin/jobs/salaries.csv"
)

salary_lookup = salary_df.set_index(
    "job_id"
).to_dict(
    orient="index"
)

joblib.dump(
    salary_lookup,
    "models/salary_lookup.pkl"
)

print(
    f"Salary records indexed: {len(salary_lookup)}"
)