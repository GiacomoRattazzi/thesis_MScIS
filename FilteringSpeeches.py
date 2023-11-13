import pandas as pd
from tqdm.auto import tqdm
import os

# Directory path
directory_path = 'M:\Thesis\DatasetStanford\hein-daily'

# Function to safely read CSV with different encodings
def read_csv_safe(file_path, sep='|'):
    encodings = ['utf-8', 'latin1', 'cp1252', 'ISO-8859-1', 'windows-1250', 'windows-1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, sep=sep, encoding=encoding, error_bad_lines=False, warn_bad_lines=True)
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError(f"None of the encodings worked for file {file_path}")

# Function to truncate speech to 512 words
def truncate_speech(speech):
    return ' '.join(str(speech).split()[:512])

# Define keywords for filtering speeches related to climate change
keywords = ['climate change', 'global warming', 'carbon emissions']

# Enable progress_apply with tqdm
tqdm.pandas()

# Process each set of files
all_metadata = pd.DataFrame()
all_speeches = pd.DataFrame()

for i in range(97, 115):  # Files are numbered from 097 to 114
    metadata_file = os.path.join(directory_path, f'descr_{i:03d}.txt')
    speeches_file = os.path.join(directory_path, f'speeches_{i:03d}.txt')
    speakermap_file = os.path.join(directory_path, f'{i:03d}_SpeakerMap.txt')

    metadata_df = read_csv_safe(metadata_file)
    speeches_df = read_csv_safe(speeches_file)
    speakermap_df = read_csv_safe(speakermap_file)

    # Merge speakermap to include party information in metadata
    metadata_df = metadata_df.merge(speakermap_df[['speech_id', 'party']], on='speech_id', how='left')

    # Filter and truncate speeches
    filtered_speeches_df = speeches_df[speeches_df['speech'].progress_apply(lambda x: any(keyword in str(x).lower() for keyword in keywords))]
    filtered_speeches_df['speech'] = filtered_speeches_df['speech'].progress_apply(truncate_speech)

    # Merge the filtered speeches with the metadata
    filtered_metadata_df = metadata_df.merge(filtered_speeches_df, on='speech_id')

    # Append to the final DataFrame
    all_metadata = pd.concat([all_metadata, filtered_metadata_df])
    all_speeches = pd.concat([all_speeches, filtered_speeches_df])

# Remove unnecessary columns and rows with missing party information
final_metadata = all_metadata.drop(columns=['number_within_file', 'line_start', 'line_end', 'file'])
final_metadata = final_metadata.dropna(subset=['party'])

# Saving the filtered data to new files
final_metadata.to_csv('filtered_metadata_with_party.csv', index=False)
all_speeches.to_csv('filtered_speeches_truncated.csv', index=False)

print("Filtering and merging complete. Files saved as 'filtered_metadata_with_party.csv' and 'filtered_speeches_truncated.csv'")
