import pandas as pd
import joblib

print("Loading industry mappings...")

job_industries = pd.read_csv(
    "data/linkedin/jobs/job_industries.csv"
)

industries = pd.read_csv(
    "data/linkedin/mappings/industries.csv"
)

industry_lookup = dict(
    zip(
        industries["industry_id"],
        industries["industry_name"]
    )
)

job_industry_lookup = {}

for _, row in job_industries.iterrows():

    job_id = row["job_id"]

    industry_id = row["industry_id"]

    industry_name = industry_lookup.get(
        industry_id
    )

    if industry_name:

        job_industry_lookup[job_id] = (
            industry_name
        )

joblib.dump(
    job_industry_lookup,
    "models/job_industry_lookup.pkl"
)

print(
    f"Industry mappings created: "
    f"{len(job_industry_lookup)}"
)
