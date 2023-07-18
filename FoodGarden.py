import FoodItem 
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup

class FoodGarden():
    def __init__(self):
        print("FoodGarden")

    def loadMenuItems(self):
        url = "https://www.cateringmelodie.cz/lunch-garden"
        soup = BeautifulSoup(self.loadPage(url), "html.parser")
        menu_items = []

        # Find the menu section

        dt = datetime.now()
        q = dt.weekday()
        weekdays = ['pondeli', 'utery', 'streda', 'ctvrtek','patek']
        menu_section = soup.find('div', {'id': weekdays[q]})

        if menu_section:
            for i in range(0,5):
                var = menu_section.contents[0].contents[0].contents[0].contents[0].contents[i]
                match i:
                    case 0: #Name
                        day_name_element = var.find('h3')
                    
                    case 2: #Food
                        menu = var.find_all('p')
                        for item in menu:
                            m = FoodItem.FoodItem('Food Garden', item.contents[0], 'neznámá')
                            menu_items.append(m)
                    
                    case 4: #Superior
                        sup = var.find_all('div', {'class':'listitem-cell'})[1]
                        m = FoodItem.FoodItem('Food Garden', 'SUPERIOR: '+sup.contents[0], 'neznámá')
                        menu_items.append(m)
                        return menu_items             

    def loadPage(self, url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        return mystr