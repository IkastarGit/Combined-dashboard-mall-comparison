import pandas as pd

# Load CSV
df = pd.read_csv("C:/Users/srira/Downloads/Book 1(Sheet1).csv", header=None)
df.columns = ["Tenants_List", "Other_List"]

# Normalize text
tenants = (
    df["Tenants_List"]
    .dropna()
    .astype(str)
    .str.lower()
    .str.strip()
)

other = (
    df["Other_List"]
    .dropna()
    .astype(str)
    .str.lower()
    .str.strip()
)

tenants_set = set(tenants)
other_set = set(other)

# Comparisons
present_in_both = sorted(tenants_set & other_set)
missing_in_other = sorted(tenants_set - other_set)
only_in_other = sorted(other_set - tenants_set)

# Results
print(" Tenants present in BOTH lists:")
for t in present_in_both:
    print("-", t)

print("\n Tenants MISSING in second list:")
for t in missing_in_other:
    print("-", t)

print("\n Entries ONLY in second list:")
for t in only_in_other:
    print("-", t)
