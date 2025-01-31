from app.config.database import get_cursor, encrypt_data, decrypt_data
from datetime import datetime
from flask import jsonify
import requests
# -------------------- Validation Functions -------------------- #

def validate_order_data(data):
    """
    Validates the order data received in the request.

    Args:
        data (dict): The JSON data from the request containing 'user_id' and 'items'.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not data.get('user_id'):
        return False
    if not data.get('items') or not isinstance(data['items'], list):
        return False
    return all('item_id' in item for item in data['items'])



# -------------------- CRUD Helper Functions -------------------- #

def fetch_all_orders_by_branch_id(branch_id):
    """
    Fetches all orders from the database by branch ID.
    
    Args:
        branch_id (int): The ID of the branch to fetch orders for.
    
    Returns:
        list: A list of dictionaries containing order details.
    """
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE branch_id = ?", (branch_id,))
        orders = cursor.fetchall()
        
        all_orders = []
        for order in orders:
            cursor.execute("SELECT * FROM order_item WHERE order_id = ?", (order[0],))
            items = cursor.fetchall()
            all_orders.append({
                'order_id': order[0],
                'user_id': decrypt_data(order[1]),
                'order_date': order[2],
                'status': order[3],
                'order_type': decrypt_data(order[4]),
                'table_number': order[5],
                'price': order[6],
                'branch_id': order[7],
                'items': [
                    {
                        'item_id': decrypt_data(item[1]),  
                        'quantity': decrypt_data(item[2]),  
                        'modifications': decrypt_data(item[3])
                    } for item in items
                ]
            })
        return all_orders

def insert_order(user_id, order_type, table_number, price, branch_id):
    """Insert a new order into the database.

    Args:
        user_id (int): The ID of the user placing the order.
        order_type (str): The type of the order ('Eat In', 'Takeaway', 'Delivery').
        table_number (int or None): The table number if applicable, otherwise None.
        price (real): The total price of the order.
        branch_id (int): The ID of the branch where the order is / was placed.

    Returns:
        int: The ID of the newly created order.
    """
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO orders (user_id, order_date, order_status, order_type, table_number, price, branch_id)
            VALUES (?, datetime('now'), 'PENDING', ?, ?, ?, ?)
            """,
            (encrypt_data(str(user_id)), order_type, table_number, price, branch_id)
        )
        return cursor.lastrowid

def insert_item(item_id, name, description, category, price):
    """Insert a new item into the database.

    Args:
        item_id (int): The ID of the item.
        name (str): The name of the item.
        description (str): The description of the item.
        category (str): The category of the item.
        price (real): The price of the item.
    """
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO item (id, name, description, category, price) VALUES (?, ?, ?, ?, ?)",
            (item_id, name, description, category, price)
    )
def add_items_to_order(order_id, items):
    """
    Adds items to the order in the database.

    Args:
        order_id (int): The ID of the order to which items are being added.
        items (list): A list of item dictionaries, each containing 'item_id', 'quantity', and optional 'modifications'.
    """
    with get_cursor() as cursor:
        for item in items:
            cursor.execute(
                "INSERT INTO order_item (order_id, item_id, quantity, modifications) VALUES (?, ?, ?, ?)",
                (order_id, item['item_id'], encrypt_data(str(item.get('quantity', 1))), encrypt_data(item.get('modifications', '')))
            )

def get_order_by_id(order_id):
    """
    Retrieves an order from the database by its ID.
    
    Args:
        order_id (int): The ID of the order to retrieve.
    Returns:
        dict: A dictionary containing the order details. 
    """
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        if not order:
            return None
        
        cursor.execute("SELECT * FROM order_item WHERE order_id = ?", (order_id,))
        items = cursor.fetchall()
        
        return {
            'order_id': order[0],
            'user_id': decrypt_data(order[1]),
            'order_date': order[2],
            'status': order[3],
            'order_type': decrypt_data(order[4]),
            'table_number': order[5],
            'price': order[6],
            'branch_id': order[7],
            'items': [
                {
                    'item_id': decrypt_data(item[1]),  
                    'quantity': decrypt_data(item[2]),  
                    'modifications': decrypt_data(item[3])
                } for item in items
            ]
        }

def delete_order_items(order_id):
    """
    Deletes all items from the item-order table based on an order_id

    Args:
        order_id (int): The ID of the order to delete all items associated with it
    
    Returns:
        bool: True on successfull deletion of all items, False if failed

    """

    with get_cursor() as cursor:
        cursor.execute("DELETE FROM order_item WHERE order_id = ?", (order_id,))

        return cursor.rowcount > 0

# -------------------- Order Processing -------------------------- #
    
def update_order_status(order_id, new_status):
    """
    Updates the status of an order in the database.

    Args:
        order_id (int): The ID of the order to update.
        new_status (str): The new status to assign to the order.

    Returns:
        bool: True if the update was successful, False otherwise.
    """

    with get_cursor() as cursor:
        
        cursor.execute(
            "UPDATE orders SET order_status = ? WHERE order_id = ?",
            (new_status, order_id)
        )

        return cursor.rowcount > 0 

# -------------------- Reporting and Fetching -------------------- #

