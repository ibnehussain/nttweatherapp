# Contributing to Weather Dashboard

We welcome contributions to the Weather Dashboard project! This document outlines the process for contributing and the standards we follow.

## Getting Started

### Prerequisites
- Python 3.8+ installed
- Git for version control
- OpenWeatherMap API key for testing
- Basic knowledge of Flask and JavaScript

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Follow the setup instructions in [DEVELOPMENT.md](DEVELOPMENT.md)
4. Create a feature branch from `main`

## Contribution Process

### 1. Issue Selection
- Check existing issues for available work
- Comment on an issue to indicate you're working on it
- For new features, create an issue first to discuss the approach

### 2. Development
- Create a feature branch: `git checkout -b feature/your-feature-name`
- Follow the coding standards outlined below
- Write tests for new functionality
- Update documentation as needed

### 3. Testing
- Run all tests: `python -m pytest tests/ -v`
- Test manually in both normal and test modes
- Verify frontend functionality across different browsers
- Check responsive design on mobile devices

### 4. Commit Guidelines
Follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Examples:**
- `feat: add 5-day weather forecast endpoint`
- `fix: resolve cache expiry issue`
- `docs: update API documentation`
- `test: add unit tests for weather service`

### 5. Pull Request
- Push your branch to your fork
- Create a pull request to the main repository
- Fill out the pull request template completely
- Ensure all checks pass

## Code Standards

### Python Code Style

**Follow PEP 8:**
```python
# Use descriptive variable names
weather_data = get_weather_by_city(city_name)

# Proper function documentation
def format_temperature(temp: float, unit: str) -> str:
    """
    Format temperature with appropriate unit symbol.
    
    Args:
        temp: Temperature value
        unit: Unit type ('metric', 'imperial', 'kelvin')
        
    Returns:
        Formatted temperature string with unit symbol
    """
    symbols = {'metric': '°C', 'imperial': '°F', 'kelvin': 'K'}
    return f"{temp:.1f}{symbols.get(unit, '')}"
```

**Error Handling:**
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    logger.error(f"Timeout fetching data from {url}")
    return create_error_response("Request timeout")
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {str(e)}")
    return create_error_response("Service unavailable")
```

### JavaScript Code Style

**ES6+ Standards:**
```javascript
// Use const/let, avoid var
const API_ENDPOINT = '/api/weather';
let currentWeatherData = null;

// Arrow functions for short callbacks
const formatTemperature = (temp, unit) => `${temp}°${unit}`;

// Async/await for API calls
async function fetchWeatherData(city) {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch weather:', error);
        throw new Error('Weather service unavailable');
    }
}
```

### CSS Code Style

**Organized Structure:**
```css
/* Use consistent naming convention */
.weather-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.weather-card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.weather-card__temperature {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
}

/* Mobile-first responsive design */
@media (min-width: 768px) {
    .weather-card {
        flex-direction: row;
        gap: 2rem;
    }
}
```

## API Guidelines

### Endpoint Design
- Use RESTful conventions
- Consistent response format
- Proper HTTP status codes
- Comprehensive error messages

### Request Validation
```python
@app.route('/api/weather', methods=['POST'])
def get_weather():
    # Validate request data
    if not request.json or 'city' not in request.json:
        return jsonify({
            'status': 'error',
            'message': 'City name is required'
        }), 400
    
    city = request.json['city'].strip()
    if not city or len(city) < 2:
        return jsonify({
            'status': 'error', 
            'message': 'Invalid city name'
        }), 400
```

### Response Format
```python
# Success response
{
    'status': 'success',
    'data': {
        # Actual data
    },
    'timestamp': '2026-02-12T15:30:00Z'
}

# Error response  
{
    'status': 'error',
    'message': 'Human-readable error description',
    'error_code': 'OPTIONAL_ERROR_CODE'
}
```

## Testing Guidelines

### Unit Tests
```python
def test_format_weather_response():
    """Test weather response formatting"""
    service = WeatherService()
    mock_data = {
        'name': 'London',
        'main': {'temp': 18.5, 'humidity': 65},
        'weather': [{'description': 'Partly cloudy'}]
    }
    
    result = service._format_weather_response(mock_data, 'metric')
    
    assert result['status'] == 'success'
    assert result['data']['current']['temperature'] == 18.5
    assert result['data']['current']['humidity'] == 65
```

### Integration Tests
```python
def test_weather_endpoint_success(client):
    """Test successful weather API call"""
    response = client.post('/api/weather', json={
        'city': 'London',
        'units': 'metric'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'current' in data['data']
```

### Frontend Testing
- Test form validation
- Verify error message display
- Check responsive layout
- Validate accessibility features

## Documentation Requirements

### Code Documentation
- Docstrings for all public functions
- Inline comments for complex logic
- Type hints where applicable

### API Documentation
- Update API_REFERENCE.md for new endpoints
- Include request/response examples
- Document error conditions

### User Documentation
- Update README.md for user-facing changes
- Add setup instructions for new dependencies
- Update troubleshooting section as needed

## Review Checklist

Before submitting a pull request, ensure:

**Code Quality:**
- [ ] Code follows style guidelines
- [ ] No commented-out code
- [ ] No TODO comments without issue references
- [ ] No hardcoded sensitive values

**Testing:**
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Edge cases covered
- [ ] Manual testing completed

**Documentation:**
- [ ] Code documented appropriately
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Changelog entry added

**Security:**
- [ ] No sensitive data in commits
- [ ] Input validation implemented
- [ ] Error messages don't leak information
- [ ] Dependencies are secure

## Feature Development Process

### New Feature Workflow
1. **Issue Creation**: Create detailed issue with requirements
2. **Design Discussion**: Discuss implementation approach
3. **Implementation**: Follow coding standards
4. **Testing**: Comprehensive test coverage
5. **Documentation**: Update all relevant docs
6. **Review**: Address feedback from code review
7. **Merge**: Squash commits and merge

### Example Feature Branches
- `feature/weather-alerts`
- `feature/user-location-save`
- `feature/weather-history`
- `enhancement/improved-caching`
- `bugfix/ios-display-issue`

## Community Guidelines

### Communication
- Be respectful and constructive
- Ask questions if requirements are unclear
- Provide helpful feedback on pull requests
- Share knowledge and best practices

### Issue Reporting
- Use issue templates when available
- Provide detailed reproduction steps
- Include environment information
- Add relevant labels

### Code of Conduct
- Treat all contributors with respect
- Focus on constructive feedback
- Be patient with new contributors
- Follow the project's code of conduct

## Getting Help

### Resources
- **Documentation**: Check existing docs first
- **Issues**: Search existing issues for similar problems
- **Discussion**: Use GitHub Discussions for questions
- **Code Examples**: Refer to existing codebase patterns

### Contact
- Create an issue for bugs or feature requests
- Use discussions for questions and ideas
- Tag maintainers for urgent issues

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Notes
- Summarize all changes since last release
- Include breaking changes with migration guide
- Credit contributors
- Link to relevant issues and PRs

Thank you for contributing to the Weather Dashboard! 🌤️