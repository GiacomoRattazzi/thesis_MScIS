import pandas as pd
import os
from tqdm import tqdm

# Assuming all your filtered files are in a directory called 'filtered_files'
directory = 'M:\Thesis\data2\comparedatasets/filtered'

# List to store rows that match the criteria
matching_rows = []

# Iterate through each file in the directory
for filename in tqdm(os.listdir(directory)):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)

        # Check each row for 'climate change' in the headline
        for index, row in tqdm(df.iterrows(), position=0):
            if 'climate change' in str(row['headline']).lower():
                row['headline'] = row['headline'].lower() # make headline lowercase
                matching_rows.append(row)

# Create a DataFrame from the matching rows
new_df = pd.DataFrame(matching_rows)

# Save to a new CSV file
new_df.to_csv('climate_change_headlines.csv', index=False)
