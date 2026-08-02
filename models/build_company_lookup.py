import pandas as pd
import joblib

print("Loading companies...")

companies = pd.read_csv(
    "data/linkedin/companies/companies.csv"
)

company_lookup = companies.set_index(
    "company_id"
).to_dict(
    orient="index"
)

joblib.dump(
    company_lookup,
    "models/company_lookup.pkl"
)

print(
    f"Companies indexed: {len(company_lookup)}"
)