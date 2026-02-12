# API Reference

Complete API documentation for the Weather Dashboard backend.

## Base URL
```
http://localhost:5000/api
```

## Authentication
All endpoints use OpenWeatherMap API integration. No authentication required for client requests, but server requires `OPENWEATHERMAP_API_KEY` environment variable.

---

## Endpoints

### Health Check
Check service status and configuration.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "weather-dashboard", 
  "timestamp": "2026-02-12T10:30:00Z",
  "test_mode": false
}
```

**Status Codes:**
- `200` - Service is healthy

---

### Get Weather Data
Retrieve current weather information for a specified city.

**Endpoint:** `POST /api/weather`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "city": "London",           // Required: City name
  "units": "metric"           // Optional: metric|imperial|kelvin (default: metric)
}
```

**Successful Response:**
```json
{
  "status": "success",
  "data": {
    "city": "London, GB",
    "coordinates": {
      "lat": 51.5074,
      "lon": -0.1278
    },
    "current": {
      "temperature": 18.5,
      "feels_like": 17.2,
      "temp_min": 16.8,
      "temp_max": 20.1,
      "humidity": 65,
      "pressure": 1013,
      "description": "Partly Cloudy",
      "icon": "02d",
      "wind_speed": 3.6,
      "wind_direction": 250,
      "visibility": 10000,
      "uv_index": 3
    },
    "units": {
      "temperature": "°C",
      "wind_speed": "m/s",
      "pressure": "hPa"
    },
    "sun": {
      "sunrise": "2026-02-12T07:15:00Z",
      "sunset": "2026-02-12T17:30:00Z"
    },
    "timestamp": "2026-02-12T15:30:00Z",
    "cached": false
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "message": "City \"InvalidCity\" not found. Please check the spelling and try again."
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing/invalid city)
- `404` - City not found
- `500` - Internal server error

---

### Get Cached Weather Data
Retrieve cached weather data for a city without making new API calls.

**Endpoint:** `GET /api/weather/{city}`

**Parameters:**
- `city` (path) - City name
- `units` (query) - Temperature units (metric|imperial|kelvin)

**Example:**
```
GET /api/weather/London?units=metric
```

**Response:**
Same structure as POST `/api/weather` but only returns data if available in cache.

**Status Codes:**
- `200` - Cached data found
- `404` - No cached data available

---

## Test Mode Endpoints
*Available only when `TEST_MODE=true`*

### Get Test Cities
Get list of available test cities for mock data.

**Endpoint:** `GET /api/test/cities`

**Response:**
```json
{
  "status": "success",
  "cities": ["London", "Tokyo", "New York", "Paris", "Sydney", "Mumbai"],
  "message": "Available test cities"
}
```

### Get Random Weather
Get weather data for a random test city.

**Endpoint:** `GET /api/test/weather/random`

**Parameters:**
- `units` (query) - Temperature units

**Response:**
Same structure as POST `/api/weather` but with mock data.

---

## Error Handling

### Common Error Response Format
```json
{
  "status": "error",
  "message": "Human-readable error description",
  "error_code": "ERROR_CODE",      // Optional
  "retry_after": 60               // Optional for rate limiting
}
```

### HTTP Status Codes

| Code | Description | Common Causes |
|------|-------------|---------------|
| 200  | Success | Request completed successfully |
| 400  | Bad Request | Missing city, invalid JSON, invalid units |
| 404  | Not Found | City not found, no cached data |
| 429  | Too Many Requests | Rate limit exceeded |
| 500  | Internal Server Error | API key issues, service unavailable |
| 503  | Service Unavailable | External API down, timeout |

### Error Categories

**Client Errors (4xx):**
- Invalid city names
- Missing required fields
- Rate limiting

**Server Errors (5xx):**
- External API failures
- Configuration issues
- Unexpected exceptions

---

## Caching Behavior

- Weather data cached for **15 minutes** (900 seconds)
- Cache key format: `{city_lowercase}_{units}`
- Cache hit indicated by `"cached": true` in response
- No cache for error responses

---

## Rate Limiting

- **Free Tier:** 60 requests/minute, 1000 requests/day
- Rate limit headers not exposed in current version
- `429` response includes `retry_after` field in seconds

---

## Request/Response Examples

### Successful Weather Request
```bash
curl -X POST http://localhost:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "Tokyo", "units": "metric"}'
```

### Error Cases

**Missing city:**
```bash
curl -X POST http://localhost:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Invalid city:**
```bash
curl -X POST http://localhost:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "InvalidCityName123"}'
```

**Imperial units:**
```bash
curl -X POST http://localhost:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "New York", "units": "imperial"}'
```