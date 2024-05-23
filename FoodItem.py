class FoodItem:
    def __init__(self, place, name, price, category):
        self.name = name
        self.price = price
        self.category = category
        self.place = place

    @classmethod
    def from_dict(cls, data):
        # Ensure that the data keys exactly match those expected
        return cls(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            place=data['place']
        )

    def to_dict(self):
        # This method is for serialization, ensuring compatibility with JSON structure
        return {
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'place': self.place,
        }

class FoodCategory:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, item):
        self.items.append(item)

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.categories = []  # This will store FoodCategory objects

    def add_food(self, food_dict):
        # Find category of the food, if exists append food to it, if not create a new category
        category_found = None
        for category in self.categories:
            if category.name == food_dict['category']:
                category_found = category
                break

        if not category_found:
            # If the category was not found, create a new one and add it to the list
            category_found = FoodCategory(food_dict['category'])
            self.categories.append(category_found)

        # Add the food item to the found or newly created category's items list
        category_found.add_item(food_dict)

class FoodItemCollection:
    def __init__(self, collection):
        self.collection = collection

    def transformCollection(self):
        transformed = []

        for item in self.collection:
            # Attempt to find an existing restaurant in the transformed list
            restaurant_found = None
            for restaurant in transformed:
                if restaurant.name == item.place:
                    restaurant_found = restaurant
                    break

            if not restaurant_found:
                # If the restaurant was not found, create a new one and add it to the list
                restaurant_found = Restaurant(item.place)
                transformed.append(restaurant_found)

            # Add the food item to the found or newly created restaurant's foods list
            restaurant_found.add_food(item.to_dict())  # Assuming you want the item as a dictionary

        return transformed