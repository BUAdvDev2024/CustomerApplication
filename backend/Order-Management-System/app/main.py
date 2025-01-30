from flask import Flask, jsonify, request, render_template
from app.config.routes import order_blueprint
from app.config.metric_routes import order_metrics_blueprint
from dotenv import load_dotenv
from app.config.database import insert_dummy_data, get_cursor
from app.config.setup.setup_item_data import retrieve_dummy_item_data
import os
import sqlite3

load_dotenv()

app = Flask(__name__)
app.json.sort_keys = False

app.register_blueprint(order_blueprint, url_prefix='/api/')
app.register_blueprint(order_metrics_blueprint, url_prefix='/api/')

API_KEY = os.getenv('API_KEY')

"""
#Dummy data code - commented out
DUMMY_DATA = os.getenv('DUMMY_DATA')

add_DUMMY_DATA = DUMMY_DATA == True
dummy_data_path = os.getcwd() + "/instance/insert_dummy_data.txt"
insert_completed = True
"""


@app.before_request
def before_request():
    if request.path.startswith('/api/'):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != f'Bearer {API_KEY}':
            return jsonify({'error': 'Unauthorized'}), 401
        
        
@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)