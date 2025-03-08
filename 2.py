import json

# Assuming api.json is in the same directory as this script
with open('api.json', 'r') as file:
    data = json.load(file)

slugs = [item['slug'] for item in data['data']]

print(slugs)