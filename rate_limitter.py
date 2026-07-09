import time
import threading

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        :param capacity: Max tokens a bucket can hold (Maximum burst size).
        :param refill_rate: How many tokens are added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        
        # State tracking: { "client_endpoint_key": {"tokens": float, "last_refill": float} }
        self.client_buckets = {}
        self.lock = threading.Lock()  # Ensures thread safety for concurrent API requests

    def is_allowed(self, client_ip: str, endpoint: str) -> bool:
        """
        Checks if a specific client is allowed to access a specific endpoint.
        """
        # Create a unique composite key combining IP and Endpoint
        client_key = f"{client_ip}:{endpoint}"
        now = time.time()

        with self.lock:
            # 1. Initialize the bucket if this is the first time seeing this IP + Endpoint combo
            if client_key not in self.client_buckets:
                self.client_buckets[client_key] = {
                    "tokens": float(self.capacity),
                    "last_refill": now
                }

            bucket = self.client_buckets[client_key]

            # 2. Lazy Refill: Calculate time elapsed and add tokens mathematically
            elapsed = now - bucket["last_refill"]
            generated_tokens = elapsed * self.refill_rate
            
            # Top off the bucket without exceeding max capacity
            bucket["tokens"] = min(self.capacity, bucket["tokens"] + generated_tokens)
            bucket["last_refill"] = now

            # 3. Evaluate Request
            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0  # Consume 1 token
                return True              # ALLOWED ✅
                
            return False                 # BLOCKED ❌ (Out of tokens)


# ==========================================
# SIMULATION / VERIFICATION (How it works at runtime)
# ==========================================
if __name__ == "__main__":
    # Configure: Max capacity of 2 requests, refills 1 token per second
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0)
    
    user_ip = "192.168.1.50"
    
    print("--- Simulating Heavy Traffic on /search Endpoint ---")
    # First 2 requests should pass (utilizing the burst capacity)
    print(f"Hit 1 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")
    print(f"Hit 2 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")
    # 3rd request fails because the /search bucket for this IP is empty
    print(f"Hit 3 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")

    print("\n--- Simulating Immediate Hit on a DIFFERENT Endpoint (/checkout) ---")
    # This passes instantly! Even though /search is blocked, /checkout has its own isolated bucket.
    print(f"Hit 1 (/checkout): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/checkout') else 'BLOCKED ❌'}")

    print("\n... Waiting 1.0 second for /search tokens to refill ...\n")
    time.sleep(1.0)

    print("--- Retrying /search Endpoint After Refill ---")
    # This passes now because 1 token refilled during the sleep period
    print(f"Hit 4 (/search): {'ALLOWED ✅' if limiter.is_allowed(user_ip, '/search') else 'BLOCKED ❌'}")