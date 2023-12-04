import pandas as pd
import json
import os
from tqdm import tqdm

# Paths
json_dir = 'M:\Thesis\ArticleBiasPrediction\Article-Bias-Prediction-main\data\jsons'
csv_dir = 'M:\Thesis\POLUSA\polusa_balanced'


print("Indexing JSON data...")
# Indexing JSON data
json_urls = {}
for json_file_name in tqdm(os.listdir(json_dir)):
    json_file_path = os.path.join(json_dir, json_file_name)
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        json_urls[data['title']] = json_file_name


print("Indexing JSON data complete.")

print("Comparing Titles...")

# Processing CSV data and finding matches
matches = []
i = 1
for csv_file_name in tqdm(os.listdir(csv_dir), position = 0):
    print("Comparing titles for file " + str(i) + "...")
    i+=1
    csv_file_path = os.path.join(csv_dir, csv_file_name)
    csv_data = pd.read_csv(csv_file_path)
    for index, row in csv_data.iterrows():
        if row['headline'] in json_urls:
            matches.append({
                'csv_id': row['id'],
                'json_file': json_urls[row['headline']],
                'csv_file': csv_file_name,
                'csv_index': index
            })


pd.DataFrame(matches).to_csv('matches_titles.csv', index=False)
print("CSV file created, matches found: " + str(len(matches)))