import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os
import aiohttp
import asyncio

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

    async def fetch_warframe_market_orders(self, session, slug):
        url = f"https://api.warframe.market/v2/orders/item/{slug}/top"
        try:
            response = await session.get(url)
            if response.status == 200:
                return {slug: await response.json()}
            else:
                print(f"Failed to fetch data for item {slug}")
                return {}
        except aiohttp.ClientError as e:
            print(f"An error occurred while fetching the data for {slug}: {e}")
            return {}
    
    async def fetch_all_data(self, slugs):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_warframe_market_orders(session, slug) for slug in slugs]
            detailed_data = await asyncio.gather(*tasks)
            result = {}
            for data in detailed_data:
                result.update(data)
            return result

    def should_fetch_new_data(self):
        if not os.path.exists(self.filepath):
            return True

        last_modified_time = datetime.fromtimestamp(os.path.getmtime(self.filepath))
        current_time = datetime.now()
        time_difference = current_time - last_modified_time

        return time_difference > timedelta(days=7)

    def update_json_file(self, data):
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4) 

async def main():
    api = WarframeMarketAPI("https://api.warframe.market/v2/items", "warframe_market_data.json")
    if api.should_fetch_new_data():
        data = api.fetch_warframe_market_data()  # Fetch data synchronously
        # slugs = [item['slug'] for item in data['data']]
        # sorted_slugs = sorted(slugs)  # Sort the slugs alphabetically
        # print(sorted_slugs)
        detailed_data = await api.fetch_all_data(sorted_slugs)
        api.update_json_file(detailed_data)
    else:
        with open('sorted_slugs.json', 'r') as file:
            data = json.load(file)
        detailed_data = await api.fetch_all_data(data)
        api.update_json_file(detailed_data)
        
# Run the main function in an asyncio event loop
asyncio.run(main())


"""
# Fetch detailed data for each item
detailed_data = {}
last_modified_time = datetime.fromtimestamp(os.path.getmtime("pricedata.json"))
current_time = datetime.now()
time_difference = current_time - last_modified_time
if time_difference > timedelta(days=0):
    for slug in sorted_slugs:
        url = f"https://api.warframe.market/v2/orders/item/{slug}/top" 
        response = requests.get(url)
        if response.status_code == 200:
            detailed_data[slug] = json.loads(response.text)
            # print(slug, detailed_data[slug])
            print(f'working on gathering data... {slug}')
            print(f'Working on gathering data... {slug}')
        else:
            print(f"Failed to fetch data for item {slug}")
    with open(detailed_data_file, 'w') as file:
        json.dump(detailed_data, file, indent=4)
else:
    with open("pricedata.json", 'r') as file:
        detailed_data = json.load(file)
"""

"""
# Process and store the data
item_data = []
for slug, data in detailed_data.items():
    buy_orders = data['data']['buy']['stats_for_sale'][1]['orders']
    sell_orders = data['data']['sell']['stats_for_sale'][2]['orders']

    avg_buy_price = sum(order['price'] for order in buy_orders) / len(buy_orders)
    avg_sell_price = sum(order['price'] for order in sell_orders) / len(sell_orders)
    profit = avg_sell_price - avg_buy_price

    item_data.append({
        'item_name': data['payload']['item']['name'],
        'avg_buy_price': avg_buy_price,
        'avg_sell_price': avg_sell_price,
        'profit_per_item': profit
    })

# Create a DataFrame
df = pd.DataFrame(item_data)

# Sort by profit per item
df_sorted_by_profit = df.sort_values(by='profit_per_item', ascending=False)
print(df_sorted_by_profit.head())

# Plotting the data
plt.figure(figsize=(12, 8))

# Bar chart for profits
plt.subplot(1, 2, 1)
plt.barh(df['item_name'], df['profit_per_item'], color='skyblue')
plt.xlabel('Profit per Item')
plt.title('Item Profits')

# Line chart for historical prices (assuming we have historical data available)
# For simplicity, let's assume we have a function to fetch historical price data
def fetch_historical_prices(item_name):
    # Placeholder function to fetch historical prices
    return pd.DataFrame({
        'date': pd.date_range(start='1/1/2023', periods=10),
        'price': [i * 10 for i in range(1, 11)]
    })

historical_prices = {}
for item_name in df['item_name']:
    historical_prices[item_name] = fetch_historical_prices(item_name)

# Plotting historical prices
plt.subplot(1, 2, 2)
for item_name, price_data in historical_prices.items():
    plt.plot(price_data['date'], price_data['price'], label=item_name)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Historical Prices of Items')
plt.legend()

plt.tight_layout()
plt.show()
"""
