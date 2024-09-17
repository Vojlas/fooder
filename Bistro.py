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
        dmenuAll = menu_section.contents
        
        menuDaySelection =[]
        ranges = [(1, 8), (9, 16), (17, 24), (25, 32), (33, 40)]
        if q < len(ranges):
            for i in range(ranges[q][0], ranges[q][1]):
                menuDaySelection.append(dmenuAll[i])
        else:
            print(f"Index {q} is out of range for the 'ranges' list.")
        
        #dmenuRaw = dmenuAll.contents[1]

        #prFoo = dmenuAll.contents[3].find('span', {'class':'table_v2'}).text.strip() #cena jidlo
        #prMenu = dmenuAll.contents[5].find('span', {'class':'table_v2'}).text.strip() #cena menu
        if len(menuDaySelection) == 0:
            print("Error getting menu for Bistro Kavčí hory")
            return

        soup = menuDaySelection[0].text.split('\n')[3].strip()
        matches = re.findall(r'(\d+Kč)$', soup)
        value = 'neznámá'
        if matches:
            value = matches[-1]
            soup = re.sub(value, '',soup)


        # soup = dmenuRaw.contents[3].text.strip() #.contents[0]
        # matches = re.findall(r'(\d+Kč)$', soup)
        # value = 'neznámá'
        # if matches:
        #     value = matches[-1]
        #     soup = re.sub(value, '',soup)

        soup.strip()
        soup = re.sub(r'A ((,| )?\d(,| )?)*$', '', soup).strip()
        menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', soup, value, "Polévka"))


        ## FOODS
        item = menuDaySelection[2].text.split('\n')
        food = item[1] #.split('/')[1].strip()
        food = re.sub(r'A ((,| )?\d(,| )?)*$', '', food).strip()
        menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', food, item[2], "menu"))
        
        for index in [4, 6]:
            item = menuDaySelection[index].text.split('\n')
            food = item[1].split('/')[1].strip()
            food = re.sub(r'A ((,| )?\d(,| )?)*$', '', food).strip()
            menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', food, item[2], "menu"))

        # rawFood = dmenuRaw.contents[5]
        # for i in range(0, len(rawFood.contents)):
        #     if(i % 2 == 0):
        #         foo =  rawFood.contents[i].strip()
        #         menu_items.append(FoodItem.FoodItem('Bistro Kavčí hory', foo, prFoo + ' v menu: '+prMenu))

        return menu_items
                



    def loadPage(self, url):
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        return mystr
    
#bis = Bistro()
#bis.loadMenuItems()
