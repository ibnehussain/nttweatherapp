"""
Cache Service - Simple in-memory caching for weather data
"""

import time
import threading
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheService:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key (str): Cache key
            
        Returns:
            Any: Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            current_time = time.time()
            
            # Check if entry has expired
            if current_time > entry['expires_at']:
                del self._cache[key]
                logger.debug(f"Cache entry expired: {key}")
                return None
            
            logger.debug(f"Cache hit: {key}")
            return entry['value']
    
    def set(self, key: str, value: Any, ttl: int = 900) -> None:
        """
        Set value in cache with TTL
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            ttl (int): Time to live in seconds (default: 15 minutes)
        """
        with self._lock:
            expires_at = time.time() + ttl
            self._cache[key] = {
                'value': value,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key (str): Cache key
            
        Returns:
            bool: True if key existed, False otherwise
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache deleted: {key}")
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            logger.info(f"Cache cleared: {count} entries removed")
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache
        
        Returns:
            int: Number of entries removed
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time > entry['expires_at']
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            if expired_keys:
                logger.info(f"Cache cleanup: {len(expired_keys)} expired entries removed")
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            dict: Cache statistics including size, entries info
        """
        with self._lock:
            current_time = time.time()
            total_entries = len(self._cache)
            expired_entries = sum(
                1 for entry in self._cache.values()
                if current_time > entry['expires_at']
            )
            
            return {
                'total_entries': total_entries,
                'active_entries': total_entries - expired_entries,
                'expired_entries': expired_entries,
                'cache_keys': list(self._cache.keys())
            }
    
    def has_key(self, key: str) -> bool:
        """
        Check if key exists and is not expired
        
        Args:
            key (str): Cache key
            
        Returns:
            bool: True if key exists and is valid
        """
        return self.get(key) is not None
    
    def get_remaining_ttl(self, key: str) -> Optional[int]:
        """
        Get remaining TTL for a cache entry
        
        Args:
            key (str): Cache key
            
        Returns:
            int: Remaining seconds or None if key doesn't exist
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            current_time = time.time()
            
            if current_time > entry['expires_at']:
                return 0
            
            return int(entry['expires_at'] - current_time)