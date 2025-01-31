import os
from app.config.order_utils import insert_item
import requests


def retrieve_dummy_item_data():
    """
    Retrieves dummy item data from the DummyDataAPI and inserts it into our database.
    """
    try:
        response = requests.get("http://dummydataapi:8010/menu/items") # Use docker images name when sending requests to it's API endpoint
        items = response.json()
        for item in items:
            item_id = item['id']
            name = item['name']
            price = float(item['price'])
            description = item['description']
            category = item['category']
            insert_item(item_id, name, description, category, price)
        return {'message': 'Items inserted successfully'}
    
    except Exception as e:
        return {'error': str(e)}

print(retrieve_dummy_item_data())