import os
import json
from collections import defaultdict, Counter
import csv
import tqdm

def process_json_files(folder_path):
    # Initialize a dictionary to store source and total article counts
    article_counts = defaultdict(int)

    # List all files in the directory
    file_list = os.listdir(folder_path)
    for filename in tqdm.tqdm(file_list):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                # Load the JSON data
                data = json.load(file)
                source = data['source']

                # Increment the article count for this source
                article_counts[source] += 1

    return article_counts


def read_allsides_data(file_path):
    stance_map = {}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            news_source = row['news_source']
            stance = row['rating']
            stance_map[news_source] = stance
    return stance_map

allsides_file_path = 'M:\Thesis\ArticleBiasPrediction\Python/allsides_data.csv'
stance_map = read_allsides_data(allsides_file_path)
folder_path = 'M:\Thesis\ArticleBiasPrediction\Article-Bias-Prediction-main\data\jsons'
article_counts = process_json_files(folder_path)

# Sort the sources by the total number of articles in descending order
sorted_sources = sorted(article_counts.items(), key=lambda x: x[1], reverse=True)

# Writing the sorted data to a CSV file with an additional column for political stance
csv_file_path = 'M:/Thesis/ArticleBiasPrediction/Python/news_article_counts_with_stance.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['News Company', 'Number of Articles', 'Political Stance (AllSides)'])

    for source, count in sorted_sources:
        political_stance = stance_map.get(source, 'Unknown')  # Get the political stance from the map
        csvwriter.writerow([source, count, political_stance])

print(f"CSV file created at {csv_file_path}")