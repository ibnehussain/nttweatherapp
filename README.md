# NTT Weather App 🌦️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![GitHub issues](https://img.shields.io/github/issues/ibnehussain/nttweatherapp)](https://github.com/ibnehussain/nttweatherapp/issues)
[![GitHub stars](https://img.shields.io/github/stars/ibnehussain/nttweatherapp)](https://github.com/ibnehussain/nttweatherapp/stargazers)

A responsive web application that provides real-time weather information for cities worldwide. Built with HTML, CSS, JavaScript frontend and Python Flask backend, powered by the OpenWeatherMap API.

🚀 **[Live Demo](https://ibnehussain.github.io/nttweatherapp)** | 📖 **[Documentation](docs/)** | 🐛 **[Report Bug](https://github.com/ibnehussain/nttweatherapp/issues)**

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment-options)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- 🌤️ **Real-time Weather Data** - Current weather conditions for any city
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices  
- 🔄 **Smart Caching** - Reduces API calls with 15-minute data caching
- 🌡️ **Temperature Units** - Toggle between Celsius and Fahrenheit
- 📍 **Location Details** - Coordinates, sunrise/sunset times, and weather specifics
- 📝 **Recent Searches** - Quick access to previously searched cities
- ⚡ **Fast Performance** - Optimized API calls and caching layer

## Architecture

```
Frontend (HTML/CSS/JS) ↔ Flask Backend ↔ OpenWeatherMap API
                      ↕
                 Cache Layer
```

### Data Flow
1. User enters city name in frontend form
2. JavaScript sends AJAX request to Flask API endpoint
3. Flask backend validates input and checks cache
4. If cache miss, fetch data from OpenWeatherMap API  
5. Process and format API response
6. Cache successful responses for 15 minutes
7. Return JSON data to frontend
8. Frontend updates UI with weather information

## Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenWeatherMap API key (free at https://openweathermap.org/api)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ibnehussain/nttweatherapp.git
   cd nttweatherapp
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   # or cp .env.example .env  # Linux/macOS
   ```
   
   Edit `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHERMAP_API_KEY=your_actual_api_key_here
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Visit `http://localhost:5000`

## API Documentation

### Endpoints

#### `POST /api/weather`
Get weather data for a city.

**Request Body:**
```json
{
  "city": "London",
  "units": "metric"  // optional: metric, imperial, kelvin
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "city": "London, UK",
    "coordinates": {"lat": 51.51, "lon": -0.13},
    "current": {
      "temperature": 15.2,
      "feels_like": 14.1,
      "temp_min": 12.8,
      "temp_max": 17.5,
      "humidity": 72,
      "pressure": 1013,
      "description": "Partly Cloudy",
      "icon": "02d",
      "wind_speed": 3.6,
      "wind_direction": 250
    },
    "units": {
      "temperature": "°C",
      "wind_speed": "m/s",
      "pressure": "hPa"
    },
    "sun": {
      "sunrise": "2026-02-11T07:15:00Z",
      "sunset": "2026-02-11T17:30:00Z"
    },
    "timestamp": "2026-02-11T10:30:00Z"
  }
}
```

#### `GET /api/health`
Health check endpoint.

#### `GET /api/weather/<city>`
Get cached weather data for a city.

### Error Responses

```json
{
  "status": "error", 
  "message": "Error description"
}
```

**Common Error Codes:**
- `400` - Invalid input (missing city, invalid format)
- `404` - City not found
- `429` - Rate limit exceeded
- `500` - Internal server error

## Project Structure

```
nttweatherapp/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration management
│   ├── requirements.txt       # Python dependencies
│   └── services/
│       ├── weather_service.py # OpenWeatherMap integration
│       ├── cache_service.py   # In-memory caching
│       ├── mock_weather_service.py # Test data provider
│       └── __init__.py
├── frontend/
│   ├── index.html            # Main UI
│   ├── style.css             # Responsive styles
│   └── script.js             # Frontend logic
├── docs/                     # Comprehensive documentation
│   ├── README.md             # Documentation index
│   ├── API_REFERENCE.md      # Detailed API documentation
│   ├── DEVELOPMENT.md        # Developer setup and guidelines
│   ├── ARCHITECTURE.md       # Technical architecture details
│   ├── TESTING.md           # Testing strategies and examples
│   ├── CONTRIBUTING.md      # Contribution guidelines
│   └── CHANGELOG.md         # Version history
├── tests/
│   └── test_basic.py         # API endpoint tests
├── .env.example              # Environment template
└── README.md                 # This file
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHERMAP_API_KEY` | Your OpenWeatherMap API key | Required |
| `FLASK_DEBUG` | Enable debug mode | False |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `CACHE_DEFAULT_TTL` | Cache time-to-live (seconds) | 900 |
| `REQUEST_TIMEOUT` | API request timeout | 10 |

### OpenWeatherMap API

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key from the dashboard
3. Add it to your `.env` file

**API Limits:**
- Free tier: 1,000 calls/day, 60 calls/minute
- Paid tiers available for higher limits

## Development

### Running Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Code Style
The project follows Python PEP 8 standards and uses:
- Descriptive variable names
- Comprehensive error handling
- Structured logging
- Clear separation of concerns

## Deployment Options

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Azure App Service
1. Create Azure App Service
2. Set environment variables in Configuration
3. Deploy code via Git or ZIP

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

## Troubleshooting

### Common Issues

**"API key not configured"**
- Ensure `.env` file exists with valid `OPENWEATHERMAP_API_KEY`
- Restart Flask server after adding API key

**"City not found"**
- Check city name spelling
- Try adding country code: "Paris, FR"
- Use English city names

**"Rate limit exceeded"** 
- Wait 1 minute before next request
- Consider upgrading OpenWeatherMap plan

**Frontend not loading**
- Ensure Flask server is running on port 5000
- Check browser console for JavaScript errors
- Verify CORS configuration in Flask

### Performance Optimization

- **Caching**: Weather data cached for 15 minutes
- **Compression**: Enable gzip in production
- **CDN**: Use CDN for static assets
- **Minification**: Minify CSS/JS for production

## Documentation

For detailed information about the project, see the [docs](docs/) directory:

- **[Development Guide](docs/DEVELOPMENT.md)** - Complete setup and development workflow
- **[API Reference](docs/API_REFERENCE.md)** - Detailed API documentation  
- **[Architecture Overview](docs/ARCHITECTURE.md)** - Technical architecture and design
- **[Testing Guide](docs/TESTING.md)** - Testing strategies and examples
- **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute to the project
- **[Version History](docs/CHANGELOG.md)** - Detailed changelog and release notes

## Future Enhancements

- [ ] 5-day weather forecast
- [ ] Interactive weather maps
- [ ] Weather alerts and notifications  
- [ ] PWA support with offline capability
- [ ] User authentication and saved locations
- [ ] Historical weather data charts
- [ ] Azure Cosmos DB integration for user data

## Technologies Used

- **Frontend**: HTML5, CSS3 (Grid/Flexbox), Vanilla JavaScript
- **Backend**: Python Flask, Requests
- **API**: OpenWeatherMap REST API  
- **Caching**: In-memory with TTL
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome

## Contributing 🤝

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/nttweatherapp.git
   cd nttweatherapp
   ```
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and add tests
5. **Run tests** to ensure everything works
   ```bash
   cd backend && python -m pytest tests/ -v
   ```
6. **Commit your changes**
   ```bash
   git commit -am "Add: your feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request** on GitHub

### Development Setup

```bash
# Setup development environment
git clone https://github.com/ibnehussain/nttweatherapp.git
cd nttweatherapp
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
cp .env.example .env  # Add your OpenWeatherMap API key
python backend/app.py
```

## License

MIT License - see LICENSE file for details.

## Support 💬

Need help? Here are your options:

### 🔍 First, try these resources:
1. **[Troubleshooting Guide](#troubleshooting)** - Common issues and solutions
2. **[API Documentation](docs/API_REFERENCE.md)** - Complete API reference
3. **[Development Guide](docs/DEVELOPMENT.md)** - Setup and development workflow

### 💡 Still need help?
- **[Create an Issue](https://github.com/ibnehussain/nttweatherapp/issues)** - For bugs or feature requests
- **[Discussions](https://github.com/ibnehussain/nttweatherapp/discussions)** - For questions and community support
- **[OpenWeatherMap Docs](https://openweathermap.org/api)** - For weather API questions

### 📧 Contact
- Email: your.email@example.com
- Twitter: [@yourusername](https://twitter.com/yourusername)