import FoodItem 
import urllib.request
from bs4 import BeautifulSoup

class Sokolovna():
    def __init__(self):
        print("Sokolovna")
        

    def loadMenuItems(self):
        url = "https://www.starasokolovna.cz/denni-nabidka"
        soup = BeautifulSoup(self.loadPage(url), "html.parser")

        menu_items = []
        menu_rows = soup.select(".row")

        #for row in menu_rows:
        row = menu_rows[0] # For now ignore other days
        menuRaw = row.select(".col-md-7")[0]
        day = menuRaw.select('.category-name')[0].text

        menu = menuRaw.select('.list-items')[0].contents
        filtered_menu = [item for item in menu if item != '\n']

        foodSection = ''
        for item in filtered_menu:
            if 'food-section' in item.get('class', []):
                foodSection = item.text
            elif 'list-item' in item.get('class', []):
                item = item.select('.row')[0]

                name = item.select('h3')[0].text.strip()
                price = item.select('.menu-price')[0].text.strip()
                menu_items.append(FoodItem.FoodItem("Sokolovna", name, price, foodSection))
        return menu_items

        # Print the menu items
        #for item in menu_items:
        #    print(f"Cislo: {item['cislo']}")
        #    print(f"Popis: {item['popis']}")
        #    print(f"Cena: {item['cena']}")
        #    print()

    def loadPage(self, url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        return mystr
    
#soko = Sokolovna()
#soko.loadMenuItems()
