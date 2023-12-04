import pandas as pd
import json

# Loading the CSV file
csv_file = "M:\Thesis\data2\comparedatasets/climate_change_headlines.csv"
df = pd.read_csv(csv_file)

# Filter rows where the political leaning is 'RIGHT'
filtered_df = df[df['political_leaning'] == 'RIGHT']

# Write to a JSONL file
jsonl_file = 'right_leaning_articles.jsonl'

with open(jsonl_file, 'w') as file:
    for index, row in filtered_df.iterrows():
        # Create a JSON object with headline and body
        json_obj = {
            "headline": row['headline'],  # Replace 'headline' with the actual column name for headline
            "body": row['body']  # Replace 'body' with the actual column name for the article body
        }
        # Write JSON object to the file
        file.write(json.dumps(json_obj) + '\n')