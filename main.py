import json
import requests
from datetime import datetime, timedelta

class WarframeMarketAPI:
    def __init__(self, url, filepath):
        self.url = url
        self.filepath = filepath

    def fetch_warframe_market_data(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                raise Exception("Failed to fetch data from warframe.market with status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            raise Exception("An error occurred while fetching the data:", str(e))

    def should_fetch_new_data(self):
        import os
        if not os.path.exists(self.filepath):
            return True

        last_modified_time = datetime.fromtimestamp(os.path.getmtime(self.filepath))
        current_time = datetime.now()
        time_difference = current_time - last_modified_time

        return time_difference > timedelta(days=7)

    def update_json_file(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)

# Example usage
api = WarframeMarketAPI("https://api.warframe.market/v2/items", "warframe_market_data.json")
if api.should_fetch_new_data():
    data = api.fetch_warframe_market_data()
    api.update_json_file(data)
else:
    with open(api.filepath, 'r') as file:
        data = json.load(file)

print(data)

# Extract all the "slug" keys
slugs = [item['slug'] for item in data['data']]
sorted_slugs = sorted(slugs)  # Sort the slugs alphabetically

print(sorted_slugs)