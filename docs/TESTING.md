# Testing Guide

Comprehensive testing documentation for the Weather Dashboard application.

## Testing Strategy

The project uses a multi-layered testing approach:
- **Unit Tests** - Individual component functionality
- **Integration Tests** - API endpoint testing
- **Manual Testing** - User interface and workflow validation
- **Performance Testing** - Load and response time testing

## Running Tests

### Quick Test Run
```bash
cd backend
python -m pytest tests/ -v
```

### Detailed Test Run with Coverage
```bash
# Install coverage tools
pip install pytest-cov

# Run tests with coverage report
python -m pytest tests/ --cov=. --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### Running Specific Tests
```bash
# Run specific test file
python -m pytest tests/test_basic.py -v

# Run specific test function
python -m pytest tests/test_basic.py::test_health_check -v

# Run tests matching pattern
python -m pytest -k "weather" -v
```

## Test Structure

### Current Test Files
```
tests/
├── test_basic.py           # Basic API endpoint tests
├── test_weather_service.py # Weather service unit tests (to be added)
├── test_cache_service.py   # Cache service unit tests (to be added)
└── conftest.py            # Shared test fixtures (to be added)
```

## Unit Testing

### Weather Service Tests
```python
import pytest
from unittest.mock import patch, Mock
from backend.services.weather_service import WeatherService

class TestWeatherService:
    def setup_method(self):
        self.service = WeatherService()
    
    @patch('requests.get')
    def test_successful_weather_fetch(self, mock_get):
        """Test successful weather data retrieval"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'name': 'London',
            'main': {'temp': 18.5, 'humidity': 65},
            'weather': [{'description': 'Partly cloudy'}]
        }
        mock_get.return_value = mock_response
        
        result = self.service.get_weather_by_city('London', 'metric')
        
        assert result['status'] == 'success'
        assert result['data']['current']['temperature'] == 18.5
        
    @patch('requests.get')
    def test_city_not_found(self, mock_get):
        """Test handling of invalid city names"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = self.service.get_weather_by_city('InvalidCity123', 'metric')
        
        assert result['status'] == 'error'
        assert 'not found' in result['message']
        
    @patch('requests.get') 
    def test_api_timeout(self, mock_get):
        """Test handling of API timeouts"""
        mock_get.side_effect = requests.exceptions.Timeout()
        
        result = self.service.get_weather_by_city('London', 'metric')
        
        assert result['status'] == 'error'
        assert 'timeout' in result['message'].lower()
```

### Cache Service Tests
```python
import pytest
import time
from backend.services.cache_service import CacheService

class TestCacheService:
    def setup_method(self):
        self.cache = CacheService()
    
    def test_cache_set_and_get(self):
        """Test basic cache operations"""
        self.cache.set('test_key', 'test_value', ttl=60)
        
        result = self.cache.get('test_key')
        assert result == 'test_value'
        
    def test_cache_expiry(self):
        """Test cache expiration"""
        self.cache.set('expire_key', 'value', ttl=1)
        
        # Value should exist initially
        assert self.cache.get('expire_key') == 'value'
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Value should be None after expiry
        assert self.cache.get('expire_key') is None
        
    def test_cache_delete(self):
        """Test cache deletion"""
        self.cache.set('delete_key', 'value', ttl=60)
        assert self.cache.get('delete_key') == 'value'
        
        deleted = self.cache.delete('delete_key')
        assert deleted is True
        assert self.cache.get('delete_key') is None
        
    def test_cache_stats(self):
        """Test cache statistics"""
        self.cache.clear()
        self.cache.set('key1', 'value1', ttl=60)
        self.cache.set('key2', 'value2', ttl=60)
        
        stats = self.cache.get_stats()
        assert stats['total_entries'] == 2
        assert stats['active_entries'] == 2
```

## Integration Testing

### API Endpoint Tests
```python
import pytest
from backend.app import app

@pytest.fixture
def client():
    """Flask test client fixture"""
    app.config['TESTING'] = True
    app.config['TEST_MODE'] = True
    with app.test_client() as client:
        yield client

