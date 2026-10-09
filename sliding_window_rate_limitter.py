import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window = window_seconds
        self.clients = {}  # key → deque of timestamps

    def is_allowed(self, user_id, endpoint):
        key = f"{user_id}:{endpoint}"
        now = time.time()

        if key not in self.clients:
            self.clients[key] = deque()

        q = self.clients[key]

        # 1. Remove old requests (outside window)
        while q and q[0] <= now - self.window:
            q.popleft()

        # 2. Check limit
        if len(q) < self.limit:
            q.append(now)
            return True

        return False