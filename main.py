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
    html += f"<p>{today}</p>"
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
    