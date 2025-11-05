import json

from src.data_model.place.place_subclasses import *


@dataclass
class UserPreferences:
    """
    User preferences data model."""
    priceLevel: int
    accessibilityOptions: bool
    goodForGroups: bool
    
    servesVegetarianFood: bool
    children: bool
    alcohol: bool
    allowsDogs: bool
    categories: list[str]
    
    subcategories: dict[str, list | list[str]]
    restaurant_categories: list[str]

    def __init__(self, needs: list[str], priceLevel: int, categories: list[str],
                 subcategories: dict[str, list | list[str]]):
        self.priceLevel = priceLevel
        
        self.accessibilityOptions = 'wheelchairAccessible' in needs
        self.goodForGroups = 'goodForGroups' in needs
        
        self.servesVegetarianFood = 'vegan' in needs
        self.children = 'children' in needs
        self.alcohol = 'alcohol' in needs
        self.allowsDogs = 'allowsDogs' in needs
        self.categories = categories
        self.subcategories = subcategories
        self._handle_places_of_worship()
        self.restaurant_categories = []

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def _handle_places_of_worship(self):
        """Handle places of worship."""
        if 'place_of_worship' not in self.categories:
            return
        self.categories.remove('place_of_worship')
        pow = self.subcategories.pop('place_of_worship')
        if len(pow) == 0:
            pow = ['church', 'mosque', 'synagogue']
        for cat in pow:
            if cat == 'church':
                self.categories.append('church')
                self.subcategories['church'] = []
            elif cat == 'mosque':
                self.categories.append('mosque')
                self.subcategories['mosque'] = []
            elif cat == 'synagogue':
                self.categories.append('synagogue')
                self.subcategories['synagogue'] = []

    def to_json(self):
        return json.dumps(self.to_dict())

    def cat_weights(self):
        weights = {cat: 0 for cat in self.categories}
        for key, val in weights.items():
            weights[key] = len(self.subcategories[key])
        return weights

    def to_dict(self):
        return {
            "priceLevel": self.priceLevel,
            "wheelchairAccessible": self.accessibilityOptions,
            "goodForGroups": self.goodForGroups,
            "vegan": self.servesVegetarianFood,
            "children": self.children,
            "alcohol": self.alcohol,
            "allowsDogs": self.allowsDogs,
            "restaurant": self.restaurant_categories
        }


def debug():  
    preferences = {'art': 1, 'antique': 1, 'coffee': 1,
                   'nature': 1, 'museum': 1, 'theater': 1}

    user_preferences = UserPreferences(
        data=preferences,
        categories=['museum', 'park', 'zoo', 'church'],
        subcategories={'museum': ['Art', 'History', 'Science', 'War', 'Maritime'],
                       'park': [], 'zoo': [], 'church': []}
    )
    print(user_preferences.cat_weights())


if __name__ == "__main__":
    debug()
