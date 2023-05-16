import requests
from pymongo import MongoClient

# Connect to your MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['terraform']  # Use your database name here
collection = db['providers']  # Use your collection name here

# Define the base URL of the Terraform Registry API
base_url = 'https://registry.terraform.io'
url = f'{base_url}/v1/providers'

# Use a while loop to paginate through the results
while url:
    print(f"Fetching data from: {url}")
    
    # Make a GET request to the Terraform Registry API
    response = requests.get(url)
    data = response.json()

    offset = data['meta'].get('next_offset')

    # Insert the providers into the MongoDB collection
    for provider in data['providers']:
        collection.insert_one(provider)

    # Set the URL to the next page of results
    url = f"{url}?offset={offset}" if offset else None

    print(f"Providers fetched: {len(data['providers'])}")

print('Scraping completed.')
