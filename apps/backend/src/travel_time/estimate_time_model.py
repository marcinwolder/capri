import json

from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

from src.backend.get_recommendation import get_attractions
from src.data_model.city.city import City
from src.path import get_path
from src.route_optimalization.haversine import calculate_distance
from src.travel_time.travel_time import travel_estimator
from joblib import dump


def get_travel_data():
    places_list, restaurants_list = get_attractions(None, City.get_const_krakow(),
                                                    None, from_file=True)
    data = []

    def append_data(place, place2):
        if place == place2:
            return
        distance = calculate_distance(place.location.latitude, place.location.longitude,
                                      place2.location.latitude, place2.location.longitude)
        transport = 'foot' if distance <= 5 else 'car'
        osm = travel_estimator.get_travel_time(place.location, place2.location, transport=transport)
        data.append({
            "start": place.placeInfo.id,
            "end": place2.placeInfo.id,
            "distance": distance,
            'real_distance': osm[1],
            "time": osm[0],
            "transport": transport
        })

    def save_data():
        with open('../ml_operations/travel_data.json', 'w') as f:
            json.dump(data, f, default=vars)

    try:
        for place in places_list.get_list():
            for place2 in places_list.get_list():
                append_data(place, place2)
        for place in restaurants_list.get_list():
            for place2 in restaurants_list.get_list():
                append_data(place, place2)
    except:
        save_data()
    save_data()


def train_model(car=True):
    
    with open(get_path('travel_data.json', 'time_estimation_models'), 'r') as file:
        data = json.load(file)

    
    if car:
        data = [i for i in data if i['distance'] > 5]
    else:
        data = [i for i in data if i['distance'] <= 5]

    
    distances = np.array([d["distance"] for d in data]).reshape(-1, 1)  
    times = np.array([d["time"] / 60 / 60 for d in data])  

    
    distances_train, distances_test, times_train, times_test = train_test_split(distances, times, test_size=0.2,
                                                                                random_state=42)

    
    model = LinearRegression()
    model.fit(distances_train, times_train)

    
    times_pred = model.predict(distances_test)

    
    mse = mean_squared_error(times_test, times_pred)
    r2 = r2_score(times_test, times_pred)

    
    print("Coefficient (Slope):", model.coef_[0])
    print("Intercept:", model.intercept_)
    print("Mean Squared Error (MSE):", mse)
    print("R-squared (R²):", r2)

    times_pred = model.predict(distances_test)

    
    plt.figure(figsize=(10, 6))
    plt.scatter(distances_test, times_test, color='blue', label='Actual Data')
    plt.plot(distances_test, times_pred, color='red', label='Model Predictions')
    plt.title('Test Data vs. Model Predictions')
    plt.xlabel('Distance')
    plt.ylabel('Time (hours)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return model


if __name__ == "__main__":
    
    model_car = train_model(car=True)
    
    model_foot = train_model(car=False)
    
