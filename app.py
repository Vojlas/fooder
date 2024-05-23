import Pekarka as pk
import FoodGarden as food
import Bistro
import subprocess
import sys, os
from datetime import date, datetime
import argparse
from flask import Flask, request, send_from_directory, render_template
from bs4 import BeautifulSoup
from flask_cors import CORS
from dotenv import load_dotenv
from BackgroundTask import BackgroundTasks
from utils import fetch_menu_items, cache_data, load_cached_data
from FoodItem import FoodItem, FoodItemCollection
import json


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get("FLASK_DEBUG")
LoggingEnabled = False

def main(order_param, returnAsString=False):
    cached_items = load_cached_data()
    if not cached_items:
        # Fetch data if not cached
        Items = fetch_menu_items()
        cache_data(Items)
    else:
        Items = cached_items

    # Map letters to restaurant names
    order_mapping = {'F': 'Food Garden', 'P': 'Pekařka', 'B': 'Bistro Kavčí hory', 'S': 'Sokolovna'}
    ordered_restaurants = [order_mapping[letter] for letter in order_param if letter in order_mapping]

    menu_data = {}
    for item in Items:
        # Determine if the item is a FoodItem instance or a dictionary and access accordingly
        place = item.place if isinstance(item, FoodItem) else item['place']

        # Ensure there is a list to append to for the given place
        if place not in menu_data:
            menu_data[place] = []

        # Append the item to the list for the restaurant/place
        menu_data[place].append(item.to_dict())

    coll = FoodItemCollection(Items)
    sorted_menu_data = coll.transformCollection()

    today = date.today().strftime("%d/%m/%Y")

    if returnAsString:
        html_content = render_template('menu.html', menu_data=sorted_menu_data, today=today)
        # Code to save html_content to a file
        return html_content
    else:
        return render_template('menu.html', menu_data=sorted_menu_data, today=today)

def load_cached_data():
    cache_path = "./data/menu_items_cache.json"
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cache_content = json.load(f)
                cache_date = cache_content['date']
                today_date = datetime.now().strftime("%Y-%m-%d")
                if cache_date == today_date:
                    print('Cache loaded')
                    # Convert the list of dictionaries to a list of FoodItem instances
                    items = [FoodItem.from_dict(item) for item in cache_content['items']]
                    return items
                else:
                    return None
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading cache: {e}")
            return None
    return None


@app.route('/')
def index():
    print("Index")
    order_param = request.args.get('order', default='FPBS')
    return main(order_param)
    
@app.route('/erase')
def eraseCache():
    path = "./data/menu_items_cache.json"
    if os.path.exists(path):
        os.remove(path)
        return "Cache erased!"
    else:
        return "Cache not found!"
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/update_cache', methods=['POST'])
def update_cache():
    key = request.form.get('key')
    if key == '12rnxHJo1PRkmKArogiyhDKEnmBuOT486':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        file.save('./data/menu_items_cache.json')
        return 'Cache updated', 200
    else:
        return 'Unauthorized', 403

if (__name__ == "__main__"):
    # Create the parser
    parser = argparse.ArgumentParser(description="Specify working directory")

    # Add the arguments
    parser.add_argument('--dir', type=str, help='The working directory')

    # Parse the arguments
    args = parser.parse_args()

    # Use the provided working directory
    if args.dir:
        os.chdir(args.dir)

    if os.getenv('START_BACKGROUND_TASK') == 'true':
        t = BackgroundTasks()
        t.run()
    
    print("Starting the server...")
    app.run()

    