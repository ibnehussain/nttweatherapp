/**
 * Weather Dashboard JavaScript
 * Handles user interactions, API calls, and data display
 */

class WeatherDashboard {
    constructor() {
        this.apiBaseUrl = window.location.origin + '/api';
        this.currentUnits = 'metric';
        this.recentSearches = this.loadRecentSearches();
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.updateRecentSearches();
        this.setupEnterKeySupport();
    }

    bindEvents() {
        // Search functionality
        document.getElementById('searchBtn').addEventListener('click', () => {
            this.handleSearch();
        });

        // Units toggle
        document.querySelectorAll('input[name="units"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.currentUnits = e.target.value;
            });
        });

        // Error dismissal
        document.getElementById('dismissError').addEventListener('click', () => {
            this.hideError();
        });

        // Recent searches click events
        document.getElementById('recentList').addEventListener('click', (e) => {
            if (e.target.classList.contains('recent-item')) {
                const city = e.target.textContent;
                document.getElementById('cityInput').value = city;
                this.handleSearch();
            }
        });
    }

    setupEnterKeySupport() {
        document.getElementById('cityInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.handleSearch();
            }
        });
    }

    async handleSearch() {
        const cityInput = document.getElementById('cityInput');
        const city = cityInput.value.trim();

        if (!city) {
            this.showError('Please enter a city name');
            return;
        }

        if (city.length < 2) {
            this.showError('City name must be at least 2 characters long');
            return;
        }

        this.showLoading();
        this.hideError();

        try {
            const weatherData = await this.fetchWeatherData(city);
            
            if (weatherData.status === 'success') {
                this.displayWeatherData(weatherData.data);
                this.addToRecentSearches(city);
                cityInput.value = '';
            } else {
                this.showError(weatherData.message);
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Failed to fetch weather data. Please check your connection and try again.');
        } finally {
            this.hideLoading();
        }
    }

    async fetchWeatherData(city) {
        const response = await fetch(`${this.apiBaseUrl}/weather`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                city: city,
                units: this.currentUnits
            })
        });

        if (!response.ok) {
            if (response.status === 404) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'City not found');
            } else if (response.status === 429) {
                throw new Error('Too many requests. Please wait a moment before searching again.');
            } else {
                throw new Error('Weather service temporarily unavailable');
            }
        }

        return await response.json();
    }

    displayWeatherData(data) {
        // Show the weather display
        const weatherDisplay = document.getElementById('weatherDisplay');
        weatherDisplay.classList.add('visible');

        // Update city name and timestamp
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('timestamp').textContent = `Last updated: ${this.formatTimestamp(data.timestamp)}`;

        // Update weather icon
        const weatherIcon = document.getElementById('weatherIcon');
        weatherIcon.src = `https://openweathermap.org/img/wn/${data.current.icon}@2x.png`;
        weatherIcon.alt = data.current.description;

        // Update temperature display
        const tempUnit = data.units.temperature;
        document.getElementById('currentTemp').textContent = `${data.current.temperature}${tempUnit}`;
        document.getElementById('feelsLike').textContent = `Feels like ${data.current.feels_like}${tempUnit}`;
        
        // Update description
        document.getElementById('description').textContent = data.current.description;

        // Update weather details
        document.getElementById('highLow').textContent = `${data.current.temp_max}${tempUnit} / ${data.current.temp_min}${tempUnit}`;
        document.getElementById('humidity').textContent = `${data.current.humidity}%`;
        document.getElementById('pressure').textContent = `${data.current.pressure} ${data.units.pressure}`;
        document.getElementById('wind').textContent = `${data.current.wind_speed} ${data.units.wind_speed}`;
        
        // Handle visibility
        const visibility = data.current.visibility;
        document.getElementById('visibility').textContent = visibility !== 'N/A' 
            ? `${(visibility / 1000).toFixed(1)} km` 
            : 'N/A';

        // Update coordinates
        if (data.coordinates) {
            document.getElementById('coordinates').textContent = 
                `Coordinates: ${data.coordinates.lat.toFixed(2)}, ${data.coordinates.lon.toFixed(2)}`;
        }

        // Update sun times
        if (data.sun) {
            document.getElementById('sunriseTime').textContent = this.formatTime(data.sun.sunrise);
            document.getElementById('sunsetTime').textContent = this.formatTime(data.sun.sunset);
            document.getElementById('sunrise').textContent = this.formatTime(data.sun.sunrise);
        }

        // Scroll to weather display on mobile
        if (window.innerWidth <= 768) {
            weatherDisplay.scrollIntoView({ behavior: 'smooth' });
        }
    }

    showLoading() {
        document.getElementById('loadingIndicator').classList.remove('hidden');
        document.getElementById('searchBtn').disabled = true;
    }

    hideLoading() {
        document.getElementById('loadingIndicator').classList.add('hidden');
        document.getElementById('searchBtn').disabled = false;
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorContainer').classList.remove('hidden');
    }

    hideError() {
        document.getElementById('errorContainer').classList.add('hidden');
    }

    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        });
    }

    // Recent searches management
    addToRecentSearches(city) {
        // Remove if already exists
        const index = this.recentSearches.indexOf(city);
        if (index > -1) {
            this.recentSearches.splice(index, 1);
        }

        // Add to beginning
        this.recentSearches.unshift(city);

        // Keep only last 5 searches
        this.recentSearches = this.recentSearches.slice(0, 5);

        this.saveRecentSearches();
        this.updateRecentSearches();
    }

    updateRecentSearches() {
        const recentList = document.getElementById('recentList');
        
        if (this.recentSearches.length === 0) {
            recentList.innerHTML = '<p class="no-recent">No recent searches</p>';
            return;
        }

        recentList.innerHTML = this.recentSearches
            .map(city => `<span class="recent-item">${city}</span>`)
            .join('');
    }

    loadRecentSearches() {
        try {
            const saved = localStorage.getItem('weatherDashboard_recentSearches');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading recent searches:', error);
            return [];
        }
    }

    saveRecentSearches() {
        try {
            localStorage.setItem('weatherDashboard_recentSearches', 
                JSON.stringify(this.recentSearches));
        } catch (error) {
            console.error('Error saving recent searches:', error);
        }
    }

    // Health check for API connectivity
    async checkAPIHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('API Health:', data);
            return data.status === 'healthy';
        } catch (error) {
            console.error('API health check failed:', error);
            return false;
        }
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize the dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new WeatherDashboard();
    
    // Perform health check on load
    dashboard.checkAPIHealth().then(healthy => {
        if (!healthy) {
            console.warn('API health check failed - some features may not work');
        }
    });

    // Make dashboard available globally for debugging
    window.weatherDashboard = dashboard;
});

// Service Worker registration for PWA capabilities (optional enhancement)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .catch(error => {
                console.log('ServiceWorker registration failed');
            });
    });
}