import threading
import time
import schedule
import datetime
import requests
import os
from utils import fetch_menu_items, cache_data
from dotenv import load_dotenv

load_dotenv()

class BackgroundTasks(threading.Thread):
    def __init__(self):
        super().__init__()
        self.cache_path = "./data/menu_items_cache.json"

    def run(self, *args, **kwargs):
        # Schedule the fetch_menu_items task to run every workday at 7am
        schedule.every().monday.at("07:00").do(self.fetch_and_cache_menu_items)
        schedule.every().tuesday.at("07:00").do(self.fetch_and_cache_menu_items)
        schedule.every().wednesday.at("07:00").do(self.fetch_and_cache_menu_items)
        schedule.every().thursday.at("07:00").do(self.fetch_and_cache_menu_items)
        schedule.every().friday.at("07:00").do(self.fetch_and_cache_menu_items)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def fetch_and_cache_menu_items(self):
        print("Fetching and caching menu items...")
        items = fetch_menu_items()
        cache_data(items)
        print("Menu items fetched and cached.")
        self.call_remote_server(os.getenv('KEY'), os.getenv('URL'))
        print("Saved and notified remote server")

    def call_remote_server(self, key, url):
        try:
            with open(self.cache_path, "rb") as f:
                files = {'file': f}
                response = requests.post(url, files=files, data={'key': key})
                response.raise_for_status()
                print("Request was successful")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending the request: {e}")


if __name__ == '__main__':
    c = BackgroundTasks()
    c.fetch_and_cache_menu_items()
