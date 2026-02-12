"""
Weather Dashboard Flask Backend
Main application file with API endpoints
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from services.weather_service import WeatherService
from services.mock_weather_service import MockWeatherService
from services.cache_service import CacheService
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend communication
CORS(app)

# Initialize services
weather_service = MockWeatherService() if Config.TEST_MODE else WeatherService()
cache_service = CacheService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static frontend files"""
    return send_from_directory('../frontend', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'weather-dashboard',
        'timestamp': weather_service.get_current_timestamp(),
        'test_mode': Config.TEST_MODE
    })

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather data for a city"""
    try:
        # Validate request data
        if not request.json or 'city' not in request.json:
            return jsonify({
                'status': 'error',
                'message': 'City name is required'
            }), 400

        city = request.json['city'].strip()
        units = request.json.get('units', 'metric')

        # Validate city name
        if not city or len(city) < 2:
            return jsonify({
                'status': 'error',
                'message': 'Invalid city name. Please provide a valid city name.'
            }), 400

        # Check cache first
        cache_key = f"{city.lower()}_{units}"
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached data for {city}")
            return jsonify(cached_data)

        # Fetch from OpenWeatherMap API
        weather_data = weather_service.get_weather_by_city(city, units)
        
        if weather_data['status'] == 'error':
            return jsonify(weather_data), 404

        # Cache successful response for 15 minutes
        cache_service.set(cache_key, weather_data, ttl=900)
        
        logger.info(f"Fetched fresh weather data for {city}")
        return jsonify(weather_data)

    except Exception as e:
        logger.error(f"Error processing weather request: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error. Please try again later.'
        }), 500

@app.route('/api/weather/<city>', methods=['GET'])
def get_cached_weather(city):
    """Get cached weather data for a city"""
    try:
        units = request.args.get('units', 'metric')
        cache_key = f"{city.lower()}_{units}"
        cached_data = cache_service.get(cache_key)
        
        if cached_data:
            return jsonify(cached_data)
        else:
            return jsonify({
                'status': 'error',
                'message': 'No cached data found for this city'
            }), 404

    except Exception as e:
        logger.error(f"Error retrieving cached data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error retrieving cached data'
        }), 500

@app.route('/api/test/cities', methods=['GET'])
def get_test_cities():
    """Get available test cities (only works in test mode)"""
    if not Config.TEST_MODE:
        return jsonify({
            'status': 'error',
            'message': 'Test endpoints are only available in test mode'
        }), 403
    
    try:
        cities = weather_service.get_available_cities()
        return jsonify({
            'status': 'success',
            'cities': cities,
            'message': 'Available test cities'
        })
    except Exception as e:
        logger.error(f"Error getting test cities: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error retrieving test cities'
        }), 500

@app.route('/api/test/weather/random', methods=['GET'])
def get_random_weather():
    """Get weather for a random test city (only works in test mode)"""
    if not Config.TEST_MODE:
        return jsonify({
            'status': 'error',
            'message': 'Test endpoints are only available in test mode'
        }), 403
    
    try:
        import random
        cities = weather_service.get_available_cities()
        random_city = random.choice(cities)
        units = request.args.get('units', 'metric')
        
        weather_data = weather_service.get_weather_by_city(random_city, units)
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error getting random weather: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error retrieving random weather data'
        }), 500

@app.errorhandler(429)
def rate_limit_handler(e):
    """Handle rate limiting errors"""
    return jsonify({
        'status': 'error',
        'message': 'Too many requests. Please wait before making another request.',
        'retry_after': 60
    }), 429

@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error. Please try again later.'
    }), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)