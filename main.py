import Pekarka as pk
import FoodGarden as food
# import Bistro
import subprocess
import sys, os
from datetime import date

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    #install("beautifulsoup4")
    Items = []

    #Pekarka:
    pkk = pk.Pekarka()
    x = pkk.loadMenuItems()
    for a in x:
        Items.append(a)

    #FoodGarden:
    foo = food.FoodGarden()
    y = foo.loadMenuItems();
    for b in y:
        Items.append(b)

    #Bistro:
   # kavky = Bistro.Bistro()
   # kavkyFood = kavky.loadMenuItems()
   # for k in kavkyFood:
   #     Items.append(k)



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
    html += """<script>
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
    </script>"""
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
    html += "</body>"

    path = "\\\\orion\\USYS_DIRECTORY\\USYS_Home\\VojtaP\\menu.html"
    #path = "C:\\Users\\vojtech.pavlas.USYS\\Desktop\\menu.html"


    if os.path.exists(path):
        os.remove(path)
    f = open(path, "a")
    f.write(html)
    f.close()

    print("Done!")

if (__name__ == "__main__"):
    main()
    