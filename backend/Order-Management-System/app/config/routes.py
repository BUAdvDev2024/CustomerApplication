from app.config.database import get_cursor
from app.config.order_utils import insert_order, fetch_all_orders, fetch_all_orders_with_date_range, fetch_all_orders_items_quantity, fetch_all_orders_extended, get_order_by_id, update_order_status, delete_order_items, add_items_to_order, validate_order_data, send_to_delivery_app
from flask import Blueprint, jsonify, request
import os
from datetime import datetime

# Blueprint for order-related routes
order_blueprint = Blueprint('orders', __name__)

@order_blueprint.route('/orders', methods=['GET'])
def get_orders():
    """
    Endpoint to fetch all orders.
    
    Returns:
        Response: A JSON response with the list of all orders.
    """
    try:
        orders = fetch_all_orders()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(orders), 200


@order_blueprint.route('/orders/create', methods=['POST'])
def create_order():
    """
    Endpoint to create a new order.

    Expects a JSON payload with 'user_id' 'order_type' 'branch_id' 'price' and 'items'. A table number is also possible.

    Returns:
        Response: A JSON response with the order details or an error message.
    """
    data = request.get_json()
    
    if not validate_order_data(data):
        return jsonify({'error': 'Invalid input data'}), 400

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
    
    if order_type == 'Delivery':
        try:
            send_to_delivery_app(order_id)
        except Exception as e:
            pass # Update logs or notify failure without compromising the order creation

    return jsonify({
        'message': 'Order has been created successfully',
        'order_id': order_id,
        'order_type': order_type,
        'order_date': 'datetime.now()',
        'status': 'PENDING',
        'table_number': table_number,
        'price': price,
        'branch_id': branch_id,
        'items': items
    }), 201
    
@order_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def view_order(order_id):
    """
    Endpoint to view a pre-existing order.
    
    Args:
        order_id (int): The ID of the order to view.
    Returns:
        Response: A JSON response with the order details or an error message.
    """
    try:
        order = get_order_by_id(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
     
    return jsonify(order)

@order_blueprint.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    """
    Endpoint to update the status of an existing order.

    Expects payload JSON with new_status

    Args:
        order_id (int): The ID of the order to update it's status
    Returns:
        Response: A JSON response with the updated order status or an error message.
    """

    data = request.get_json()
    
    new_status = data['new_status']

    if not data or not new_status:
        return jsonify({'error': 'Invalid input data. New status is required.'}), 400

    try:
        result = update_order_status(order_id, new_status)
        if not result:
            return jsonify({'error': 'Order not found or update failed'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    # Update the Delivery App here with an awaited function whereby when an order is complete of type delivery, notify the system

    return jsonify({
        'message': 'Order Status has been updated successfully',
        'order_id': order_id,
        'new_status': new_status
    }), 200

@order_blueprint.route('orders/<int:order_id>/items', methods=['PUT'])
def amend_order_items(order_id):
    """
    Endpoint to amend the items in an existing order.

    Expects a JSON payload with the full new list of 'items' (list of items with 'item_id', 'quantity', and optional 'modifications').

    Args:
        order_id (int): The ID of the order to update its items.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    data = request.get_json()

    if not data.get('items') or not isinstance(data['items'], list):
        return jsonify({'error': 'Invalid input data. New Items for the order is required.'}), 400
    
    items = data['items']

    try:
        if not delete_order_items(order_id):
             return jsonify({'error': 'Failed to delete existing items or no items found for this order.'}), 500
        
        add_items_to_order(order_id, items)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'message': 'Order items have been amended successfully',
        'order_id': order_id,
        'items': items
    }), 200

@order_blueprint.route('/orders/<int:order_id>/delete', methods=['DELETE'])
def delete_order(order_id):
    """
    Endpoint to delete an order and its associated items by order ID.

    Args:
        order_id (int): The ID of the order to delete.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Order not found'}), 404

        if not delete_order_items(order_id):
            return jsonify({'error': 'Failed to delete order items'}), 500

        with get_cursor() as cursor:
            cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            if cursor.rowcount == 0:
                return jsonify({'error': 'Failed to delete order'}), 500

        return jsonify({'message': 'Order deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_blueprint.route('/orders/date', methods=['GET'])
def get_orders_by_date():
    """
    Endpoint to fetch all orders in a date range.
    
    Returns:
        Response: A JSON response with the list of all orders in a date range.        
    """

    data = request.args
    start_date = data['start_date']
    end_date = data['end_date']
    
    if not data or not start_date or not end_date:
        return jsonify({'error': 'Both start_date and end_date are required'}), 400

    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. You must use YYYY-MM-DD.'}), 400

    try:
        orders = fetch_all_orders_with_date_range(start_date, end_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(orders), 200

@order_blueprint.route('/orders/items/quantity/date', methods=['GET'])
def get_orders_items_quantity_by_date():
    """
    Endpoint to fetch all orders in a date range.
    
    Returns:
        Response: A JSON response with the list of all orders in a date range.        
    """

    data = request.args    
    start_date = data['start_date']
    end_date = data['end_date']
    
    if not data or not start_date or not end_date:
        return jsonify({'error': 'Both start_date and end_date are required'}), 400

    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    try:
        orders = fetch_all_orders_items_quantity(start_date, end_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(orders), 200

@order_blueprint.route('/orders/extended', methods=['GET'])
def get_orders_extended():
    """
    Endpoint to fetch all orders with more info for items.
    
    Returns:
        Response: A JSON response with the list of all orders with more info for items.
    """
    try:
        orders = fetch_all_orders_extended()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(orders), 200