"""
Weather Service - OpenWeatherMap API Integration
Handles all weather data fetching and processing
"""

import requests
import logging
from datetime import datetime, timezone
from config import Config

logger = logging.getLogger(__name__)

class WeatherService:
    """Service class for OpenWeatherMap API integration"""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHERMAP_API_KEY
        self.base_url = Config.OPENWEATHERMAP_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        
        # Validate API key on initialization
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not configured")
    
    def get_weather_by_city(self, city, units='metric'):
        """
        Fetch current weather data for a city
        
        Args:
            city (str): City name
            units (str): Temperature units ('metric', 'imperial', 'kelvin')
            
        Returns:
            dict: Formatted weather data or error response
        """
        try:
            # Prepare API request
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }
            
            logger.info(f"Fetching weather data for {city}")
            
            # Make API request
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_response(data, units)
            
            elif response.status_code == 404:
                return {
                    'status': 'error',
                    'message': f'City "{city}" not found. Please check the spelling and try again.'
                }
            
            elif response.status_code == 401:
                logger.error("Invalid API key")
                return {
                    'status': 'error',
                    'message': 'Weather service temporarily unavailable. Please try again later.'
                }
            
            else:
                logger.error(f"API request failed with status {response.status_code}")
                return {
                    'status': 'error',
                    'message': 'Weather service temporarily unavailable. Please try again later.'
                }
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching weather for {city}")
            return {
                'status': 'error',
                'message': 'Request timeout. Please try again.'
            }
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error fetching weather for {city}")
            return {
                'status': 'error',
                'message': 'Unable to connect to weather service. Please check your internet connection.'
            }
            
        except Exception as e:
            logger.error(f"Unexpected error fetching weather for {city}: {str(e)}")
            return {
                'status': 'error',
                'message': 'An unexpected error occurred. Please try again later.'
            }
    
    def get_forecast_by_city(self, city, units='metric', days=5):
        """
        Fetch weather forecast for a city
        
        Args:
            city (str): City name
            units (str): Temperature units
            days (int): Number of forecast days (max 5)
            
        Returns:
            dict: Formatted forecast data or error response
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units,
                'cnt': days * 8  # API returns 3-hour intervals, so 8 per day
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_response(data, units)
            else:
                return {
                    'status': 'error',
                    'message': 'Unable to fetch forecast data.'
                }
                
        except Exception as e:
            logger.error(f"Error fetching forecast for {city}: {str(e)}")
            return {
                'status': 'error',
                'message': 'Unable to fetch forecast data.'
            }
    
    def _format_weather_response(self, data, units):
        """Format OpenWeatherMap current weather response"""
        
        # Determine temperature unit symbol
        temp_unit = '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
        
        return {
            'status': 'success',
            'data': {
                'city': f"{data['name']}, {data['sys']['country']}",
                'coordinates': {
                    'lat': data['coord']['lat'],
                    'lon': data['coord']['lon']
                },
                'current': {
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'temp_min': round(data['main']['temp_min'], 1),
                    'temp_max': round(data['main']['temp_max'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'visibility': data.get('visibility', 'N/A'),
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data.get('wind', {}).get('speed', 0),
                    'wind_direction': data.get('wind', {}).get('deg', 0)
                },
                'units': {
                    'temperature': temp_unit,
                    'wind_speed': 'm/s' if units == 'metric' else 'mph',
                    'pressure': 'hPa'
                },
                'sun': {
                    'sunrise': self._format_timestamp(data['sys']['sunrise']),
                    'sunset': self._format_timestamp(data['sys']['sunset'])
                },
                'timestamp': self.get_current_timestamp(),
                'source': 'OpenWeatherMap'
            }
        }
    
    def _format_forecast_response(self, data, units):
        """Format OpenWeatherMap forecast response"""
        temp_unit = '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
        
        forecast_items = []
        for item in data['list'][:40]:  # Limit to 5 days max
            forecast_items.append({
                'datetime': item['dt_txt'],
                'temperature': round(item['main']['temp'], 1),
                'description': item['weather'][0]['description'].title(),
                'icon': item['weather'][0]['icon'],
                'humidity': item['main']['humidity'],
                'wind_speed': item.get('wind', {}).get('speed', 0)
            })
        
        return {
            'status': 'success',
            'data': {
                'city': f"{data['city']['name']}, {data['city']['country']}",
                'forecast': forecast_items,
                'units': {
                    'temperature': temp_unit,
                    'wind_speed': 'm/s' if units == 'metric' else 'mph'
                },
                'timestamp': self.get_current_timestamp()
            }
        }
    
    def _format_timestamp(self, timestamp):
        """Convert Unix timestamp to ISO format"""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
    
    def get_current_timestamp(self):
        """Get current timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
    
    def is_api_key_valid(self):
        """Check if the API key is configured and basic validation"""
        return bool(self.api_key and len(self.api_key) == 32)