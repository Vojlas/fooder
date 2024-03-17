import Pekarka as pk
import FoodGarden as food
import Bistro
import subprocess
import sys, os
from datetime import date
import argparse
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)
LoggingEnabled = False

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main(returnAsString):
    #install("beautifulsoup4")
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
        y = foo.loadMenuItems();
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



    res_list = []
    for item in Items: 
        if item.place not in res_list: 
            res_list.append(item.place) 
    print()
    html = """<h
    <body>"""
    today = date.today()
        # show date in different format
    today = today.strftime("%d/%m/%Y")
    html += f"<p class=\"time\">{today}</p>"
    #html += f"<p class=\"time\">10/09/2023</p>"
    html = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .time {
            color: green;
            font-size: 1.2em;
        }
        h2 {
            color: navy;
            text-align: center;
        }
        table {
            width: 100%; /* Make table width 100% of its container */
            margin: auto;  /* Center the table */
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        @media screen and (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }
            th, td {
                text-align: right;
            }
            td:before {
                content: attr(data-label);
                float: left;
                font-weight: bold;
            }
        }
    </style>
</head>
<body>"""

    today = date.today()
    # show date in different format
    today = today.strftime("%d/%m/%Y")
    html += f'<p class="time">{today}</p>'

    for restaurant in res_list:
        if LoggingEnabled:
            print(restaurant)
        html += f"<h2>{restaurant}</h2>"
        fo = filter(lambda x: x.place==restaurant, Items)
        html += "<table><thead><tr><th>Název</th><th>Cena</th></tr></thead><tbody>"
        for f in fo:
            html += f'<tr><td data-label="Název">{f.name}</td><td data-label="Cena">{f.price}</td></tr>'
            if LoggingEnabled:
                print(f.name)
        html += "</tbody></table>"
        if LoggingEnabled:
            print('\n')
        html += "<br />"
    html += "</body></html>"

    localPath = ".\\data\\menu.html"
    path = "\\\\orion\\USYS_DIRECTORY\\USYS_Home\\VojtaP\\menu.html"

    if returnAsString:
        if not os.path.exists(".\\data"):
            os.mkdir(".\\data")
        copyFile(html, localPath)

        return html
    else:
        localPath = ".\\data\\menu.html"
        if not os.path.exists(".\\data"):
            os.mkdir(".\\data")

        # Make local copy
        copyFile(html, localPath)

        # Publish
        copyFile(html, path)

    if LoggingEnabled:
        print("Done!")

def copyFile(html, path):
    if os.path.exists(path):
        os.remove(path)
    f = open(path, "a")
    f.write(html)
    f.close()

def getCache():
    path = ".\\data\\menu.html"

    if os.path.exists(path):
        f = open(path, "r")
        html = f.read()
        f.close()

        soup = BeautifulSoup(html, "html.parser")
        time = soup.find("p", {"class": "time"})

        if time:
            time = time.text
            today = date.today()
            today = today.strftime("%d/%m/%Y")

            if time == today:
                return html
                app.logger.info("Cache hit!")
            else:
                return None
                app.logger.info("Cache old!")
        return html
    else:
        return None
        app.logger.info("Cache miss!")

@app.route('/')
def index():
    print("Index")
    cache = getCache()
    if cache:
        print("    Cache hit!")
        return cache
    else:
        print("    Cache miss!")
        return main(True)
    
@app.route('/erase')
def ereaseCache():
    path = ".\\data\\menu.html"
    if os.path.exists(path):
        os.remove(path)

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
    
    print("Starting the server...")
    app.run(host='0.0.0.0', port=8000)
    