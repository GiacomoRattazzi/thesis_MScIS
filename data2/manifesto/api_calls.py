import pandas as pd

api_key = '8b0c5b46bdb70725767476f8c2f62114'
dataset_key = "MPDS2023a"
version = '2023-1'
import requests

# def list_core_versions(api_key):
#     url = f"https://manifesto-project.wzb.eu/api/v1/list_metadata_versions?api_key=8b0c5b46bdb70725767476f8c2f62114&key=MPDS2017b"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Failed to fetch core versions:", response.text)
#         return []

def get_core_data(api_key, dataset_key):
    base_url = "https://manifesto-project.wzb.eu/api/v1/get_core"
    params = {
        "api_key": api_key,
        "key": dataset_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_metadata(api_key, keys, version):
    base_url = "https://manifesto-project.wzb.eu/api/v1/metadata"
    # Prepare parameters with keys as a list
    params = {
        "api_key": api_key,
        "keys[]": keys,  # keys is a list of key values
        "version": version
    }

    # Construct the full URL for debugging
    request_url = requests.Request('GET', base_url, params=params).prepare().url
    print("Request URL:", request_url)

    # Make the request
    response = requests.get(request_url)
    if response.status_code == 200:
        return response
    else:
        return None


def get_texts_and_annotations(api_key, manifesto_ids, version):
    base_url = "https://manifesto-project.wzb.eu/api/v1/texts_and_annotations"

    # Ensure manifesto_ids are unique and not None
    valid_manifesto_ids = [mid for mid in set(manifesto_ids) if mid is not None]

    params = {
        "api_key": api_key,
        "keys[]": valid_manifesto_ids,  # Pass all valid manifesto_ids
        "version": version
    }

    response = requests.get(base_url, params=params)
    texts = {}

    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            key = item.get('key')
            text_items = item.get('items', [])
            # Concatenate all texts for this key
            full_text = ' '.join([text_item.get('text', '') for text_item in text_items])
            texts[key] = full_text
    else:
        # If the response is not successful, you can decide how to handle this
        pass

    return texts


#
# def get_manifesto_texts(api_key, keys, version):
#     base_url = "https://manifesto-project.wzb.eu/api/v1/texts_and_annotations"
#     params = {
#         "api_key": api_key,
#         "keys[]": keys,
#         "version": version
#     }
#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None
#
# # Get the core data
# core_data = get_core_data(api_key, dataset_key)
#
# # Extract keys from core data
# keys = []
# if core_data and 'data' in core_data:
#     for item in core_data['data']:
#         party = item[6]  # Index for 'party'
#         date = item[5]   # Index for 'date'
#         keys.append(f"{party}_{date}")
#         print(date)
# # Example version - replace with actual value
# version = "20171211135550"




if __name__ == '__main__':
    # response = get_core_data(api_key, dataset_key)
    # df = pd.DataFrame(response)
    # # Filter for rows where 'countryname' is "United States"
    # us_data = df[df[1] == 'United States']
    #
    # # Select only the 'countryname', 'party', and 'date' columns
    # us_filtered_df = us_data[[1, 7, 5]]
    #
    # # Display the first few rows of the filtered DataFrame
    # print(us_filtered_df.head())

    response = get_core_data(api_key, dataset_key)
    headers = response[0]
    data = response[1:]

    # Creating DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Filtering for rows where 'countryname' is "United States"
    us_data = df[df['countryname'] == 'United States']

    # Selecting only the 'countryname', 'party', 'partyname', and 'date' columns
    us_filtered_df = us_data[['countryname', 'party', 'partyname', 'date']]
    us_filtered_df = us_filtered_df.copy()
    us_filtered_df.loc[:, 'keys'] = us_filtered_df['party'] + '_' + us_filtered_df['date']
    # Displaying the first few rows of the filtered DataFrame
    # print(us_filtered_df)

    keys = us_filtered_df['keys'].tolist()
    metadata_response = get_metadata(api_key, keys, "2023-1")

    if metadata_response:
        # Parse the JSON response
        data = metadata_response.json()

        # Create a dictionary to map each key to its manifesto_id
        id_map = {item['manifesto_id']: item.get('manifesto_id') for item in data.get('items', [])}

        # Add manifesto_ids to DataFrame
        us_filtered_df['manifesto_id'] = us_filtered_df['keys'].map(id_map)

    # Verify the DataFrame
    print(us_filtered_df.head())


    manifesto_ids = us_filtered_df['manifesto_id'].tolist()  # List of manifesto IDs
    # Fetch the texts and annotations
    texts = get_texts_and_annotations(api_key, manifesto_ids, version)

    # Add texts to DataFrame
    us_filtered_df['text'] = us_filtered_df['manifesto_id'].map(texts)

    # Verify the DataFrame
    print(us_filtered_df.head())
    us_filtered_df.to_csv('us_filtered.csv', index=False)
    us_filtered_df.to_json('us_filtered.json')
    us_filtered_df.to_excel('us_filtered.xlsx', index=False)