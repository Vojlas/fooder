import FoodItem 
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
import re

class Bistro():
    def __init__(self):
        print("Bistro")

    def loadMenuItems(self):
        #url = "https://www.nakavcichhorach.cz/info/tydenni/"
        url = "https://www.nakavcichhorach.cz/info/menu/#tydenni"
        soup = BeautifulSoup(self.loadPage(url), "html.parser")
        menu_items = []

        # Find the menu section

        dt = datetime.now()
        q = dt.weekday()
        weekdays = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek','Pátek']


        menu_section = soup.find('table', {'class': 'table_menu'})

        day = 1 + q*2
        dmenuAll = menu_section.contents[day]
        dmenuRaw = dmenuAll.contents[1]

        prFoo = dmenuAll.contents[3].find('span', {'class':'table_v2'}).text.strip() #cena jidlo
        prMenu = dmenuAll.contents[5].find('span', {'class':'table_v2'}).text.strip() #cena menu


        soup = dmenuRaw.contents[3].text.strip() #.contents[0]
        matches = re.findall(r'(\d+Kč)$', soup)
        value = 'neznámá'
        if matches:
            value = matches[-1]
            soup = re.sub(value, '',soup)

        menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', soup.strip(), value))

        rawFood = dmenuRaw.contents[5]
        for i in range(0, len(rawFood.contents)):
            if(i % 2 == 0):
                foo =  rawFood.contents[i].strip()
                menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', foo, prFoo + ' v menu: '+prMenu))

        return menu_items
                



    def loadPage(self, url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        return mystr
    
bis = Bistro()
bis.loadMenuItems()