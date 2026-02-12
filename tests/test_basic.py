"""
Basic tests for Weather Dashboard API
"""

import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.app import app
from backend.services.cache_service import CacheService
from backend.services.weather_service import WeatherService


@pytest.fixture
def client():
    """Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def cache_service():
    """Cache service instance"""
    return CacheService()


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_weather_endpoint_missing_city(client):
    """Test weather endpoint with missing city"""
    response = client.post('/api/weather', json={})
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'city name is required' in data['message'].lower()


def test_weather_endpoint_empty_city(client):
    """Test weather endpoint with empty city"""
    response = client.post('/api/weather', json={'city': ''})
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['status'] == 'error'


def test_weather_endpoint_short_city(client):
    """Test weather endpoint with very short city name"""
    response = client.post('/api/weather', json={'city': 'A'})
    assert response.status_code == 400
    
    data = response.get_json()
    assert data['status'] == 'error'
    assert 'at least 2 characters' in data['message']


def test_cached_weather_not_found(client):
    """Test getting cached weather for non-existent cache entry"""
    response = client.get('/api/weather/nonexistentcity')
    assert response.status_code == 404


def test_cache_service():
    """Test cache service basic functionality"""
    cache = CacheService()
    
    # Test set and get
    cache.set('test_key', {'data': 'test_value'}, ttl=60)
    result = cache.get('test_key')
    assert result is not None
    assert result['data'] == 'test_value'
    
    # Test non-existent key
    result = cache.get('nonexistent')
    assert result is None
    
    # Test delete
    success = cache.delete('test_key')
    assert success is True
    
    result = cache.get('test_key')
    assert result is None


def test_cache_service_ttl():
    """Test cache service TTL functionality"""
    import time
    cache = CacheService()
    
    # Set with very short TTL
    cache.set('test_ttl', 'test_value', ttl=1)
    
    # Should be available immediately
    result = cache.get('test_ttl')
    assert result == 'test_value'
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should be expired
    result = cache.get('test_ttl')
    assert result is None


def test_cache_service_stats():
    """Test cache service statistics"""
    cache = CacheService()
    cache.clear()  # Start with clean cache
    
    stats = cache.get_stats()
    assert stats['total_entries'] == 0
    assert stats['active_entries'] == 0
    
    cache.set('test1', 'value1')
    cache.set('test2', 'value2')
    
    stats = cache.get_stats()
    assert stats['total_entries'] == 2
    assert stats['active_entries'] == 2


def test_weather_service_api_key_validation():
    """Test weather service API key validation"""
    service = WeatherService()
    
    # This test depends on whether API key is configured
    # In a real test environment, you'd mock this
    is_valid = service.is_api_key_valid()
    assert isinstance(is_valid, bool)


def test_frontend_served(client):
    """Test that frontend files are served"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Weather Dashboard' in response.data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])