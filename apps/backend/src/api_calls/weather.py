from datetime import datetime, timedelta

import openmeteo_requests
import requests_cache
from retry_requests import retry


def get_weather(lat, lon):
	cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
	retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
	openmeteo = openmeteo_requests.Client(session=retry_session)

	url = 'https://api.open-meteo.com/v1/forecast'
	params = {
		'latitude': lat,
		'longitude': lon,
		'daily': 'weather_code',
		'forecast_days': 16,
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]

	daily = response.Daily()
	daily_weather_codes = daily.Variables(0).ValuesAsNumpy().tolist()
	return daily_weather_codes


def get_weather_for_dates(lat, lon, start_date, end_date):
	"""Get weather conditions for a specified range of dates within a 16-day forecast period.
	Returns a list of corresponding weather forecast.
	:param lat: Latitude of the location
	:param lon: Longitude of the location
	:param start_date: Start date as a date object
	:param end_date: End date as a date object
	:return: List of weather forecasts in WMO code format
	"""
	today = datetime.now().date()
	print(today, start_date, end_date)
	end_of_forecast = today + timedelta(days=16)

	if start_date < today or start_date > end_of_forecast:
		print('Start date is out of the forecastable range')
		return [None for _ in range((end_date - start_date).days + 1)]

	forecast_data = get_weather(lat, lon)
	interesting_days = []

	start_idx = (start_date - today).days
	full_end_idx = (end_date - today).days + 1
	end_idx = min(16, full_end_idx)
	print(start_idx, end_idx)

	for i in range(start_idx, end_idx):
		date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
		if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date:
			interesting_days.append(int(forecast_data[i]))
	for i in range(end_idx, full_end_idx):
		date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
		if start_date <= datetime.strptime(date, '%Y-%m-%d').date() <= end_date:
			interesting_days.append(None)
	return interesting_days
