import FoodItem 
import urllib.request
from bs4 import BeautifulSoup

class Pekarka():
    def __init__(self):
        print("Pekarka")
        

    def loadMenuItems(self):
        url = "https://www.napekarce.cz/"
        soup = BeautifulSoup(self.loadPage(url), "html.parser")

        menu_items = []
        table_rows = soup.select(".dailyMenuTable tr")
        for row in table_rows:
            cislo_elem = row.select_one(".td-cislo")
            popis_elem = row.select_one(".td-popis .td-jidlo-obsah")
            cena_elem = row.select_one(".td-cena")
            
            # Check if any of the elements are None
            if cislo_elem is None or popis_elem is None or cena_elem is None:
                continue
            
            if cislo_elem.next_element == "DĚTI":
                continue
            
            # Remove all numbers and ',' from the end of the string
            popis_text = popis_elem.text.strip()
            popis_text = ''.join([i for i in popis_text if not i.isdigit() and i != ','])
            
            item = FoodItem.FoodItem("Pekařka", popis_text, cena_elem.text.strip(), "menu")
            menu_items.append(item)
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