def fetch_all_orders():
    """
    Fetches all orders from the database.
    
    Returns:
        list: A list of dictionaries containing order details.
    """
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        
        all_orders = []
        for order in orders:
            cursor.execute("SELECT * FROM order_item WHERE order_id = ?", (order[0],))
            items = cursor.fetchall()
            all_orders.append({
                'order_id': order[0],
                'user_id': decrypt_data(order[1]),
                'order_date': order[2],
                'status': order[3],
                'order_type': decrypt_data(order[4]),
                'table_number': order[5],
                'price': order[6],
                'branch_id': order[7],
                'items': [
                    {
                        'item_id': decrypt_data(item[2]),  
                        'quantity': decrypt_data(item[3]),  
                        'modifications': decrypt_data(item[4])
                    } for item in items
                ]
            })
        return all_orders

def fetch_all_orders_with_date_range(start_date, end_date):
    """
    Fetches all orders from the database.
    
    Returns:
        list: A list of dictionaries containing order details.
    """
    with get_cursor() as cursor:
        start_date = start_date.replace("-", "")
        end_date = end_date.replace("-", "")

        # Cast order_date to INTEGER to avoid complications with comparing dates
        cursor.execute("SELECT * FROM orders WHERE CAST(strftime('%Y%m%d', order_date) as INTEGER) BETWEEN ? AND ?", (start_date, end_date))
        orders = cursor.fetchall()
        
        all_orders = []
        for order in orders:
            cursor.execute("SELECT * FROM order_item WHERE order_id = ?", (order[0],))
            items = cursor.fetchall()
            all_orders.append({
                'order_id': order[0],
                'user_id': decrypt_data(order[1]),
                'order_date': order[2],
                'status': order[3],
                'order_type': order[4],
                'table_number': order[5],
                'price': order[6],
                'branch_id': order[7],
                'items': [
                    {
                        'item_id': item[2],  
                        'quantity': decrypt_data(item[3]),  
                        'modifications': decrypt_data(item[4])
                    } for item in items
                ]
            })
        return all_orders
    
def fetch_all_orders_items_quantity(start_date, end_date):
    """
    Fetches all orders from the database.
    
    Returns:
        list: A list of dictionaries containing order details.
    """
    with get_cursor() as cursor:
        start_date = start_date.replace("-", "")
        end_date = end_date.replace("-", "")

        # Cast order_date to INTEGER to avoid complications with comparing dates
        cursor.execute("SELECT * FROM orders WHERE CAST(strftime('%Y%m%d', order_date) as INTEGER) BETWEEN ? AND ?", (start_date, end_date))
        orders = cursor.fetchall()

        items = {}
        for order in orders:
            cursor.execute("""SELECT order_item.quantity, item.name, item.price, item.description FROM order_item 
                              INNER JOIN item ON order_item.item_id = item.id WHERE order_id = ?""", (order[0],))
            order_items = cursor.fetchall()
            
            for item in order_items:
                quantity = int(decrypt_data(item[0]))
                name = item[1]
                price = item[2]
                description = item[3]


                if name not in items.keys():#

                    items[name] = {
                        "quantity": quantity,
                        "price": price,
                        "description": description
                    }
                else:

                    items[name]["quantity"] += quantity

        # Add names back to object and put objects into array for easier use when processing data
        items_array = []
        for key, value in items.items():
            value['name'] = key 
            items_array.append(value)

        return items_array

def fetch_all_orders_extended():
    """
    Fetches all orders from the database.
    
    Returns:
        list: A list of dictionaries containing order details.
    """
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        
        all_orders = []
        for order in orders:    
            cursor.execute("SELECT * FROM order_item WHERE order_id = ?", (order[0], ))
            items_with_orders = cursor.fetchall()

            items = []
            for item_with_orders in items_with_orders:
                cursor.execute("SELECT * FROM item WHERE id = ?", (item_with_orders[2], )) # Bracket added to parameters section
                item_query_return = cursor.fetchall()
                item = {
                    'item_id': item_with_orders[2],
                    'quantity': decrypt_data(item_with_orders[3]),  
                    'name': item_query_return[0][1],
                    'description': item_query_return[0][2],
                    'price': item_query_return[0][3],
                    'item_type': item_query_return[0][4],
                    'modifications': decrypt_data(item_with_orders[4])
                }
                items.append(item)

            all_orders.append({
                'order_id': order[0],
                'user_id': decrypt_data(order[1]),
                'order_date': order[2],
                'status': order[3],
                'order_type': decrypt_data(order[4]),
                'table_number': order[5],
                'price': order[6],
                'branch_id': order[7],
                'items': items
            })
        return all_orders
    

# -------------------- Module Communication -------------------- #

def send_to_delivery_app(order_id):
    """
    Sends a specified order to the Delivery App to process.

    Args:
        order_id (int): The ID of the order to send.

    Returns:
        dict: The response from the Delivery App.
    """
    order_id = str(order_id)
    
    DELIVERYAPPURL = f"http://localhost:3000/delivery_update/{order_id}"

    try:
        response = requests.put(DELIVERYAPPURL)

        if response.status_code == 200:
            return jsonify({"status": "Updated the Delivery App successfully", "details": response.json()})

        else:
            return jsonify({'error': response.json()})
        
    except Exception as e:
        return jsonify({'error': "An error occurred attempting to send the request", "details": str(e)})