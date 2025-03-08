import json

with open("warframe_market_data.json", 'r') as file:
            data = json.load(file)

slugs = [item['slug'] for item in data['data']]
sorted_slugs = sorted(slugs)

with open('sorted_slugs.json', 'w') as f:
    json.dump(sorted_slugs, f, indent=4)