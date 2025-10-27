from django.core.cache import cache
from rest_framework.exceptions import Throttled
import time 


class SimpleRateLimiter:
    def __init__(self, rate_limit=1, period=60):
        """
        rate_limit: number of allowed requests
        period: in seconds (default: 60 seconds = 1 minute)
        """

        self.rate_limit = rate_limit
        self.period = period

    def check(self, key: str):
        """
        Raises Throttled if the limit is exceeded
        key: unique API key identifier
        """
        cache_key = f"ratelimit:{key}"
        data = cache.get(cache_key)

        now = time.time()
        if data:
            count, start_time = data
            if now - start_time < self.period:
                if count >= self.rate_limit:
                    remaining = int(self.period - (now - start_time))
                    raise Throttled(detail=f"Rate Limit exceeded. Try again in {remaining}")
                else:
                    cache.set(cache_key, (count + 1, start_time), self.period)
            else:
                cache.set(cache_key, (1, now), self.period)
        else:
            cache.set(cache_key, (1, now), self.period)