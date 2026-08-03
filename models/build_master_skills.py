import pandas as pd


print("=" * 60)
print("BUILDING MASTER SKILLS DATABASE")
print("=" * 60)

# ----------------------------------
# Load custom skills
# ----------------------------------

print("\nLoading custom skills...")

with open(
    "data/skills.txt",
    "r",
    encoding="utf-8"
) as file:

    custom_skills = {
        line.strip()
        for line in file
        if line.strip()
    }

print(
    f"Custom skills loaded: {len(custom_skills)}"
)

# ----------------------------------
# Load LinkedIn skills
# ----------------------------------

print("\nLoading LinkedIn skills...")

linkedin_skills = pd.read_csv(
    "data/linkedin/mappings/skills.csv"
)

print(
    f"LinkedIn records loaded: {len(linkedin_skills)}"
)

# ----------------------------------
# Extract LinkedIn skill names
# ----------------------------------

linkedin_skill_set = set()

for skill in linkedin_skills["skill_name"]:

    if pd.notna(skill):

        linkedin_skill_set.add(
            str(skill).strip()
        )

print(
    f"Unique LinkedIn skills: {len(linkedin_skill_set)}"
)

# ----------------------------------
# Merge both sources
# ----------------------------------

master_skills = sorted(
    custom_skills.union(
        linkedin_skill_set
    )
)

print(
    f"Total merged skills: {len(master_skills)}"
)

# ----------------------------------
# Save master skills file
# ----------------------------------

output_file = "data/master_skills.txt"

with open(
    output_file,
    "w",
    encoding="utf-8"
) as file:

    for skill in master_skills:

        file.write(skill + "\n")

print("\nMaster skills file created.")

print(
    f"Saved to: {output_file}"
)

print(
    f"Final skill count: {len(master_skills)}"
)

print("\nDone.")