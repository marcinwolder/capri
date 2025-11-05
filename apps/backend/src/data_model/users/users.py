from src.data_model.city.city import City
from src.data_model.user.user import User
from src.database import DataBaseUsers


class Users:
    raw_users = []
    users: list[User] = []

    def __init__(self, db):
        self.db = db

    def get_users_rated_data(self):
        """
        zbieramy wszystkie miejsca, w jakich był użyutkownik w danym mieście. Tworzymy dict[miasto: {id, ocena} ]
        Bierzemy następnie tylko te ocenione."""

        users = self.db.get_all_users()
        self.raw_users = users
        for user in users:
            trip_history = self.db.get_user_trip_history(user_id=user['id'])
            city_attr = {}
            for trip in trip_history:
                city = City(trip['city_id'])
                all_places_ids_with_rating = []
                for day in trip['days']:
                    for place in day['places']:
                        if 'user_rating' in place:
                            all_places_ids_with_rating.append(place)
                city_attr[city.name] = all_places_ids_with_rating
            user_class = User(id=user['id'], collaborative_filtering_dict=city_attr)
            self.users.append(user_class)
        return self.users

    def get_rated_data(self, user_id):
        return self.users[user_id].collaborative_filtering_dict

    def make_user_data(self):
        users = self.get_users_rated_data()
        ret_dict = {'user_id': [], 'item_id': [], 'rating': []}
        for user in users:
            dct = user.collaborative_filtering_dict
            vals = dct.values()
            vals = [j for i in vals for j in i]
            ret_dict['user_id'].extend([user.id] * len(vals))
            ret_dict['item_id'].extend([i['id'] for i in vals])
            ret_dict['rating'].extend([i['user_rating'] for i in vals])
        return ret_dict


def debug():
    users = Users(DataBaseUsers())
    
    
    print(users.make_user_data())


if __name__ == "__main__":
    debug()
    
