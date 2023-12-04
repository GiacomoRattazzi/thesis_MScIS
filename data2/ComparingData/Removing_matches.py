import pandas as pd
import os
from tqdm import tqdm

# Paths
csv_dir = 'M:\Thesis\POLUSA\polusa_balanced'
matched_articles_file = 'matches_content.csv'
matched_titles_file = 'matches_titles.csv'

# Load matched IDs from both files
matched_articles_ids = set(pd.read_csv(matched_articles_file)['csv_id'])
matched_titles_ids = set(pd.read_csv(matched_titles_file)['csv_id'])
all_matched_ids = matched_articles_ids.union(matched_titles_ids)

# Process each CSV file and remove matching rows
rows_removed_count = {}
for csv_file_name in tqdm(os.listdir(csv_dir)):
    if csv_file_name.endswith('.csv'):  # Process only CSV files
        csv_file_path = os.path.join(csv_dir, csv_file_name)
        csv_data = pd.read_csv(csv_file_path)

        # Filter out rows with matched IDs
        filtered_data = csv_data[~csv_data['id'].isin(all_matched_ids)]
        rows_removed = len(csv_data) - len(filtered_data)
        rows_removed_count[csv_file_name] = rows_removed

        # Save the filtered CSV in the current working directory
        filtered_csv_path = f"filtered_{csv_file_name}"
        filtered_data.to_csv(filtered_csv_path, index=False)

# Print the total rows removed by file
for file, count in rows_removed_count.items():
    print(f"Total rows removed from {file}: {count}")