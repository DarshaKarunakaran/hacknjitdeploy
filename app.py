import requests
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

app = Flask(__name__)

def get_lat_long(city_name, state_code, country_code, API_key):
    try:
        res = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}')
        res.raise_for_status()  # Raise an error for bad responses
        data = res.json()
        if data:
            latitude = data[0].get('lat')
            longitude = data[0].get('lon')
            return latitude, longitude 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latitude and longitude: {e}")
    return None, None 

def get_current_air_pollution(lat, lon, API_key):
    try:
        res = requests.get(f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_key}')
        res.raise_for_status()  # Raise an error for bad responses
        return res.json()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching air pollution data: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/map')
def show_map():
    return render_template('map.html')

@app.route('/historical_data')
def historical_data():
    return render_template('historical.html')

@app.route('/airquality_simulator')
def airquality_simulator():
    return render_template('airquality_simulator.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api_key')
def get_api_key():
    return jsonify({'api_key': api_key})

@app.route('/get_data', methods=['GET'])
def get_data():
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    
    lat, lon = get_lat_long(city, state, country, api_key)
    if lat is not None and lon is not None:
        pollution_data = get_current_air_pollution(lat, lon, api_key)
        if pollution_data:
            return jsonify(pollution_data) 
    return jsonify({'error': 'Location not found or data retrieval failed'}), 404

if __name__ == '__main__':
    app.run(debug=True)
