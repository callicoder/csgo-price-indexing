import requests
from bs4 import BeautifulSoup
import json
import math
import time
from pymongo import MongoClient

def main():
	client = MongoClient('mongodb://localhost:27017/')
	db = client.csgo_pricing_db
	pricing = db.pricing

	url = 'http://steamcommunity.com/market/search/render/?start={0}&count=100&sort_column=price&sort_dir=asc&appid=730'
	request_url = url.format(0)
	response = requests.get(request_url)
	resp = json.loads(response.text)

	soup = BeautifulSoup(resp['results_html'], 'html.parser')
	market_item_rows = soup.find_all(name='div', class_='market_listing_row market_recent_listing_row market_listing_searchresult')
	for row in market_item_rows:
		marketing_hash_name = row.find(class_="market_listing_item_name").string
		market_hash_price = row.find(class_="market_listing_their_price").span.span.string
		market_hash_price = float(market_hash_price[1:-4])
		pricing_data= {"market_hash_name": marketing_hash_name, "market_hash_price":market_hash_price}
		pricing.update({"market_hash_name": marketing_hash_name}, {"$set": {"market_hash_price":market_hash_price}}, upsert=True)

	for i in range(1, int(math.ceil(float(resp['total_count'])/100))+1):
		request_url = url.format(i*100)
		response = requests.get(request_url)
		resp = json.loads(response.text)

		soup = BeautifulSoup(resp['results_html'], 'html.parser')
		market_item_rows = soup.find_all(name='div', class_='market_listing_row market_recent_listing_row market_listing_searchresult')
		for row in market_item_rows:
			marketing_hash_name = row.find(class_="market_listing_item_name").string
			market_hash_price = row.find(class_="market_listing_their_price").span.span.string
			market_hash_price = float(market_hash_price[1:-4])
			pricing_data= {"market_hash_name": marketing_hash_name, "market_hash_price":market_hash_price}
			pricing.update({"market_hash_name": marketing_hash_name}, {"$set": {"market_hash_price":market_hash_price}}, upsert=True)
		time.sleep(10)	
			

if __name__ == '__main__':
	main()

