import requests
import os

# Set the base URL and API key
BASE_URL = "http://localhost:5002/api"
API_KEY = os.getenv('API_KEY')  # Ensure this is set in your environment

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_orders():
    """
    Fetch all orders from the API.
    """
    response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)
    return response.json()

def create_order(user_id, order_type, branch_id, price, items, table_number=None):
    """
    Create a new order.
    """
    data = {
        "user_id": user_id,
        "order_type": order_type,
        "branch_id": branch_id,
        "price": price,
        "items": items
    }
    if table_number:
        data["table_number"] = table_number
    
    response = requests.post(f"{BASE_URL}/orders/create", json=data, headers=HEADERS)
    return response.json()

def view_order(order_id):
    """
    View details of a specific order.
    """
    response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
    return response.json()

def update_status(order_id, new_status):
    """
    Update the status of an order.
    """
    data = {"new_status": new_status}
    response = requests.put(f"{BASE_URL}/orders/{order_id}/status", json=data, headers=HEADERS)
    return response.json()

def amend_order_items(order_id, items):
    """
    Amend the items in an order.
    """
    data = {"items": items}
    response = requests.put(f"{BASE_URL}/orders/{order_id}/items", json=data, headers=HEADERS)
    return response.json()

def delete_order(order_id):
    """
    Delete an order.
    """
    response = requests.delete(f"{BASE_URL}/orders/{order_id}/delete", headers=HEADERS)
    return response.json()

def get_orders_by_date(start_date, end_date):
    """
    Fetch orders in a specific date range.
    """
    data = {
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(f"{BASE_URL}/orders/date", json=data, headers=HEADERS)
    return response.json()

def get_orders_items_quantity_by_date(start_date, end_date):
    """
    Fetch orders with item quantities in a date range.
    """
    data = {
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(f"{BASE_URL}/orders/items/quantity/date", json=data, headers=HEADERS)
    return response.json()

def get_orders_extended():
    """
    Fetch all orders with extended information.
    """
    response = requests.get(f"{BASE_URL}/orders/extended", headers=HEADERS)
    return response.json()

def get_popular_items(start_date, end_date):
    """
    Fetch the most popular items.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/orders/popular-item",
            headers=HEADERS,
            params={
                'start_date': start_date,
                'end_date': end_date
            }
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

result = get_popular_items("2023-01-01", "2023-12-")
print(result)

