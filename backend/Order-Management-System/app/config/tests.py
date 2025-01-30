import unittest
from get import (
    get_orders,
    create_order,
    view_order,
    update_status,
    amend_order_items,
    delete_order,
    get_orders_by_date,
    get_orders_items_quantity_by_date,
    get_orders_extended,
)

class TestAPIInteractions(unittest.TestCase):

    def test_get_orders(self):
        """Test for fetching orders."""
        orders = get_orders()

        # Display the output for debugging or review
        display_test_output(orders, "get_orders")

        # Assert the structure and values of the response
        self.assertIsInstance(orders, list)
        self.assertEqual(orders[0]["order_id"], 1)
        self.assertEqual(orders[0]["status"], "PENDING")

        print("✅ get_orders test passed")
    
    def test_update_status(self):
        """Test for updating an order status."""
        order_id = 1
        new_status = "IN PROGRESS"

        result = update_status(order_id, new_status)

        # Display the output for debugging or review
        display_test_output(result, "update_status")

        # Assert the response contains the correct fields
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Order Status has been updated successfully")

        print("✅ update_status test passed")
    
    def test_view_order(self):
        """Test for viewing an order."""
        order_id = 1
        order = view_order(order_id)

        # Display the output for debugging or review
        display_test_output(order, "view_order")

        # Assert the structure and values of the response
        self.assertIsInstance(order, dict)
        self.assertEqual(order["order_id"], 1)
        self.assertEqual(order["status"], "IN PROGRESS")

        print("✅ view_order test passed")

    def test_create_order(self):
        """Test for creating a new order."""
        user_id = 1
        order_type = "Eat In"
        branch_id = 2
        price = 29.99
        table_number = 5
        items = [{"item_id": 1, "quantity": 2}]

        order_data = {
            "user_id": 1,
            "order_type": "Eat In",
            "branch_id": 2,
            "price": 29.99,
            "items": [{"item_id": 1, "quantity": 2}],
            "table_number": 5
        }
        result = create_order(user_id, order_type, branch_id, price, items, table_number)

        # Display the output for debugging or review
        display_test_output(result, "create_order")

        # Assert the response contains the correct fields
        self.assertIn("message", result)
        self.assertEqual(result["message"], "Order has been created successfully")

        print("✅ create_order test passed")

def display_test_output(data, test_name):
    print(f"\n🚀 TEST OUTPUT FOR {test_name} 🚀")
    print(data)

if __name__ == "__main__":
    unittest.main()
