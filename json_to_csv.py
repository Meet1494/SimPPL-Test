import pandas as pd

# Load JSONL file
file_path = "data.jsonl"
df = pd.read_json(file_path, lines=True)

# Expand the 'data' column into separate columns
df_expanded = pd.json_normalize(df['data'])

# Save the flattened data as CSV
csv_path = "data.csv"
df_expanded.to_csv(csv_path, index=False)

# Check the new column names
print(df_expanded.columns)

print(f"CSV file saved at: {csv_path}")
