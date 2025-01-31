from flask import Blueprint, jsonify, request
from app.config.database import get_cursor, decrypt_data
import datetime
import random

# Blueprint for additional order-related routes
order_metrics_blueprint = Blueprint('metrics', __name__)



@order_metrics_blueprint.route('/orders/popular-item/all', methods=['GET'])
def most_popular_item_all():
    """
    Endpoint to return the most popular item overall, grouped by branch.

    Returns:
        Response: A JSON response with the most popular item per branch or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "most_popular_item_id": 1,
                "item_name": "Burger",
                "frequency": 20
            },
            {
                "branch_id": 1001,
                "most_popular_item_id": 3,
                "item_name": "Pizza",
                "frequency": 15
            }
        ]
    }
    """

    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT o.branch_id, oi.item_id, i.name, COUNT(*) as frequency
                FROM orders o
                JOIN order_item oi ON o.order_id = oi.order_id
                JOIN item i ON oi.item_id = i.id
                GROUP BY o.branch_id, oi.item_id, i.name
                ORDER BY frequency DESC
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No items found'}), 404

            data = [
                {
                    'branch_id': row[0],
                    'most_popular_item_id': decrypt_data(row[1]),
                    'item_name': row[2],
                    'frequency': row[3]
                }
                for row in results
            ]
            return jsonify({'data': data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_metrics_blueprint.route('/orders/popular-item', methods=['GET'])
def most_popular_item():
    """
    Endpoint to return the most popular item between two dates, grouped by branch.

    Query Parameters:
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.

    Returns:
        Response: A JSON response with the most popular item per branch or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "most_popular_item_id": 1,
                "frequency": 20
            },
            {
                "branch_id": 1001,
                "most_popular_item_id": 3,
                "frequency": 15
            }
        ]
    }
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'Both start_date and end_date are required'}), 400

    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
        datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT o.branch_id, oi.item_id, COUNT(*) as frequency
                FROM orders o
                JOIN order_item oi ON o.order_id = oi.order_id
                WHERE DATE(o.order_date) BETWEEN ? AND ?
                GROUP BY o.branch_id, oi.item_id
                ORDER BY frequency DESC
                """,
                (start_date, end_date)
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No items found within the specified date range'}), 404

            data = [
                {
                    'branch_id': row[0],
                    'most_popular_item_id': decrypt_data(row[1]),
                    'frequency': row[2]
                }
                for row in results
            ]
            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@order_metrics_blueprint.route('/orders/popular-time-slot', methods=['GET'])
def most_popular_time_slot_all():
    """
    Endpoint to return the most popular time slot for orders on a given day, grouped by branch.

    Returns:
        Response: A JSON response with the most popular time slot per branch or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "most_popular_time_slot": "12:00",
                "frequency": 20
            },
            {
                "branch_id": 1001,
                "most_popular_time_slot": "13:00",
                "frequency": 15
            }
        ]
    }
    """
    required_date = request.args.get('required_date')

    if not required_date:
        return jsonify({'error': 'required_date is required'}), 400

    try:
        datetime.datetime.strptime(required_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id, SUBSTR(order_date, 12, 2) || ':00' as hour, COUNT(*) as frequency
                FROM orders
                WHERE DATE(order_date) = ?
                GROUP BY branch_id, hour
                HAVING frequency = (
                    SELECT MAX(frequency)
                    FROM (
                        SELECT branch_id, SUBSTR(order_date, 12, 2) || ':00' AS hour, COUNT(*) AS frequency
                        FROM orders
                        WHERE DATE(order_date) = ?
                        GROUP BY branch_id, hour
                    ) subquery
                    WHERE subquery.branch_id = orders.branch_id
                )
                """,
                (required_date, required_date)
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404

            data = [
                {
                    'branch_id': row[0],
                    'most_popular_time_slot': row[1],
                    'frequency': row[2]
                }
                for row in results
            ]
            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_metrics_blueprint.route('/orders/average-value', methods=['GET'])
def average_order_value():
    """
    Endpoint to return the average order value across all branches.

    Returns:
        Response: A JSON response with the average order value or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "average_order_value": 20.0
            },
            {
                "branch_id": 1001,
                "average_order_value": 25.0
            }
        ]
    }
    """
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id, AVG(price) as average_value 
                FROM orders
                GROUP BY branch_id
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404

            data = [
                {'branch_id': row[0], 'average_order_value': float(row[1])}
                for row in results
            ]

            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_metrics_blueprint.route('/orders/beverage-sales-percentage', methods=['GET'])
def beverage_sales_percentage():
    """
    Endpoint to return the percentage of sales from beverages per branch.

    Returns:
        Response: A JSON response with the beverage sales percentage or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "beverage_sales_percentage": 20.0
            },
            {
                "branch_id": 1001,
                "beverage_sales_percentage": 15.0
            }
        ]
    }
    """
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id, 
                       (SUM(CASE WHEN category = 'drinks' THEN price ELSE 0 END) / SUM(price)) * 100 AS percentage
                FROM order_item
                INNER JOIN item ON order_item.item_id = item.id
                INNER JOIN orders ON order_item.order_id = orders.id
                GROUP BY branch_id
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404
            
            data = [
                {'branch_id': row[0], 'beverage_sales_percentage': float(row[1])}
                for row in results
            ]

            return jsonify({'data':data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_metrics_blueprint.route('/orders/monthly-revenue', methods=['GET'])
def monthly_revenue():
    """
    Endpoint to return the monthly revenue from orders per branch.

    Returns:
        Response: A JSON response with the monthly revenue or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "month": "2021-07",
                "revenue": 200.0
            },
            {
                "branch_id": 1001,
                "month": "2021-07",
                "revenue": 150.0
            }
        ]
    }
    """
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id, SUBSTR(order_date, 1, 7) AS month, SUM(price) AS revenue
                FROM orders
                GROUP BY branch_id, month
                ORDER BY month DESC
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404

            data = [
                {'branch_id': row[0], 'month': row[1], 'revenue': float(row[2])}
                for row in results
            ]

            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@order_metrics_blueprint.route('/orders/traffic/peak', methods=['GET'])
def get_peak_traffic_hours_all():
    """
    Endpoint to return the peak traffic hours per branch overall.

    Returns:
        Response: A JSON response with the peak traffic hours or an error message.
    
    Example:
    {
        "data": [
            {
                "branch_id": 1000,
                "hour": 12:00,
                "traffic": 20
            },
            {
                "branch_id": 1001,
                "hour": 13:00,
                "traffic": 15
            }
        ]
    }

    """
    try:
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id, SUBSTR(order_date, 12, 2) || ':00' AS hour, COUNT(*) AS traffic
                FROM orders
                GROUP BY branch_id, hour
                ORDER BY traffic DESC
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404

            data = [
                {'branch_id': row[0], 'hour': row[1], 'traffic': row[2]}
                for row in results
            ]

            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@order_metrics_blueprint.route('/orders/average-order-time', methods=['GET'])
def average_order_time():
    """
    Endpoint to return the average time it takes to complete an order per branch. This is currently not achievable with the current database configuration, 
    so this will return dummy data instead. The dummy data is random average times selected from all branch_id's within the order database.

    Returns:
        Response: A JSON response with dummy average order time or an error message.

    Example:
    {
        "data": [
            {
                "branch_id": 1,
                "average_order_time_mins": 30
            },
            {
                "branch_id": 2,
                "average_order_time_mins": 40
            }
        ]
    }

    """
    try:

        random_average_times = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT branch_id
                FROM orders
                GROUP BY branch_id
                """
            )
            results = cursor.fetchall()

            if not results:
                return jsonify({'error': 'No orders found'}), 404

            data = [
                {'branch_id': row[0], 'average_order_time_mins': random.choice(random_average_times)}
                for row in results
            ]

            return jsonify({'data': data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