class TestWeatherAPI:
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        
    def test_weather_endpoint_success(self, client):
        """Test successful weather request"""
        response = client.post('/api/weather', json={
            'city': 'London',
            'units': 'metric'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'success'
        assert 'current' in data['data']
        
    def test_weather_endpoint_missing_city(self, client):
        """Test weather request without city"""
        response = client.post('/api/weather', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        assert 'required' in data['message']
        
    def test_weather_endpoint_invalid_city(self, client):
        """Test weather request with invalid city"""
        response = client.post('/api/weather', json={
            'city': 'X'  # Too short
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['status'] == 'error'
        
    def test_cached_weather_endpoint(self, client):
        """Test cached weather retrieval"""
        # First request should fetch data
        response1 = client.post('/api/weather', json={
            'city': 'London',
            'units': 'metric'
        })
        assert response1.status_code == 200
        
        # Second request should return cached data
        response2 = client.get('/api/weather/London?units=metric')
        assert response2.status_code == 200
        
        data = response2.get_json()
        assert data['status'] == 'success'
```

## Frontend Testing

### Manual Testing Checklist

**Basic Functionality:**
- [ ] Page loads without errors
- [ ] Search form accepts input
- [ ] Search button triggers request
- [ ] Loading spinner displays during requests
- [ ] Weather data displays correctly
- [ ] Error messages show for invalid cities
- [ ] Temperature units toggle correctly

**Responsive Design:**
- [ ] Mobile layout (320px - 768px)
- [ ] Tablet layout (768px - 1024px)
- [ ] Desktop layout (1024px+)
- [ ] Touch targets are appropriately sized
- [ ] Text remains readable at all sizes

**Browser Compatibility:**
- [ ] Chrome (latest 2 versions)
- [ ] Firefox (latest 2 versions)
- [ ] Safari (latest 2 versions)
- [ ] Edge (latest 2 versions)

**Accessibility:**
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Color contrast meets WCAG standards
- [ ] Focus indicators visible
- [ ] Alt text for weather icons

### JavaScript Testing
```javascript
// Example test setup for frontend (future enhancement)
describe('Weather Dashboard', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <input id="cityInput" type="text">
            <button id="searchBtn">Search</button>
            <div id="weatherDisplay"></div>
        `;
    });
    
    test('validates city input correctly', () => {
        const input = document.getElementById('cityInput');
        input.value = 'X';
        
        const isValid = validateCityInput(input.value);
        expect(isValid).toBeFalsy();
    });
    
    test('displays weather data correctly', async () => {
        const mockWeatherData = {
            status: 'success',
            data: {
                city: 'London, UK',
                current: { temperature: 18.5, description: 'Sunny' }
            }
        };
        
        await displayWeatherData(mockWeatherData);
        
        const display = document.getElementById('weatherDisplay');
        expect(display.textContent).toContain('London');
        expect(display.textContent).toContain('18.5');
    });
});
```

## Performance Testing

### Load Testing
```python
import time
import concurrent.futures
import requests

def test_concurrent_requests():
    """Test multiple concurrent weather requests"""
    def make_request():
        response = requests.post('http://localhost:5000/api/weather', 
                               json={'city': 'London'})
        return response.status_code
    
    # Test 10 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [future.result() for future in futures]
    
    # All requests should succeed
    assert all(status == 200 for status in results)
    
def test_cache_performance():
    """Test cache performance improvement"""
    start_time = time.time()
    
    # First request (cache miss)
    response1 = requests.post('http://localhost:5000/api/weather',
                            json={'city': 'London'})
    miss_time = time.time() - start_time
    
    start_time = time.time()
    
    # Second request (cache hit) 
    response2 = requests.post('http://localhost:5000/api/weather',
                            json={'city': 'London'})
    hit_time = time.time() - start_time
    
    # Cache hit should be significantly faster
    assert hit_time < miss_time / 2
```

## Test Data Management

### Mock Weather Data
```python
# Test fixtures for consistent testing
MOCK_WEATHER_RESPONSES = {
    'london': {
        'name': 'London',
        'main': {
            'temp': 18.5,
            'feels_like': 17.2,
            'humidity': 65,
            'pressure': 1013
        },
        'weather': [{'description': 'Partly cloudy', 'icon': '02d'}],
        'wind': {'speed': 3.6, 'deg': 250},
        'coord': {'lat': 51.5074, 'lon': -0.1278}
    },
    'tokyo': {
        'name': 'Tokyo',
        'main': {
            'temp': 25.0,
            'feels_like': 24.1,
            'humidity': 58,
            'pressure': 1020
        },
        'weather': [{'description': 'Sunny', 'icon': '01d'}],
        'wind': {'speed': 2.1, 'deg': 140},
        'coord': {'lat': 35.6762, 'lon': 139.6503}
    }
}
```

### Test Environment
```python
# conftest.py
import pytest
from backend.app import app
from backend.services.cache_service import CacheService

@pytest.fixture(scope='function')
def clean_cache():
    """Provide clean cache for each test"""
    cache = CacheService()
    cache.clear()
    yield cache
    cache.clear()

@pytest.fixture(scope='session')
def test_app():
    """Configure app for testing"""
    app.config['TESTING'] = True
    app.config['TEST_MODE'] = True
    return app
```

## Continuous Integration

### GitHub Actions Example
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        cd backend
        python -m pytest tests/ --cov=. --cov-report=xml
        
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Test Maintenance

### Adding New Tests
1. **Create test file** for new modules
2. **Follow naming convention**: `test_*.py`
3. **Include docstrings** for test methods
4. **Test both success and failure cases**
5. **Update this documentation** with new test categories

### Test Data Updates
- Keep mock data in sync with API changes
- Update test expectations when adding new features
- Maintain test data variety for edge cases

### Performance Benchmarks
- Establish baseline performance metrics
- Monitor test execution time
- Set up alerts for performance degradation

This comprehensive testing approach ensures the Weather Dashboard maintains high quality and reliability across all components.