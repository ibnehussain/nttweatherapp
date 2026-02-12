# Development Guide

Comprehensive guide for developers working on the Weather Dashboard project.

## Development Environment Setup

### Prerequisites
- **Python 3.8+** (3.9+ recommended)
- **Git** for version control
- **Visual Studio Code** (recommended) with Python extension
- **OpenWeatherMap API Key** (free at https://openweathermap.org/api)

### Initial Setup

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd nttdemoapp
   ```

2. **Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Linux/macOS) 
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   # Copy template (create this file)
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/macOS
   ```

5. **Configure .env file**
   ```env
   OPENWEATHERMAP_API_KEY=your_api_key_here
   FLASK_DEBUG=True
   TEST_MODE=False
   SECRET_KEY=your-dev-secret-key
   ```

---

## Project Architecture

### High-Level Structure
```
Frontend (Static Files) → Flask App → Weather Services → External APIs
                        ↕
                   Cache Layer
```

### Component Breakdown

**Backend Components:**
- **app.py** - Main Flask application with routes and error handling
- **config.py** - Configuration management and environment variables
- **services/weather_service.py** - OpenWeatherMap API integration
- **services/mock_weather_service.py** - Test data provider
- **services/cache_service.py** - In-memory caching with TTL

**Frontend Components:**
- **index.html** - Main UI structure and semantic HTML
- **style.css** - Responsive CSS with Grid/Flexbox
- **script.js** - Vanilla JavaScript for API interaction and DOM manipulation

---

## Code Organization Patterns

### Service Pattern
```python
class WeatherService:
    def __init__(self):
        # Initialize with configuration
        
    def get_weather_by_city(self, city, units='metric'):
        # Main business logic
        
    def _format_weather_response(self, api_data, units):
        # Private helper method
```

### Configuration Management
```python
class Config:
    # Environment-based configuration
    API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
    
    @staticmethod
    def validate_config():
        # Configuration validation
```

### Error Handling Strategy
```python
try:
    # API operation
except requests.exceptions.Timeout:
    # Specific timeout handling
except requests.exceptions.ConnectionError:
    # Network error handling  
except Exception as e:
    # Generic error fallback
```

---

## Development Workflow

### Running the Application

**Development Server:**
```bash
cd backend
python app.py
```

**With Debug Mode:**
```bash
export FLASK_DEBUG=True  # Linux/macOS
set FLASK_DEBUG=True     # Windows
python app.py
```

**Test Mode:**
```bash
export TEST_MODE=True
python app.py
```

### Testing

**Run All Tests:**
```bash
cd backend
python -m pytest tests/ -v
```

**Run Specific Test:**
```bash
python -m pytest tests/test_basic.py::test_health_check -v
```

**Test Coverage:**
```bash
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

---

## API Development

### Adding New Endpoints

1. **Define Route in app.py:**
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        # Validate input
        # Process request
        # Return response
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error message'}), 500
```

2. **Add Service Logic:**
```python
# In appropriate service file
def new_service_method(self, param):
    """Method documentation"""
    # Implementation
    return result
```

3. **Add Tests:**
```python
def test_new_endpoint(client):
    response = client.post('/api/new-endpoint', json={'param': 'value'})
    assert response.status_code == 200
```

### Response Format Standards

**Success Response:**
```python
{
    'status': 'success',
    'data': {
        # Actual data
    },
    'timestamp': datetime.utcnow().isoformat() + 'Z'
}
```

**Error Response:**
```python
{
    'status': 'error', 
    'message': 'Human-readable error message',
    'error_code': 'OPTIONAL_ERROR_CODE'
}
```

---

## Frontend Development

### JavaScript Patterns

**API Calls:**
```javascript
async function fetchWeatherData(city, units) {
    try {
        const response = await fetch('/api/weather', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city, units })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            return data;
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
```

**DOM Manipulation:**
```javascript
function updateWeatherDisplay(weatherData) {
    const elements = {
        temperature: document.getElementById('temperature'),
        description: document.getElementById('description'),
        city: document.getElementById('city-name')
    };
    
    elements.temperature.textContent = `${weatherData.current.temperature}°`;
    elements.description.textContent = weatherData.current.description;
    elements.city.textContent = weatherData.city;
}
```

### CSS Organization

**Mobile-First Responsive Design:**
```css
/* Base mobile styles */
.container { 
    padding: 1rem; 
}

/* Tablet styles */
@media (min-width: 768px) {
    .container { 
        padding: 2rem; 
    }
}

/* Desktop styles */
@media (min-width: 1024px) {
    .container { 
        max-width: 1200px; 
        margin: 0 auto; 
    }
}
```

---

## Debugging and Troubleshooting

### Common Issues and Solutions

**API Key Not Working:**
```bash
# Check environment variable
echo $OPENWEATHERMAP_API_KEY  # Linux/macOS
echo %OPENWEATHERMAP_API_KEY% # Windows

# Verify in Python
python -c "from config import Config; print(Config.OPENWEATHERMAP_API_KEY)"
```

**CORS Issues:**
```python
# Ensure CORS is properly configured in app.py
CORS(app, origins=['http://localhost:3000', 'http://localhost:5000'])
```

**Cache Issues:**
```python
# Clear cache during development
cache_service.clear()
```

### Logging Configuration

**Enable Debug Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Custom Log Format:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Performance Optimization

### Backend Optimizations

**Caching Strategy:**
```python
# Weather data: 15 min TTL
# User preferences: 1 hour TTL
# Static data: 24 hours TTL
```

**Database Connections:**
```python
# Use connection pooling for production
# Implement proper error handling and retries
```

### Frontend Optimizations

**Asset Loading:**
- Minimize HTTP requests
- Use CDN for external libraries
- Implement proper caching headers

**JavaScript Performance:**
```javascript
// Debounce search input
const debouncedSearch = debounce(searchWeather, 300);

// Use efficient DOM queries
const weatherContainer = document.getElementById('weather-container');
```

---

## Code Quality Standards

### Python Code Standards

**PEP 8 Compliance:**
```bash
pip install flake8 black
black backend/  # Format code
flake8 backend/ # Check style
```

**Type Hints:**
```python
from typing import Dict, List, Optional

def format_weather_data(data: Dict) -> Dict[str, Any]:
    """Format weather data with proper type hints"""
    return formatted_data
```

**Documentation:**
```python
def fetch_weather_data(city: str, units: str = 'metric') -> Dict:
    """
    Fetch weather data for a given city.
    
    Args:
        city: City name to fetch weather for
        units: Temperature units (metric, imperial, kelvin)
        
    Returns:
        Dictionary containing weather data and status
        
    Raises:
        ValueError: If city name is invalid
        ConnectionError: If API is unreachable
    """
```

### JavaScript Standards

**ES6+ Features:**
```javascript
// Use const/let instead of var
const API_BASE_URL = '/api';
let weatherData = null;

// Arrow functions for callbacks
cities.map(city => ({ name: city, formatted: city.toLowerCase() }));

// Destructuring assignment
const { temperature, humidity, description } = weatherData.current;
```

---

## Git Workflow

### Branch Naming
- `feature/add-weather-alerts`
- `bugfix/fix-cache-expiry`
- `hotfix/security-patch`

### Commit Messages
```
feat: add 5-day weather forecast endpoint

- Add forecast service method
- Create new API endpoint /api/forecast
- Add forecast data formatting
- Include comprehensive tests

Closes #123
```

### Code Review Checklist
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No sensitive data in commits
- [ ] Error handling implemented
- [ ] Performance considerations addressed

---

## Deployment Preparation

### Environment Validation
```python
# Add to config.py
@staticmethod
def validate_production_config():
    required_vars = [
        'OPENWEATHERMAP_API_KEY',
        'SECRET_KEY'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
```

### Production Considerations
- Set `FLASK_DEBUG=False`
- Use proper SECRET_KEY
- Configure proper logging level
- Set up monitoring and health checks
- Implement proper rate limiting
- Use HTTPS in production

---

## Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Python Requests](https://docs.python-requests.org/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [HTTPie](https://httpie.io/) - Command line HTTP client
- [VS Code REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) - API testing in VS Code

### Extensions for VS Code
- Python
- Pylance
- Python Docstring Generator
- REST Client
- GitLens