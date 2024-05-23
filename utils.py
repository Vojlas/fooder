# utils.py
import json
import os
from datetime import datetime
from FoodItem import FoodItem
import Pekarka as pk
import FoodGarden as food
import Bistro
import Sokolovna

def fetch_menu_items():
    Items = []

    #Pekarka:
    try:
        pkk = pk.Pekarka()
        x = pkk.loadMenuItems()
        for a in x:
            Items.append(a)
    except Exception as e:
        print(f"An error occurred while loading Bistro menu items: {e}")

    #FoodGarden:
    try:
        foo = food.FoodGarden()
        y = foo.loadMenuItems()
        for b in y:
            Items.append(b)
    except Exception as e:
        print(f"An error occurred while loading Bistro menu items: {e}")

    #Bistro:
    try:
        kavky = Bistro.Bistro()
        kavkyFood = kavky.loadMenuItems()
        for k in kavkyFood:
            Items.append(k)
    except Exception as e:
        print(f"An error occurred while loading Bistro menu items: {e}")

    #Sokolovna
    try:
        soko = Sokolovna.Sokolovna()
        sokoFood = soko.loadMenuItems()
        for s in sokoFood:
            Items.append(s)
    except Exception as e:
        print(f"An error occurred while loading Sokolovna menu items: {e}")

    return Items

def cache_data(items):
    items_as_dicts = [item.to_dict() for item in items]

    cache_content = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'items': items_as_dicts
    }
    cache_path = "./data/menu_items_cache.json"
    if not os.path.exists(os.path.dirname(cache_path)):
        os.makedirs(os.path.dirname(cache_path))

    with open(cache_path, "w") as f:
        json.dump(cache_content, f)
    print('Saved to cache')

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
