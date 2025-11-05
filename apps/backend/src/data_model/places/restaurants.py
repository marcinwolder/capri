from src.data_model.city.city import City
from src.data_model.place.place import Place
from src.data_model.places.places import Places


class Restaurants:
    """A list of place with their attributes."""
    bar: Places
    coffee: Places
    dinner: Places
    lunch: Places
    breakfast: Places
    city: City
    _average_rating: float = -1
    _average_rating_count: float = -1

    def __init__(self, places_list=None, city: City = None):
        self.filter_restaurants(places_list)

    def filter_restaurants(self, restaurants):
        for place in restaurants.get_list():
            if place.dining.servesBreakfast:
                self.breakfast.set_place(place)
            if place.dining.servesLunch:
                self.lunch.set_place(place)
            if place.dining.servesDinner:
                self.dinner.set_place(place)
            if place.dining.servesCoffee:
                self.coffee.set_place(place)
            if place.alcohol.servesBeer or place.alcohol.servesWine or place.alcohol.servesCocktails:
                self.bar.set_place(place)

    def get_by_types(self):
        return [self.breakfast, self.lunch, self.dinner, self.coffee, self.bar]

    def get_list(self) -> list[Place]:
        """Returns a list of all place"""
        return self.breakfast + self.lunch + self.dinner + self.coffee + self.bar

