from flask import Flask, send_file, render_template, request
from jsonschema import validate, ValidationError
from flask_cors import CORS
import json
from enum import Enum
import os
import uuid 

app = Flask(__name__)

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8080'))

# The url with port 5000 is there so that the customer feedback system can access the data.
# If there is a better way to do this, please let me know.

CORS(app, origins=[f'http://{HOST}:{PORT}', f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}', 'http://127.0.0.1:5000', 'http://localhost:5000'])

class SearchArea(Enum):
    RESTAURANTS = 'restaurants'
    MENUS = 'menus'
    CATEGORIES = 'categories'
    ITEMS = 'items'

def get_menu_file():
    MENU_FILE = app.config.get('MENU_FILE', os.path.join(os.path.dirname(__file__), 'menus.json'))
    if os.path.exists(MENU_FILE):
        return MENU_FILE
    else:
        raise FileNotFoundError(f'The menu file {MENU_FILE} does not exist')

@app.route('/')
def home():
    return render_template('customer_view.html')

@app.route('/admin_panel')
def admin_view():
    return render_template('index.html')

@app.route('/api/get_data')
def get_all_data():
    return send_file(get_menu_file(), mimetype='application/json')

@app.route('/api/get_data/search', methods=['GET'])
def search_data():
    search_area = request.args.get('area')
    search_option = request.args.get('option')
    search_name = request.args.get('name')
    search_id = request.args.get('id')
    search_reward_eligible = request.args.get('reward_eligible')
    search_dietary_requirements = request.args.get('dietary_requirements')

    with open(get_menu_file(), 'r') as f:
        data = json.load(f)
    
    if search_area and (search_name or (search_option and search_name)) and not search_reward_eligible:
    
        if search_area == SearchArea.RESTAURANTS.value:
            result = []
            if search_option == 'name':
                result = [restaurant for restaurant in data[SearchArea.RESTAURANTS.value] if (search_name.lower() in restaurant['name'].lower() or search_name == '*')]
            elif search_option == 'contains':
                result = contains_value(data[SearchArea.RESTAURANTS.value], search_name)
            else:
                return 'Invalid search parameter (option)', 400

        elif search_area == SearchArea.MENUS.value:
            result = []
            if search_option == 'name':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        if search_name.lower() in menu['name'].lower() or search_name == '*':
                            result.append(menu)
            elif search_option == 'contains':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        if contains_value(menu, search_name):
                            result.append(menu)
            else:
                return 'Invalid search parameter (option)', 400
        
        elif search_area == SearchArea.CATEGORIES.value:
            result = []
            if search_option == 'name':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        for category in menu[SearchArea.CATEGORIES.value]:
                            if search_name.lower() in category['name'].lower() or search_name == '*':
                                result.append(category)
            elif search_option == 'contains':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        for category in menu[SearchArea.CATEGORIES.value]:
                            if contains_value(category, search_name):
                                result.append(category)
            else:
                return 'Invalid search parameter (option)', 400
                
        elif search_area == SearchArea.ITEMS.value:
            result = []
            if search_option == 'name':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        for category in menu[SearchArea.CATEGORIES.value]:
                            for item in category[SearchArea.ITEMS.value]:
                                if search_name.lower() in item['name'].lower() or search_name == '*':
                                    result.append(item)
            elif search_option == 'contains':
                for restaurant in data[SearchArea.RESTAURANTS.value]:
                    for menu in restaurant[SearchArea.MENUS.value]:
                        for category in menu[SearchArea.CATEGORIES.value]:
                            for item in category[SearchArea.ITEMS.value]:
                                if contains_value(item, search_name):
                                    result.append(item)
            else:
                return 'Invalid search parameter (option)', 400
                        
        else:
            return 'Invalid search parameter (area)', 400

    elif search_reward_eligible and not(search_area or search_option or search_name or search_dietary_requirements or search_id):
            result = []
            for restaurant in data[SearchArea.RESTAURANTS.value]:
                for menu in restaurant[SearchArea.MENUS.value]:
                    for category in menu[SearchArea.CATEGORIES.value]:
                        for item in category[SearchArea.ITEMS.value]:
                            
                            if search_reward_eligible == 'true':
                                if item['rewardEligible'] == True:
                                    result.append(item)
                            elif search_reward_eligible == 'false':
                                if item['rewardEligible'] == False:
                                    result.append(item)
                            else:
                                return 'Invalid search parameter (reward_eligible)', 400
    
    elif search_dietary_requirements and not(search_area or search_option or search_name or search_reward_eligible or search_id):
            result = []
            for restaurant in data[SearchArea.RESTAURANTS.value]:
                for menu in restaurant[SearchArea.MENUS.value]:
                    for category in menu[SearchArea.CATEGORIES.value]:
                        for item in category[SearchArea.ITEMS.value]:
                            if search_dietary_requirements in item['dietary'] or (search_dietary_requirements == '*' and item['dietary'] != []):
                                result.append(item)

    elif search_id and not(search_area or search_option or search_name or search_reward_eligible or search_dietary_requirements):
        result = []
        for restaurant in data[SearchArea.RESTAURANTS.value]:
            for menu in restaurant[SearchArea.MENUS.value]:
                for category in menu[SearchArea.CATEGORIES.value]:
                    for item in category[SearchArea.ITEMS.value]:
                        if item['id'] == search_id or search_id == '*':
                            result.append(item)

    else:
        return 'Invalid search parameters', 400

    if not result:
        return 'No results found', 404

    return json.dumps(result)

def contains_value(data, search_value):
        if isinstance(data, dict):
            return any(contains_value(value, search_value) for value in data.values())
        elif isinstance(data, list):
            return any(contains_value(item, search_value) for item in data)
        else:
            return data == search_value

def update_data_in_json(path, new_data):
    try:
        with open(get_menu_file(), 'r') as f:
            old_data = json.load(f)
        
        target = old_data
        for key in path[:-1]:
            target = target[key]

        if path[-2] == SearchArea.ITEMS.value:
            target[path[-1]]['name'] = new_data['name']
            target[path[-1]]['price'] = float(new_data['price'])
            target[path[-1]]['rewardEligible'] = new_data['rewardEligible']
        else:
            target[path[-1]] = new_data

        with open(get_menu_file(), 'w') as f:
            json.dump(old_data, f)

        return 'Data updated', 200
    except Exception as e:
        return f'Error updating data: {str(e)}', 400

@app.route('/api/update_data', methods=['PUT'])
def update_data():
    data = request.json
    path = data['path']
    new_data = data['newData']

    if not path or new_data is None:
        return 'Invalid update parameters', 400
    elif not isinstance(path[0], str):
        return 'Invalid path structure (path does not start with string value)', 400
    elif (path[-2] not in [SearchArea.ITEMS.value, 'dietary'] and path[-1] != 'name'):
        return 'Invalid path structure (last element is not name)', 400
    elif (path[-2] in [SearchArea.ITEMS.value, 'dietary'] and not isinstance(path[-1], int)):
        return 'Invalid path structure (last element is not int)', 400

    return update_data_in_json(path, new_data)

def add_data_to_json(path, new_data):
    try:
        with open(get_menu_file(), 'r') as f:
            old_data = json.load(f)
        
        target = old_data
        for key in path:
            target = target[key]
        target.append(new_data)

        with open(get_menu_file(), 'w') as f:
            json.dump(old_data, f)

        return 'Data added', 200
    except Exception as e:
        return f'Error adding data: {str(e)}', 400

@app.route('/api/add_data', methods=['POST'])
def add_data():
    data = request.json
    path = data['path']
    new_data = data['newData']

    if path[-1] == SearchArea.ITEMS.value:
        new_data['id'] = str(uuid.uuid4())

    if not path or new_data is None or not isinstance(path[-1], str) or not isinstance(path[0], str) or check_new_data_schema(new_data, path) == False:
        return 'Invalid add parameters', 400

    if 'price' in new_data:
        new_data['price'] = float(new_data['price'])

    return add_data_to_json(path, new_data)

def delete_data_from_json(path):
    try:
        with open(get_menu_file(), 'r') as f:
            old_data = json.load(f)
        
        target = old_data
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]

        with open(get_menu_file(), 'w') as f:
            json.dump(old_data, f)

        return 'Data deleted', 200
    except Exception as e:
        return f'Error deleting data: {str(e)}', 400

@app.route('/api/delete_data', methods=['DELETE'])
def delete_data():
    data = request.json
    path = data['path']

    if not path or not isinstance(path[-1], int) or not isinstance(path[0], str):
        return 'Invalid delete parameters', 400

    return delete_data_from_json(path)

def check_new_data_schema(new_data, path):
    target = path[-1]
    schema = get_schema(target)
        
    try:
        validate(instance=new_data, schema=schema)
        return True
    except ValidationError as e:
        return False
    
def get_schema(target):
    with open('/src/new_data_schema.json', 'r') as f:
        schema = json.load(f).get(target, {})
    return schema

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
