import unittest
from app import app
import shutil
import os

class TestApp(unittest.TestCase):
    def setUp(self):

        self.test_data_path = os.path.join(os.path.dirname(__file__), 'temp_test_menu_data.json')

        os.makedirs(os.path.dirname(self.test_data_path), exist_ok=True)

        shutil.copyfile('/src/menus.json', self.test_data_path)

        with open(self.test_data_path, 'r') as f:
            self.original_data = f.read()

        app.config['MENU_FILE'] = self.test_data_path

        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        if os.path.exists(self.test_data_path):
            os.remove(self.test_data_path)

    def test_update_restaurants_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants'],
            'newData': { 'name': 'test', 'menus': [ { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }]}] }
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'name'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data updated')

        self.undo_changes()

    def test_update_menus_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus'],
            'newData': { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }] }
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'name'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data updated')

        self.undo_changes()

    def test_update_category_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories'],
            'newData': { 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'name'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data updated')

        self.undo_changes()

    def test_update_item_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items'],
            'newData': {'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False}
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'name'],
            'newData': {'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False}
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data updated')

        self.undo_changes()

    def test_update_dietary_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary', 0],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data updated')

        self.undo_changes()

    def test_update_data_invalid_1(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })

        self.assertEqual(response.status_code, 200)

        response = self.app.put('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Invalid path structure (last element is not name)')

        self.undo_changes()

    def test_update_data_invalid_2(self):
        response = self.app.post('/api/update_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary', 0],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 405)

        self.undo_changes()

    def test_add_restaurants_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants'],
            'newData': { 'name': 'test', 'menus': [ { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }]}] }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data added')

        self.undo_changes()

    def test_add_menus_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus'],
            'newData': { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }] }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data added')

        self.undo_changes()

    def test_add_category_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories'],
            'newData': { 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data added')

        self.undo_changes()

    def test_add_item_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items'],
            'newData': {'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False}
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data added')

        self.undo_changes()

    def test_add_dieatary_data(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data added')

        self.undo_changes()

    def test_add_data_invalid_1(self):
        response = self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items'],
            'newData': {'name': 'test'}
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Invalid add parameters')

        self.undo_changes()

    def test_add_data_invalid_2(self):
        response = self.app.put('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })
        self.assertEqual(response.status_code, 405)

        self.undo_changes()

    def test_delete_restaurants_data(self):
        self.app.post('/api/add_data', json={
            'path': ['restaurants'],
            'newData': { 'name': 'test', 'menus': [ { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }]}] }
        })

        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data deleted')

        self.undo_changes()
    
    def test_delete_menus_data(self):
        self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus'],
            'newData': { 'name': 'test', 'categories': [{ 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }] }
        })

        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data deleted')

        self.undo_changes()

    def test_delete_category_data(self):
        self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories'],
            'newData': { 'name': 'test', 'items': [{'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False }] }
        })

        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data deleted')

        self.undo_changes()

    def test_delete_item_data(self):
        self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items'],
            'newData': {'name': 'test', 'price': 9.99, 'dietary': [], 'rewardEligible': False}
        })

        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data deleted')

        self.undo_changes()

    def test_delete_dietary_data(self):
        self.app.post('/api/add_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary'],
            'newData': 'test'
        })

        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary', 0]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Data deleted')

        self.undo_changes()

    def test_delete_data_invalid_1(self):
        response = self.app.delete('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary']
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b'Invalid delete parameters')

        self.undo_changes()
    
    def test_delete_data_invalid_2(self):
        response = self.app.post('/api/delete_data', json={
            'path': ['restaurants', 0, 'menus', 0, 'categories', 0, 'items', 0, 'dietary', 0]
        })
        self.assertEqual(response.status_code, 405)

        self.undo_changes()

    def undo_changes(self):
        if os.path.exists(self.test_data_path):
            with open(self.test_data_path, 'w') as f:
                f.write(self.original_data)

if __name__ == '__main__':
    unittest.main()