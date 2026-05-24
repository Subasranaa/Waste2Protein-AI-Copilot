# cache_service.py — production version
import hashlib
import json
import os
import redis
from app.logger import setup_logger

logger = setup_logger(__name__)

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            self.redis_client = redis.from_url(redis_url)
            self.use_redis = True
            logger.info("CacheService using Redis")
        else:
            self.cache = {}      # fallback to in-memory for local dev
            self.use_redis = False
            logger.warning("No REDIS_URL set — using in-memory cache (dev only)")

    def make_key(self, payload: dict) -> str:
        payload_string = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(payload_string.encode()).hexdigest()

    def get(self, key: str):
        if self.use_redis:
            try:
                value = self.redis_client.get(key)
                return json.loads(value) if value else None
            except Exception as e:
                logger.error(f"Redis get failed: {e}")
                return None
        return self.cache.get(key)

    def set(self, key: str, value: dict, ttl_seconds: int = 3600):
        # ttl = time to live — cache expires after 1 hour by default
        if self.use_redis:
            try:
                self.redis_client.setex(key, ttl_seconds, json.dumps(value))
            except Exception as e:
                logger.error(f"Redis set failed: {e}")
        else:
            self.cache[key] = value
