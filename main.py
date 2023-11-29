import Pekarka as pk
import FoodGarden as food
import Bistro
import subprocess
import sys, os
from datetime import date

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
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
    html = "<body>"
    today = date.today()
        # show date in different format
    today = today.strftime("%d/%m/%Y")
    html += f"<p class=\"time\">{today}</p>"
    #html += f"<p class=\"time\">10/09/2023</p>"
    html += """<!DOCTYPE html>
    <html>
    <head>
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

            @media screen and (min-width: 1200px) {
                table {
                    width: 100%;
                }
            }

            @media screen and (min-width: 1300px) {
                table {
                    width: 80%;
                }
            }

            @media screen and (min-width: 1500px) {
                table {
                    width: 70%;
                }
            }

            @media screen and (min-width: 1800px) {
                table {
                    width: 60%;
                }
            }
        </style>
        <script>
        // Get the element with class "time"
        const timeElement = document.querySelector('.time');

        // Get the current date (without time)
        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0); // Set the time to midnight

        // Extract the date part from the element's content
        const dateString = timeElement.textContent.split(' ')[0]; // Extract the date part in "dd/MM/yyyy" format

        // Parse the date string to create a Date object
        const dateParts = dateString.split('/');
        const date = new Date(`${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`);

        // Define a warning message element
        const warningMessage = document.createElement('h2');
        warningMessage.style.color = "red";

        // Compare the date and display a warning if outdated
        if (currentDate > date) {
            warningMessage.textContent = 'The menu is outdated!';
            timeElement.parentElement.appendChild(warningMessage);
        }
    </script>
    </head>
    <body>"""
    for restaurant in res_list:
        print(restaurant)
        html += f"<h2>{restaurant}</h2>"
        fo = filter(lambda x: x.place==restaurant, Items)
        html += "<table><th>Název</th><th>Cena</th>"
        for f in fo:
            html += f"<tr><td>{f.name}</td><td>{f.price}</td></tr>"
            print(f.name)
        html += "</table>"
        print('\n')
        html += "<br />"
    html += "</body></html>"

    path = "\\\\orion\\USYS_DIRECTORY\\USYS_Home\\VojtaP\\menu.html"
    localPath = ".\\data\\menu.html"
    if not os.path.exists(".\\data"):
        os.mkdir(".\\data")

    # Make local copy
    copyFile(html, localPath)

    # Publish
    copyFile(html, path)

    print("Done!")

def copyFile(html, path):
    if os.path.exists(path):
        os.remove(path)
    f = open(path, "a")
    f.write(html)
    f.close()

if (__name__ == "__main__"):
    main()
    