"""
Mock Weather Service for testing
Provides dummy weather data without external API calls
"""

import random
from datetime import datetime

class MockWeatherService:
    def __init__(self):
        self.mock_data = {
            'london': {
                'temperature': 18,
                'description': 'Partly cloudy',
                'humidity': 65,
                'wind_speed': 12,
                'weather_icon': '02d'
            },
            'tokyo': {
                'temperature': 25,
                'description': 'Sunny',
                'humidity': 58,
                'wind_speed': 8,
                'weather_icon': '01d'
            },
            'new york': {
                'temperature': 22,
                'description': 'Light rain',
                'humidity': 78,
                'wind_speed': 15,
                'weather_icon': '10d'
            },
            'paris': {
                'temperature': 16,
                'description': 'Overcast',
                'humidity': 72,
                'wind_speed': 10,
                'weather_icon': '04d'
            },
            'sydney': {
                'temperature': 28,
                'description': 'Clear sky',
                'humidity': 55,
                'wind_speed': 18,
                'weather_icon': '01d'
            },
            'mumbai': {
                'temperature': 32,
                'description': 'Thunderstorm',
                'humidity': 85,
                'wind_speed': 22,
                'weather_icon': '11d'
            },
            'berlin': {
                'temperature': 14,
                'description': 'Light snow',
                'humidity': 68,
                'wind_speed': 14,
                'weather_icon': '13d'
            },
            'moscow': {
                'temperature': -5,
                'description': 'Heavy snow',
                'humidity': 82,
                'wind_speed': 25,
                'weather_icon': '13d'
            }
        }

    def get_weather_by_city(self, city, units='metric'):
        """
        Get mock weather data for a city
        """
        city_key = city.lower().strip()
        
        if city_key not in self.mock_data:
            return {
                'status': 'error',
                'message': f'City "{city}" not found in test data'
            }

        base_data = self.mock_data[city_key].copy()
        
        # Add some randomness to make it more realistic
        temp_variation = random.randint(-3, 3)
        base_data['temperature'] += temp_variation
        base_data['humidity'] += random.randint(-5, 5)
        base_data['wind_speed'] += random.randint(-2, 2)
        
        # Convert temperature if units are imperial
        if units == 'imperial':
            base_data['temperature'] = (base_data['temperature'] * 9/5) + 32
            base_data['wind_speed'] *= 2.237  # Convert m/s to mph

        return {
            'status': 'success',
            'city': city.title(),
            'country': 'Test Country',
            'temperature': base_data['temperature'],
            'description': base_data['description'],
            'humidity': max(0, min(100, base_data['humidity'])),
            'wind_speed': max(0, base_data['wind_speed']),
            'weather_icon': base_data['weather_icon'],
            'units': units,
            'timestamp': datetime.now().isoformat(),
            'is_mock_data': True
        }

    def get_available_cities(self):
        """Get list of available test cities"""
        return list(self.mock_data.keys())

    def get_current_timestamp(self):
        """Get current timestamp"""
        return datetime.now().isoformat()
