import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.config.order_utils import insert_order, add_items_to_order
from app.config.database import get_cursor

from flask import jsonify
import random

# The number of random orders to generate
NUM_RANDOM_ORDERS = 50

# The total number of possible items in the database (with their ID's matching the quantity)
TOTAL_POSS_ITEM_COUNT = 30

def create_order(data):
    """
    Endpoint to create a new order.

    Expects a JSON payload with 'user_id' 'order_type' 'branch_id' 'price' and 'items'. A table number is also possible.

    Returns:
        Response: A JSON response with the order details or an error message.
    """

    price = data['price']
    user_id = data['user_id']
    order_type = data['order_type']
    table_number = data.get('table_number')
    items = data['items']
    branch_id = data['branch_id']
    try:
        order_id = insert_order(user_id, order_type, table_number, price, branch_id)
        add_items_to_order(order_id, items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def generate_a_random_order():
    """
    Generates a random order for dummy order data for the database.
    """
    # The price should be the total of all item prices, however, seen as this will be handled seperatley, we will dummify it for now.
    price = round(random.uniform(1.00, 100.00), 2)
    
    user_id = random.randint(1, 100)
    order_type = random.choice(["Delivery", "Takeaway", "Eat In"])
    branch_id = random.randint(1000,1005)

    random_items = [
        {"item_id": random.randint(1, TOTAL_POSS_ITEM_COUNT), "quantity": 1},
        {"item_id": random.randint(1, TOTAL_POSS_ITEM_COUNT), "quantity": random.randint(1, 2)},
        {"item_id": random.randint(1, TOTAL_POSS_ITEM_COUNT), "quantity": random.randint(1, 5)},
        {"item_id": random.randint(1, TOTAL_POSS_ITEM_COUNT), "quantity": random.randint(1, 3)},
    ]
    
    table_number = random.randint(1, 20) if order_type == "Eat In" else None

    items = random.sample(random_items, random.randint(1, len(random_items)))

    return {
        "price": price,
        "user_id": user_id,
        "order_type": order_type,
        "table_number": table_number,
        "items": items,
        "branch_id": branch_id
    }

def push_orders_to_database(count):
    """
    Pushes a given number of random orders to the database.
    """

    for i in range(count):
        data = generate_a_random_order()
        create_order(data)
        print("Order Number:", i+1, "Pushing order:", data)

def wipe_all_database_data():
    """
    Wipes all data from the database for a fresh batch.
    """

    try:
        with get_cursor() as cursor:
            # Ensure proper deletion order for tables with foreign key relationships
            cursor.execute("DELETE FROM order_item")  # Assuming it references orders
            cursor.execute("DELETE FROM orders")
            cursor.execute("DELETE FROM item")
            cursor.execute("DELETE FROM user")
        print("All database data wiped successfully.")

    except Exception as e:
        print(f"Error wiping database data: {e}")


wipe_all_database_data()
push_orders_to_database(NUM_RANDOM_ORDERS)
