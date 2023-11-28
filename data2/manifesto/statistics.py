import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the JSON file
df = pd.read_json('us_filtered.json')

# Calculate the length of each text, handling None values
df['text_length'] = df['text'].apply(lambda x: len(x) if x is not None else 0)

# Remove rows where text length is 0
df = df[df['text_length'] > 0]

# Compute basic statistics
min_length = df['text_length'].min()
max_length = df['text_length'].max()
median_length = df['text_length'].median()
mean_length = df['text_length'].mean()

print("Minimum Length:", min_length)
print("Maximum Length:", max_length)
print("Median Length:", median_length)
print("Mean Length:", mean_length)

# Set the style for seaborn
sns.set(style="whitegrid")

# Create a bar plot for text lengths
plt.figure(figsize=(10, 6))
sns.barplot(x=df.index, y="text_length", data=df)
plt.title('Size of Each Text Document')
plt.xlabel('Document Index')
plt.ylabel('Text Length')
plt.show()
# Load the JSON file
df = pd.read_json('us_filtered.json')

# Calculate the length of each text, handling None values
df['text_length'] = df['text'].apply(lambda x: len(x) if x is not None else 0)

# Calculate the word count of each text
df['word_count'] = df['text'].apply(lambda x: len(x.split()) if x is not None else 0)

# Remove rows where text length is 0
df = df[df['text_length'] > 0]

# Select relevant columns (assuming 'text_name' or a similar column exists for the name of the text)
csv_columns = ['keys', 'text_length', 'word_count']

# Save to CSV
df[csv_columns].to_csv('text_length_word_count.csv', index=False)