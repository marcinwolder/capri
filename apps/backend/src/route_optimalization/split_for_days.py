from datetime import date, timedelta
from typing import List
import numpy as np

from src.data_model.place.place import Place
from src.data_model.places.places import Places
from src.ml_operations.kmeans_constrained import constrained_kmeans


class SplitForDays:
    def __init__(self, from_date: date, to_date: date, places: Places):
        self.fixed_places = None
        self.days_with_open_places = None
        self.places = places
        self.days = (to_date - from_date).days + 1
        self.weekday_indices = self.get_weekday_indices(from_date, to_date)
        self.open_places = None

    @staticmethod
    def get_weekday_indices(start, end):
        current_date = start
        weekdays = []
        while current_date <= end:
            
            weekday_index = (current_date.weekday() + 1) % 7
            weekdays.append(weekday_index)
            current_date += timedelta(days=1)
        return weekdays

    def get_places_to_days(self) -> dict[str, List[int]]:
        places_to_days = {}
        for place in self.places.get_list():
            days = []
            for i in self.weekday_indices:
                if place.regularOpeningHours.periods[i].open_today:
                    days.append(i)
            places_to_days[place.placeInfo.id] = days
        return places_to_days

    def split(self):
        places_to_days = self.get_places_to_days()
        places_to_days = {place_id: days for place_id, days in places_to_days.items() if len(days) > 0}

        self.open_places = Places([self.places.get_place_by_id(place_id) for place_id in places_to_days.keys()],
                                  city=self.places.city)

        
        data = []
        fixed_clusters = {}
        flexible_clusters = {}

        for i, (place_id, days) in enumerate(places_to_days.items()):
            if len(days) == 0:
                continue
            if len(days) == 1:
                fixed_clusters[i] = self.weekday_indices.index(days[0])
            else:
                flexible_clusters[i] = [self.weekday_indices.index(day) for day in days]

            place = self.open_places.get_place_by_id(place_id)
            data.append([place.location.latitude, place.location.longitude, place.ratings.cumulative_rating * 10])

        data = np.array(data)

        
        k = self.days  
        centroids, cluster_assignment, w_averages = constrained_kmeans(
            data=data,
            k=k,
            fixed_clusters=fixed_clusters,
            flexible_clusters=flexible_clusters
        )
        split_places = {i: [] for i in self.weekday_indices}
        for i in range(len(self.open_places)):
            split_places[self.weekday_indices[cluster_assignment[i]]].append(self.open_places[i])
        return [Places(split_places[i], city=self.open_places.city) for i in self.weekday_indices]
