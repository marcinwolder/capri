import argparse
import logging
import time
from datetime import date, datetime

from firebase_admin import auth
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS

from src.api_calls import get_restaurants_for_city
from src.backend.get_recommendation import get_recommendations, get_attractions
from src.backend.get_restaurants import get_restaurants
from src.backend.get_user_trip_history import get_user_trip_history, get_user_trip
from src.data_model import UserPreferences
from src.data_model.city.city import City
from src.data_model.user.user_info import TripInfo


from src.database import DataBase, DataBaseUsers
from src.rating.cumulative_rating import calculate_cumulative_rating
from src.twitter_tweepy.twitter_scraper import get_twitter_posts

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
parser.add_argument('-f', '--from_file', action='store_true', help='Read input from file')
parser.add_argument('-n', '--no_db', action='store_true', help='Disable database interaction')
args = parser.parse_args()
debug, from_file, no_db = args.debug, args.from_file, args.no_db

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})


db = None
db_users = DataBaseUsers()




@app.route('/api/trip-history/<trip_id>', methods=['GET'])
def trip_details(trip_id):
    token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        trip = get_user_trip(db, db_users, token, trip_id)
        print('\n\n\n\n', trip)
        return jsonify({'success': True, 'data': trip}), 200
    except auth.InvalidIdTokenError:
        logging.error("Invalid token")
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    except Exception as e:
        logging.exception(e.__str__())
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/trip-history', methods=['GET'])
def trip_history():
    token = request.headers.get('Authorization').split('Bearer ')[1]
    try:
        history = get_user_trip_history(db, db_users, token)
        return jsonify({'success': True, 'data': history}), 200
    except auth.InvalidIdTokenError:
        logging.error("Invalid token")
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    except Exception as e:
        logging.exception(e.__str__())
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/social_media', methods=['POST'])
async def social_media():
    """Check if loc exist in firebase db"""

    data = request.json
    user_preferences = await aspect_analyzer.get_preferences_from_twitter()
    print("user_preferences", user_preferences)
    user_specified_needs = UserPreferences(data['user_preferences'], user_preferences, subcategories=[])
    recommendation, city_overview = get_recommendations(db, data, user_specified_needs, from_file=from_file)
    return jsonify({
        "status": "success",
        "received_data": recommendation
    })


async def social_media_debug():
    """Check if loc exist in firebase db"""

    user_preferences = await aspect_analyzer.get_preferences_from_twitter()
    print("user_preferences", user_preferences)


@app.route('/get_with_text', methods=['POST'])
def get_with_text():
    """Check if loc exist in firebase db."""

    data = request.json

    preferences = aspect_analyzer.get_preferences_from_text_data(data['text'])
    user_specified_needs = UserPreferences(data['user_preferences'], preferences, [])
    recommendation = get_recommendations(db, data, user_specified_needs, from_file=from_file)

    return jsonify({
        "status": "success",
        "received_data": recommendation
    })





@app.route('/api/recommendation/preferences', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_with_categories():
    """Check if loc exist in firebase db"""
    tic = time.perf_counter()
    data = request.json
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    print("data", data)
    categories = [category for category in data['preferences']['categories'].keys()]
    subcategories = data['preferences']['categories']
    dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data['dates']]
    
    user_specified_needs = UserPreferences(data['preferences']['needs'], data['preferences']['money'], categories,
                                           subcategories)
    try:
        recommendation = get_recommendations(db, db_users, data['user_id'], data['city_id'], data['days'], dates,
                                             user_specified_needs, from_file=from_file)
    except Exception as e:
        logging.exception(e.__str__())
        return jsonify({
            "status": "error",
            "received_data": e.__str__()
        })
    print("recommendation", recommendation)
    toc = time.perf_counter()
    print(f"Recommendation took {toc - tic:0.4f} seconds")
    return jsonify({
        "status": "success",
        "received_data": recommendation
    })


@app.route('/api/restaurants-nearby', methods=['GET'])
def search_restaurants():
    """for each item in eating_list find the closest time to eat
    and search for restaurants nearby

    Dla każdego typu jedzenia znajdź najbliższy czas przyjazdu, by o odpowiedniej godzinie
    zjeść odpowiedni posiłek
    """

    categories = request.args.get('categories')
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    city_id = int(request.args.get('city_id'))
    vegan = bool(int(request.args.get('vegan')))
    alcohol = bool(int(request.args.get('alcohol')))

    try:
        restaurants = get_restaurants(city_id, lat, lon, categories, vegan, alcohol)
        return jsonify({'success': True, 'data': restaurants}), 200
    except Exception as e:
        logging.exception(e.__str__())
        return jsonify({'success': False, 'message': str(e)}), 500


def run_debug(data):
    """Check if loc exist in firebase db"""

    
    categories = [category for category in data['categories'].keys()]
    subcategories = data['categories']
    user_specified_needs = UserPreferences(data['user_preferences'], categories, subcategories)
    recommendation = get_recommendations(db, data, user_specified_needs, from_file=from_file)
    print("recommendation", recommendation)


def save_to_file(data):
    categories = [category for category in data['categories'].keys()]
    subcategories = data['categories']
    user_needs = UserPreferences(data['user_preferences'], categories, subcategories)
    city = City(data['city_id'])
    open_ai_client = OpenAIClient()
    user = TripInfo(user_preferences=user_needs, city=city, days=data['days'])

    places_list = get_attractions(db=db, city=city, user_preferences=user, from_file=from_file)


def _make_dict():
    """Check if loc exist in firebase db."""
    return {
        "days": 1,
        "categories": {"museum": ["Art", "History", "Science", "War", "Maritime"],
                       "park": [], "zoo": [], "church": [],
                       },
        "restaurant": ["Polish", "Italian", "French", "Asian", "American"],
        "city_id": City.get_const_krakow().id,
        'use_saved_preferences': False,  
        "user_preferences":
            {"wheelchairAccessible": True,
             "family_friendly": False,
             "allowsDogs": True,
             "outdoor": True,
             
             "price_level": 1,
             "goodForGroups": True,
             "vegan": True,
             "children": True,
             "alcohol": True
             },
        "user_id": "user_id",
        "location": {"latitude": 50.06143, "longitude": 19.93658}

    }


def debug_users(data):
    """Check if loc exist in firebase db"""

    
    
    
    user = TripInfo(user_id=data['user_id'],
                    location=data['location'],
                    category_preferences=data['categories'],
                    user_preferences=data['user_preferences'],
                    city=City(data['city_id']),
                    days=data['days']
                    )
    if db_users.check_if_user_exist(user):
        print("User exist in database")
        if data['use_saved_preferences']:  
            
            preferences = data['user_preferences']
        else:
            db_users.update_user(user)
    else:
        print("User does not exist in database")
        db_users.add_user_to_database(user)
    
    
    


if __name__ == '__main__':

    
    
    if not no_db:
        db = DataBase()
    if debug:
        print("running debug")
        run_debug(_make_dict())
        
    else:
        app.run(debug=True, port=5000)
