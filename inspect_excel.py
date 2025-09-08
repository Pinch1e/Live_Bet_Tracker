import pandas as pd

# Load the Excel file
df = pd.read_excel('betting_summary.xlsx')

# Print the first few rows
print("First 5 rows:")
print(df.head())

# Print column names
print("\nColumn names:")
print(list(df.columns))

# Print data types
print("\nData types:")
print(df.dtypes)

# Print summary statistics
print("\nSummary statistics:")
print(df.describe())
