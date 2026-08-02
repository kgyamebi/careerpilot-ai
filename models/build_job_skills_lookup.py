import pandas as pd
import joblib

print("Loading skills data...")

job_skills = pd.read_csv(
    "data/linkedin/jobs/job_skills.csv"
)

skills = pd.read_csv(
    "data/linkedin/mappings/skills.csv"
)

# Convert abbreviations to names
skill_lookup = dict(
    zip(
        skills["skill_abr"],
        skills["skill_name"]
    )
)

job_skill_lookup = {}

for _, row in job_skills.iterrows():

    job_id = row["job_id"]

    skill_abr = row["skill_abr"]

    skill_name = skill_lookup.get(
        skill_abr
    )

    if skill_name:

        if job_id not in job_skill_lookup:
            job_skill_lookup[job_id] = []

        job_skill_lookup[job_id].append(
            skill_name
        )

joblib.dump(
    job_skill_lookup,
    "models/job_skill_lookup.pkl"
)

print(
    f"Jobs with skills: "
    f"{len(job_skill_lookup)}"
)